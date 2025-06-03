# tests/test_sales_builder.py

import pytest
from datetime import time
from src.models.sales import SalesBuilder, Sales


def test_sales_builder_successful_build():
    """
    Verifica que SalesBuilder construya correctamente una instancia de Sales cuando se proveen todos los campos obligatorios.
    """
    # Datos de ejemplo
    builder = SalesBuilder()
    sales_obj = (
        builder
        .set_sales_id(1001)
        .set_sales_person_id(10)
        .set_customer_id(500)
        .set_product_id(200)
        .set_quantity(5.0)
        .set_discount(0.15)
        .set_total_price(425.0)
        .set_sales_date(time(hour=14, minute=30, second=0))
        .set_transaction_number("ABC123XYZ")
        .build()
    )
    # Verificar tipo y valores internos
    assert isinstance(sales_obj, Sales)
    assert sales_obj.SalesID == 1001
    assert sales_obj.SalesPersonID == 10
    assert sales_obj.CustomerID == 500
    assert sales_obj.ProductID == 200
    assert sales_obj.Quantity == 5.0
    assert sales_obj.Discount == 0.15
    assert sales_obj.TotalPrice == 425.0
    assert sales_obj.SalesDate == time(14, 30, 0)
    assert sales_obj.TransactionNumber == "ABC123XYZ"


def test_sales_builder_missing_fields_raises_error():
    """
    Verifica que SalesBuilder lance ValueError cuando falta algún campo obligatorio.
    """
    builder = SalesBuilder()
    # Solo seteamos algunos campos, dejamos fuera SalesDate y TransactionNumber
    builder = (
        builder
        .set_sales_id(1002)
        .set_sales_person_id(11)
        .set_customer_id(501)
        .set_product_id(201)
        .set_quantity(3.0)
        .set_discount(0.10)
        .set_total_price(270.0)
        # Sin llamar a set_sales_date ni set_transaction_number
    )
    with pytest.raises(ValueError) as excinfo:
        _ = builder.build()
    # Debe mencionar los campos faltantes en el mensaje de error
    error_msg = str(excinfo.value)
    assert "SalesDate" in error_msg or "TransactionNumber" in error_msg