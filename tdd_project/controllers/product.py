from decimal import Decimal
from typing import List
from bson import Decimal128
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from tdd_project.core.exceptions import NotFoundException
from tdd_project.schemas.product import (
    ProductIn,
    ProductOut,
    ProductUpdate,
    ProductUpdateOut,
)
from tdd_project.usecases.product import ProductUseCase

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUseCase = Depends()
) -> ProductOut:
    try:
        if body.price > Decimal("5.000") and body.price < Decimal("8.000"):
            return await usecase.create(body=body)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Preço fora do limite esperado: (price > 5000 and price < 8000)",
            )
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUseCase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUseCase = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUseCase = Depends(),
) -> ProductUpdateOut:
    try:
        product = await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

    if not body.quantity:
        body.quantity = product.quantity
    elif not body.price:
        body.price = product.price
    elif not body.status:
        body.status = product.status

    if isinstance(body.price, Decimal128):
        body.price = str(body.price)

    return await usecase.update(id=id, body=body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUseCase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
