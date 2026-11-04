from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain import Order
from src.repository import OrderRow, SqlOrderRepository, make_engine


def test_repository_commit():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(1, Order(120))
        session.commit()
        assert session.scalar(select(OrderRow).where(OrderRow.id == 1)).total == 120

def test_repository_rollback():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(1, Order(120))
        session.rollback()
        assert session.scalar(select(OrderRow).where(OrderRow.id == 1)) is None

def test_repository_commit_id_2():
    """Nueva prueba: guarda un pedido de total 250 con id=2, hace commit y verifica id, total y estado"""
    engine = make_engine()
    with Session(engine) as session:
        order = Order(250)
        order.confirm()  # Cambia el estado a CONFIRMED y valida el total
        SqlOrderRepository(session).save(2, order)
        session.commit()

        row = session.scalar(select(OrderRow).where(OrderRow.id == 2))
        assert row is not None
        assert row.id == 2
        assert row.total == 250
        assert row.status == "CONFIRMED"