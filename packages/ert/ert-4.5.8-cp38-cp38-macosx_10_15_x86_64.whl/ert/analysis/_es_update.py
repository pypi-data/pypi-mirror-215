from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

import iterative_ensemble_smoother as ies
import numpy as np
from iterative_ensemble_smoother.experimental import (
    ensemble_smoother_update_step_row_scaling,
)

from ert._c_wrappers.enkf import ActiveMode
from ert._c_wrappers.enkf.enums import RealizationStateEnum
from ert._c_wrappers.enkf.row_scaling import RowScaling
from ert._clib import update

if TYPE_CHECKING:
    import numpy.typing as npt

    from ert._c_wrappers.analysis import AnalysisModule
    from ert._c_wrappers.analysis.configuration import UpdateConfiguration
    from ert._c_wrappers.enkf import EnKFMain
    from ert._c_wrappers.enkf.analysis_config import AnalysisConfig
    from ert._c_wrappers.enkf.enkf_fs import EnkfFs
    from ert._c_wrappers.enkf.enkf_obs import EnkfObs
    from ert._c_wrappers.enkf.ensemble_config import EnsembleConfig
    from ert._clib.enkf_analysis import UpdateSnapshot

logger = logging.getLogger(__name__)


class ErtAnalysisError(Exception):
    pass


@dataclass
class SmootherSnapshot:
    source_case: str
    target_case: str
    analysis_module: str
    analysis_configuration: Dict[str, Any]
    alpha: float
    std_cutoff: float
    update_step_snapshots: Dict[str, "UpdateSnapshot"] = field(default_factory=dict)


def _get_A_matrix(
    temporary_storage: Dict[str, "npt.NDArray[np.double]"],
    parameters: List[update.Parameter],
) -> Optional["npt.NDArray[np.double]"]:
    matrices: List["npt.NDArray[np.double]"] = []
    for p in parameters:
        if p.active_list.getMode() == ActiveMode.ALL_ACTIVE:
            matrices.append(temporary_storage[p.name])
        elif p.active_list.getMode() == ActiveMode.PARTLY_ACTIVE:
            matrices.append(
                temporary_storage[p.name][p.active_list.get_active_index_list(), :]
            )
    return np.vstack(matrices) if matrices else None


def _param_ensemble_for_projection(
    temp_storage: Dict[str, npt.NDArray[np.double]],
    ensemble_size: int,
    updatestep: UpdateConfiguration,
) -> Optional[npt.NDArray[np.double]]:
    """Responses must be projected when num_params < ensemble_size - 1.
    The number of parameters here refers to the total number of parameters used to
    drive the model and not the number of parameters in a local update step.

    Scenario 1:
        - p < N - 1, meaning that projection needs to be done.
        - User wants to loop through each parameter and update it separately,
          perhaps to do distance based localization.
        In this case, we need to pass `param_ensemble` to the smoother
        so that the responses are projected using the same `param_ensemble`
        in every loop.
    Scenario 2:
        - p > N - 1, meaning that projection is not necessary.
        - User wants to loop through every parameter as in Scenario 1.
        In this case `param_ensemble` should be `None` which means
        that no projection will be done even when updating a single parameter.
    """
    num_params = sum(arr.shape[0] for arr in temp_storage.values())
    if num_params < ensemble_size - 1:
        _params: List[List[update.Parameter]] = [
            update_step.parameters for update_step in updatestep
        ]
        # Flatten list of lists
        params: List[update.Parameter] = [
            item for sublist in _params for item in sublist
        ]
        return _get_A_matrix(temp_storage, params)
    return None


def _get_row_scaling_A_matrices(
    temporary_storage: Dict[str, "npt.NDArray[np.double]"],
    parameters: List[update.RowScalingParameter],
) -> List[Tuple["npt.NDArray[np.double]", RowScaling]]:
    matrices = []
    for p in parameters:
        if p.active_list.getMode() == ActiveMode.ALL_ACTIVE:
            matrices.append((temporary_storage[p.name], p.row_scaling))
        elif p.active_list.getMode() == ActiveMode.PARTLY_ACTIVE:
            matrices.append(
                (
                    temporary_storage[p.name][p.active_list.get_active_index_list(), :],
                    p.row_scaling,
                ),
            )

    return matrices


def _save_to_temporary_storage(
    temporary_storage: Dict[str, "npt.NDArray[np.double]"],
    parameters: List[update.Parameter],
    A: Optional["npt.NDArray[np.double]"],
) -> None:
    if A is None:
        return
    offset = 0
    for p in parameters:
        if p.active_list.getMode() == ActiveMode.ALL_ACTIVE:
            rows = temporary_storage[p.name].shape[0]
            temporary_storage[p.name] = A[offset : offset + rows, :]
            offset += rows
        elif p.active_list.getMode() == ActiveMode.PARTLY_ACTIVE:
            row_indices = p.active_list.get_active_index_list()
            for i, row in enumerate(row_indices):
                temporary_storage[p.name][row] = A[offset + i]
            offset += len(row_indices)


def _save_temporary_storage_to_disk(
    target_fs: "EnkfFs",
    ensemble_config: "EnsembleConfig",
    temporary_storage: Dict[str, "npt.NDArray[np.double]"],
    iens_active_index: List[int],
) -> None:
    for key, matrix in temporary_storage.items():
        config_node = ensemble_config.getNode(key)
        target_fs.save_parameters(
            config_node=config_node,
            iens_active_index=iens_active_index,
            parameter=update.Parameter(key),
            values=matrix,
        )


def _create_temporary_parameter_storage(
    source_fs: "EnkfFs",
    ensemble_config: "EnsembleConfig",
    iens_active_index: List[int],
) -> Dict[str, "npt.NDArray[np.double]"]:
    temporary_storage = {}
    for key in ensemble_config.parameters:
        config_node = ensemble_config.getNode(key)
        matrix = source_fs.load_parameter(
            config_node=config_node,
            iens_active_index=iens_active_index,
            parameter=update.Parameter(key),
        )
        temporary_storage[key] = matrix
    return temporary_storage


def analysis_ES(
    updatestep: "UpdateConfiguration",
    obs: "EnkfObs",
    rng: np.random.Generator,
    module: "AnalysisModule",
    alpha: float,
    std_cutoff: float,
    global_scaling: float,
    smoother_snapshot: SmootherSnapshot,
    ens_mask: List[bool],
    ensemble_config: "EnsembleConfig",
    source_fs: "EnkfFs",
    target_fs: "EnkfFs",
) -> None:
    iens_active_index = [i for i in range(len(ens_mask)) if ens_mask[i]]

    temp_storage = _create_temporary_parameter_storage(
        source_fs, ensemble_config, iens_active_index
    )

    ensemble_size = sum(ens_mask)
    param_ensemble = _param_ensemble_for_projection(
        temp_storage, ensemble_size, updatestep
    )

    # Looping over local analysis update_step
    for update_step in updatestep:
        try:
            S, observation_handle = update.load_observations_and_responses(
                source_fs,
                obs,
                alpha,
                std_cutoff,
                global_scaling,
                ens_mask,
                update_step.observation_config(),
            )
        except IndexError as e:
            raise ErtAnalysisError(e) from e

        # pylint: disable=unsupported-assignment-operation
        smoother_snapshot.update_step_snapshots[
            update_step.name
        ] = observation_handle.update_snapshot
        observation_values = observation_handle.observation_values
        observation_errors = observation_handle.observation_errors
        if len(observation_values) == 0:
            raise ErtAnalysisError(
                f"No active observations for update step: {update_step.name}."
            )

        A = _get_A_matrix(temp_storage, update_step.parameters)
        A_with_rowscaling = _get_row_scaling_A_matrices(
            temp_storage, update_step.row_scaling_parameters
        )
        noise = rng.standard_normal(size=(len(observation_values), S.shape[1]))

        if A is not None:
            smoother = ies.ES()
            smoother.fit(
                S,
                observation_errors,
                observation_values,
                noise=noise,
                truncation=module.get_truncation(),
                inversion=ies.InversionType(module.inversion),
                param_ensemble=param_ensemble,
            )
            A = smoother.update(A)
            _save_to_temporary_storage(temp_storage, update_step.parameters, A)
        if A_with_rowscaling:
            A_with_rowscaling = ensemble_smoother_update_step_row_scaling(
                S,
                A_with_rowscaling,
                observation_errors,
                observation_values,
                noise,
                module.get_truncation(),
                ies.InversionType(module.inversion),
            )
            for parameter, (A, _) in zip(
                update_step.row_scaling_parameters, A_with_rowscaling
            ):
                _save_to_temporary_storage(temp_storage, [parameter], A)

    _save_temporary_storage_to_disk(
        target_fs, ensemble_config, temp_storage, iens_active_index
    )


def analysis_IES(
    updatestep: "UpdateConfiguration",
    obs: "EnkfObs",
    rng: np.random.Generator,
    module: "AnalysisModule",
    alpha: float,
    std_cutoff: float,
    global_scaling: float,
    smoother_snapshot: SmootherSnapshot,
    ens_mask: List[bool],
    ensemble_config: "EnsembleConfig",
    source_fs: "EnkfFs",
    target_fs: "EnkfFs",
    iterative_ensemble_smoother: ies.SIES,
) -> None:
    iens_active_index = [i for i in range(len(ens_mask)) if ens_mask[i]]

    temp_storage = _create_temporary_parameter_storage(
        source_fs, ensemble_config, iens_active_index
    )

    ensemble_size = sum(ens_mask)
    param_ensemble = _param_ensemble_for_projection(
        temp_storage, ensemble_size, updatestep
    )

    # Looping over local analysis update_step
    for update_step in updatestep:
        try:
            S, observation_handle = update.load_observations_and_responses(
                source_fs,
                obs,
                alpha,
                std_cutoff,
                global_scaling,
                ens_mask,
                update_step.observation_config(),
            )
        except IndexError as e:
            raise ErtAnalysisError(e)
        # pylint: disable=unsupported-assignment-operation
        smoother_snapshot.update_step_snapshots[
            update_step.name
        ] = observation_handle.update_snapshot
        observation_values = observation_handle.observation_values
        observation_errors = observation_handle.observation_errors
        if len(observation_values) == 0:
            raise ErtAnalysisError(
                f"No active observations for update step: {update_step.name}."
            )

        A = _get_A_matrix(temp_storage, update_step.parameters)

        noise = rng.standard_normal(size=(len(observation_values), S.shape[1]))

        iterative_ensemble_smoother.fit(
            S,
            observation_errors,
            observation_values,
            noise=noise,
            ensemble_mask=np.array(ens_mask),
            truncation=module.get_truncation(),
            inversion=ies.InversionType(module.inversion),
            param_ensemble=param_ensemble,
        )
        A = iterative_ensemble_smoother.update(A)
        _save_to_temporary_storage(temp_storage, update_step.parameters, A)

    _save_temporary_storage_to_disk(
        target_fs, ensemble_config, temp_storage, iens_active_index
    )


def _write_update_report(fname: Path, snapshot: SmootherSnapshot) -> None:
    # Make sure log file parents exist
    fname.parent.mkdir(parents=True, exist_ok=True)
    for update_step_name, update_step in snapshot.update_step_snapshots.items():
        with open(fname, "w", encoding="utf-8") as fout:
            fout.write("=" * 127 + "\n")
            fout.write("Report step...: deprecated\n")
            fout.write(f"Update step......: {update_step_name:<10}\n")
            fout.write("-" * 127 + "\n")
            fout.write(
                "Observed history".rjust(73)
                + "|".rjust(16)
                + "Simulated data".rjust(27)
                + "\n".rjust(9)
            )
            fout.write("-" * 127 + "\n")
            for nr, (name, val, std, status, ens_val, ens_std) in enumerate(
                zip(
                    update_step.obs_name,
                    update_step.obs_value,
                    update_step.obs_std,
                    update_step.obs_status,
                    update_step.response_mean,
                    update_step.response_std,
                )
            ):
                if status in ["DEACTIVATED", "LOCAL_INACTIVE"]:
                    status = "Inactive"
                fout.write(
                    f"{nr+1:^6}: {name:30} {val:>16.3f} +/- {std:>17.3f} "
                    f"{status.capitalize():9} | {ens_val:>17.3f} +/- {ens_std:>15.3f}  "
                    f"\n"
                )
            fout.write("=" * 127 + "\n")


def _assert_has_enough_realizations(
    ens_mask: List[bool], analysis_config: "AnalysisConfig"
) -> None:
    active_realizations = sum(ens_mask)
    if not analysis_config.have_enough_realisations(active_realizations):
        raise ErtAnalysisError(
            f"There are {active_realizations} active realisations left, which is "
            "less than the minimum specified - stopping assimilation.",
        )


def _create_smoother_snapshot(
    prior_name: "str", posterior_name: "str", analysis_config: "AnalysisConfig"
) -> SmootherSnapshot:
    return SmootherSnapshot(
        prior_name,
        posterior_name,
        analysis_config.active_module_name(),
        analysis_config.get_active_module().variable_value_dict(),
        analysis_config.get_enkf_alpha(),
        analysis_config.get_std_cutoff(),
    )


class ESUpdate:
    def __init__(self, enkf_main: "EnKFMain"):
        self.ert = enkf_main
        self.update_snapshots: Dict[str, SmootherSnapshot] = {}

    def smootherUpdate(
        self, prior_storage: "EnkfFs", posterior_storage: "EnkfFs", run_id: str
    ) -> None:
        updatestep = self.ert.getLocalConfig()

        analysis_config = self.ert.analysisConfig()

        obs = self.ert.getObservations()
        ensemble_config = self.ert.ensembleConfig()

        alpha = analysis_config.get_enkf_alpha()
        std_cutoff = analysis_config.get_std_cutoff()
        global_scaling = analysis_config.get_global_std_scaling()
        source_state_map = prior_storage.getStateMap()
        ens_mask = source_state_map.selectMatching(RealizationStateEnum.STATE_HAS_DATA)
        _assert_has_enough_realizations(ens_mask, analysis_config)

        smoother_snapshot = _create_smoother_snapshot(
            prior_storage.case_name, posterior_storage.case_name, analysis_config
        )

        analysis_ES(
            updatestep,
            obs,
            self.ert.rng(),
            analysis_config.get_active_module(),
            alpha,
            std_cutoff,
            global_scaling,
            smoother_snapshot,
            ens_mask,
            ensemble_config,
            prior_storage,
            posterior_storage,
        )

        _write_update_report(
            Path(analysis_config.get_log_path()) / "deprecated", smoother_snapshot
        )

        self.update_snapshots[run_id] = smoother_snapshot

    def iterative_smoother_update(
        self,
        prior_storage: "EnkfFs",
        posterior_storage: "EnkfFs",
        w_container: ies.SIES,
        run_id: str,
    ) -> None:
        updatestep = self.ert.getLocalConfig()
        if len(updatestep) > 1:
            raise ErtAnalysisError(
                "Can not combine IES_ENKF modules with multi step updates"
            )

        analysis_config = self.ert.analysisConfig()

        obs = self.ert.getObservations()
        ensemble_config = self.ert.ensembleConfig()

        alpha = analysis_config.get_enkf_alpha()
        std_cutoff = analysis_config.get_std_cutoff()
        global_scaling = analysis_config.get_global_std_scaling()
        source_state_map = prior_storage.getStateMap()
        ens_mask = source_state_map.selectMatching(RealizationStateEnum.STATE_HAS_DATA)

        _assert_has_enough_realizations(ens_mask, analysis_config)

        smoother_snapshot = _create_smoother_snapshot(
            prior_storage.case_name, posterior_storage.case_name, analysis_config
        )

        analysis_IES(
            updatestep,
            obs,
            self.ert.rng(),
            analysis_config.get_active_module(),
            alpha,
            std_cutoff,
            global_scaling,
            smoother_snapshot,
            ens_mask,
            ensemble_config,
            prior_storage,
            posterior_storage,
            w_container,
        )

        _write_update_report(
            Path(analysis_config.get_log_path()) / "deprecated", smoother_snapshot
        )

        self.update_snapshots[run_id] = smoother_snapshot
