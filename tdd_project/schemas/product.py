from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import AfterValidator, Field
from tdd_project.schemas.base import BaseSchemaMixin, OutMixin


class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn, OutMixin):
    ...


def convert_decimal_128(valor):
    return Decimal128(str(valor))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdate(BaseSchemaMixin):
    updated_at: Optional[datetime] = Field(None, description="Product updated time")
    quantity: Optional[int] = Field(0, description="Product quantity")
    price: Optional[Decimal_] = Field("0.0", description="Product price")
    status: Optional[bool] = Field(True, description="Product status")

    # @field_validator('quantity', 'price', 'status', check_fields=True)
    # def prevent_none(cls, value):
    #     assert value is not None, 'field may not be None'
    #     return value


class ProductUpdateOut(ProductOut):
    ...
