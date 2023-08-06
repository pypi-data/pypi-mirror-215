from garlandtools.models.partials.partial import Partial


class ItemPartial(Partial):
    @property
    def ilvl(self) -> int:
        """The item level of the item."""
        return self._data["l"]

    @property
    def icon(self) -> str:
        """The icon of the item."""
        return self._data["c"]

    @property
    def category(self) -> int:
        """The category of the item."""
        return self._data["t"]

    @property
    def price(self) -> int:
        """The price of the item."""
        if "p" not in self._data:
            return 0
        return self._data["p"]
