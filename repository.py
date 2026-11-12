from typing import Any, Dict, List
from sqlmodel import Session, select
from models import Category, Manufacturer, Product, Supplier, Unit


def get_all_products_with_relations(session: Session) -> List[Dict[str, Any]]:
    # Выборка товаров со всеми справочными полями через JOIN
    query = (
        select(
            Product.sku,
            Product.product_name,
            Category.category_name,
            Product.description,
            Manufacturer.manufacturer_name,
            Supplier.supplier_name,
            Product.price,
            Unit.unit_name,
            Product.quantity_in_stock,
            Product.discount,
            Product.photo,
        )
        .join(Category, Product.category_id == Category.id)
        .join(Manufacturer, Product.manufacturer_id == Manufacturer.id)
        .join(Supplier, Product.supplier_id == Supplier.id)
        .join(Unit, Product.unit_id == Unit.id)
        .order_by(Product.product_name)
    )

    db_rows = session.exec(query).all()
    products_collection = []

    for item in db_rows:
        product_record = {
            "sku": item[0],
            "product_name": item[1],
            "category_name": item[2],
            "description": item[3],
            "manufacturer_name": item[4],
            "supplier_name": item[5],
            "price": float(item[6]),
            "unit_name": item[7],
            "quantity_in_stock": item[8],
            "discount": item[9],
            "photo": item[10],
        }
        products_collection.append(product_record)

    return products_collection