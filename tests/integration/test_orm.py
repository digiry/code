# test_orm은 ORM과 DB가 잘 연동되었는지 확인하는 테스트이다.
# 사실 ORM을 사용자가 테스트할 필요는 없다. ORM 개발자가 할 일이기 때문이다.
# test_orm은 ORM 초보 사용자에게 학습 목적으로 만든다.
from allocation.domain import model


# DB에 테스트 데이터를 수동을 넣고 ORM으로 전체 row들을 query할 때 Model 객체로 제대로 반환하는지 확인하는 테스트
def test_orderline_mapper_can_load_lines(session):
    # 준비
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )

    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]

    # 실행, 검증
    assert session.query(model.OrderLine).all() == expected


# Model 객체로 ORM에 데이터를 추가할 경우 제대로 추가되었는지 확인하는 테스트
def test_orderline_mapper_can_save_lines(session):
    # 준비
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)

    # 실행
    session.add(new_line)
    session.commit()

    # 검증 준비
    rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
    # 검증
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
