from datetime import date
from decimal import Decimal
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Role(SQLModel, table=True):
    __tablename__ = "role"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(unique=True, max_length=50, nullable=False)

    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: int = Field(foreign_key="role.id", nullable=False)
    full_name: str = Field(max_length=150, nullable=False)
    login: str = Field(unique=True, max_length=100, nullable=False)
    password: str = Field(max_length=100, nullable=False)

    role: Optional[Role] = Relationship(back_populates="users")
    orders: List["Order"] = Relationship(back_populates="client")


class PickupPoint(SQLModel, table=True):
    __tablename__ = "pickup_point"

    id: int = Field(primary_key=True)
    address: str = Field(max_length=255, nullable=False)

    orders: List["Order"] = Relationship(back_populates="pickup_point")


class OrderStatus(SQLModel, table=True):
    __tablename__ = "order_status"

    id: Optional[int] = Field(default=None, primary_key=True)
    status_name: str = Field(unique=True, max_length=50, nullable=False)

    orders: List["Order"] = Relationship(back_populates="status")


class Category(SQLModel, table=True):
    __tablename__ = "category"

    id: Optional[int] = Field(default=None, primary_key=True)
    category_name: str = Field(unique=True, max_length=100, nullable=False)

    products: List["Product"] = Relationship(back_populates="category")


class Manufacturer(SQLModel, table=True):
    __tablename__ = "manufacturer"

    id: Optional[int] = Field(default=None, primary_key=True)
    manufacturer_name: str = Field(unique=True, max_length=100, nullable=False)

    products: List["Product"] = Relationship(back_populates="manufacturer")


class Supplier(SQLModel, table=True):
    __tablename__ = "supplier"

    id: Optional[int] = Field(default=None, primary_key=True)
    supplier_name: str = Field(unique=True, max_length=100, nullable=False)

    products: List["Product"] = Relationship(back_populates="supplier")


class Unit(SQLModel, table=True):
    __tablename__ = "unit"

    id: Optional[int] = Field(default=None, primary_key=True)
    unit_name: str = Field(unique=True, max_length=20, nullable=False)

    products: List["Product"] = Relationship(back_populates="unit")


class OrderProduct(SQLModel, table=True):
    __tablename__ = "order_product"

    order_id: int = Field(
        foreign_key="orders.id",
        primary_key=True,
        nullable=False,
    )
    product_sku: str = Field(
        foreign_key="product.sku",
        primary_key=True,
        nullable=False,
    )
    quantity: int = Field(nullable=False)

    order: Optional["Order"] = Relationship(back_populates="order_products")
    product: Optional["Product"] = Relationship(back_populates="order_products")


class Product(SQLModel, table=True):
    __tablename__ = "product"

    sku: str = Field(primary_key=True, max_length=50)
    product_name: str = Field(max_length=255, nullable=False)
    unit_id: int = Field(foreign_key="unit.id", nullable=False)
    price: Decimal = Field(default=Decimal("0.00"), nullable=False)
    supplier_id: int = Field(foreign_key="supplier.id", nullable=False)
    manufacturer_id: int = Field(foreign_key="manufacturer.id", nullable=False)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    discount: int = Field(default=0, nullable=False)
    quantity_in_stock: int = Field(default=0, nullable=False)
    description: Optional[str] = Field(default=None)
    photo: Optional[str] = Field(default=None, max_length=255)

    unit: Optional[Unit] = Relationship(back_populates="products")
    supplier: Optional[Supplier] = Relationship(back_populates="products")
    manufacturer: Optional[Manufacturer] = Relationship(
        back_populates="products"
    )
    category: Optional[Category] = Relationship(back_populates="products")
    order_products: List[OrderProduct] = Relationship(back_populates="product")


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int = Field(primary_key=True)
    order_date: date = Field(nullable=False)
    delivery_date: date = Field(nullable=False)
    pickup_point_id: int = Field(foreign_key="pickup_point.id", nullable=False)
    client_id: int = Field(foreign_key="user.id", nullable=False)
    pickup_code: int = Field(nullable=False)
    status_id: int = Field(foreign_key="order_status.id", nullable=False)

    pickup_point: Optional[PickupPoint] = Relationship(back_populates="orders")
    client: Optional[User] = Relationship(back_populates="orders")
    status: Optional[OrderStatus] = Relationship(back_populates="orders")
    order_products: List[OrderProduct] = Relationship(back_populates="order")