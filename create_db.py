import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Session, select
from db import database_engine
from models import (
    Role,
    User,
    PickupPoint,
    OrderStatus,
    Category,
    Manufacturer,
    Supplier,
    Unit,
    Product,
    Order,
    OrderProduct,
)


def initialize_tables():
    # Создает таблицы только если их еще нет в БД
    SQLModel.metadata.create_all(database_engine)


def seed_data_if_empty():
    with Session(database_engine) as session:
        existing_products = session.exec(select(Product)).first()
        if existing_products:
            print("База данных уже содержит данные. Пропускаем импорт.")
            return

        roles = [
            Role(id=1, role_name="Администратор"),
            Role(id=2, role_name="Менеджер"),
            Role(id=3, role_name="Авторизированный клиент"),
        ]
        session.add_all(roles)

        units = [Unit(id=1, unit_name="шт.")]
        session.add_all(units)

        statuses = [
            OrderStatus(id=1, status_name="Новый"),
            OrderStatus(id=2, status_name="Завершен"),
        ]
        session.add_all(statuses)

        categories = [
            Category(id=1, category_name="Велосипед взрослый горный"),
            Category(id=2, category_name="Велосипед городской подростковый"),
            Category(id=3, category_name="Велосипед городской взрослый"),
            Category(id=4, category_name="Велосипед детский горный"),
            Category(id=5, category_name="Велосипед детский городской"),
        ]
        session.add_all(categories)

        suppliers = [
            Supplier(id=1, supplier_name="ВелоСтрана"),
            Supplier(id=2, supplier_name="ЯндексМаркет"),
            Supplier(id=3, supplier_name="Скилс"),
            Supplier(id=4, supplier_name="ПерспективаГрупп"),
            Supplier(id=5, supplier_name="kari"),
        ]
        session.add_all(suppliers)

        manufacturers = [
            Manufacturer(id=1, manufacturer_name="Slash"),
            Manufacturer(id=2, manufacturer_name="Shimano"),
            Manufacturer(id=3, manufacturer_name="Skill bike"),
            Manufacturer(id=4, manufacturer_name="NEXT"),
            Manufacturer(id=5, manufacturer_name="Aero"),
            Manufacturer(id=6, manufacturer_name="Fizard"),
            Manufacturer(id=7, manufacturer_name="kari"),
        ]
        session.add_all(manufacturers)

        session.commit()
        print("Базовые таблицы успешно инициализированы!")


if __name__ == "__main__":
    initialize_tables()
    seed_data_if_empty()