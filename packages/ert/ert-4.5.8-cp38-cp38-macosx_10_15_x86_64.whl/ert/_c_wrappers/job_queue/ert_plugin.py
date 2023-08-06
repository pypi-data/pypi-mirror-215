from .ert_script import ErtScript


class CancelPluginException(Exception):
    """Raised when a plugin is cancelled."""


class ErtPlugin(ErtScript):
    def getArguments(self, parent=None):
        """@rtype: list"""
        return []

    def getName(self) -> str:
        return str(self.__class__)

    def getDescription(self) -> str:
        return "No description provided!"
