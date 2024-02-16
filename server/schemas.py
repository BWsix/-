from pydantic import BaseModel, HttpUrl


class ItemBase(BaseModel):
    url: HttpUrl


class ItemCreate(ItemBase):
    id: str | None = None


class Item(ItemBase):
    id: str

    class Config:
        from_attributes = True
