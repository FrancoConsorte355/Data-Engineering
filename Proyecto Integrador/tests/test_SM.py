# tests/test_SM.py

import os, sys
# Inserta la carpeta padre (Proyecto Integrador) en sys.path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import pytest
from src.models.producto import PriceNormal, PriceDescount

def test_price_normal():
    assert PriceNormal().calcular(2, 3) == 6

@pytest.mark.parametrize("discount, price, qty, expected", [
    (0.10, 100, 1, 90),
    (0.25, 200, 2, 300),
    (0.0,   50,  3, 150),
])
def test_price_discount(discount, price, qty, expected):
    strat = PriceDescount(discount)
    assert strat.calcular(price, qty) == pytest.approx(expected)
