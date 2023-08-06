class Partial:
    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self) -> int:
        """The ID of the partial record."""
        return self._data["i"]

    @property
    def name(self) -> str:
        """The name of the partial record."""
        return self._data["n"]
