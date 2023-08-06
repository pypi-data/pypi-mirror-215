from garlandtools.models.records.base_record import BaseRecord
from garlandtools.models.type import Type


class Item(BaseRecord):
    @property
    def TYPE(self) -> Type:
        """The type of the record."""
        return Type.ITEM

    @property
    def ilvl(self) -> int:
        """The item level of the item."""
        if self._data is not None:
            return self._data["ilvl"]
        if self._partial is not None:
            return self._partial.ilvl
        raise ValueError("Neither data nor partial is set.")

    @property
    def icon(self) -> str:
        """The icon of the item."""
        if self._data is not None:
            return self._data["icon"]
        if self._partial is not None:
            return self._partial.icon
        raise ValueError("Neither data nor partial is set.")

    @property
    def category(self) -> int:
        """The category of the item."""
        if self._data is not None:
            return self._data["category"]
        if self._partial is not None:
            return self._partial.category
        raise ValueError("Neither data nor partial is set.")

    @property
    def price(self) -> int:
        """The price of the item."""
        if self._data is not None:
            if "price" not in self._data:
                return 0
            return self._data["price"]
        if self._partial is not None:
            return self._partial.price
        raise ValueError("Neither data nor partial is set.")

    @property
    async def description(self) -> str | None:
        """The description of the item."""
        return await self._get("description")

    # @property
    # async def patch(self) -> int:
    #     return self.data["patch"]  # TODO: return a Patch object

    # @property
    # async def patchCategory(self) -> int:
    #     return self.data["patchCategory"]  # TODO: return a PatchCategory object

    @property
    async def tradeable(self) -> bool:
        return bool(await self._get("tradeable"))

    @property
    async def sell_price(self) -> int:
        return int(await self._get("sell_price"))  # type: ignore

    # @property
    # async def rarity(self) -> int:
    #     return self.data["rarity"]  # TODO: return a Rarity Enum

    @property
    async def stack_size(self) -> int | None:
        """The maximum number of items that can be stacked together."""
        return await self._get("stackSize")

    # @property
    # def nodes(self):
    #     return self.data['nodes']
    # @property
    # def vendors(self):
    #     return self.data['vendors']
    # @property
    # def ingredient_of(self):
    #     return self.data['ingredient_of']
    # @property
    # def leves(self):
    #     return self.data['leves']
    # @property
    # def ventures(self):
    #     return self.data['ventures']
