import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from garlandtools.models.records.factory import partial_factory
from garlandtools.models.type import Type

if TYPE_CHECKING:
    from garlandtools.client import Client

from garlandtools.models.partials.item_partial import ItemPartial


class BaseRecord(ABC):
    @property
    @abstractmethod
    def TYPE(self) -> Type:
        """The type of the record."""

    @property
    def id(self) -> int:
        """The ID of the item record."""
        if self._data is not None:
            return self._data["id"]
        if self._partial is not None:
            return self._partial.id
        raise ValueError("Neither data nor partial is set.")

    @property
    def name(self) -> str:
        """The name of the item record."""
        if self._data is not None:
            return self._data["name"]
        if self._partial is not None:
            return self._partial.name
        raise ValueError("Neither data nor partial is set.")

    def __init__(
        self,
        client: "Client",
        data: dict | None = None,
        partial: ItemPartial | None = None,
        related_records: list["BaseRecord"] = [],
    ):
        if data is None and partial is None:
            raise ValueError("Either data or partial must be provided.")
        self._client = client
        self._data = data
        self._partial = partial
        self._related_records = related_records
        self._fetch_lock = asyncio.Lock()

    async def _get(self, key: str) -> Any | None:
        if self._data is not None:
            return self._data[key]

        async with self._fetch_lock:
            # Check again in case another coroutine
            # fetched the data while we were waiting
            if self._data is not None:
                return self._data[key]
            record_data = await self._client._get_by_id(self.id, self.TYPE)
            self._data = record_data[self.TYPE.value]
            self._related_records = [
                partial_factory(partial, client=self._client)
                for partial in record_data["partials"]
            ]
            return self._data[key]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id=}, {self.name=}>"
