from ai.safety.sql_guard import is_safe_select


def test_safe_select_allow():
    assert is_safe_select("SELECT * FROM vw_monthly_revenue LIMIT 10")


def test_safe_select_block():
    assert not is_safe_select("DELETE FROM fact_sales")
    assert not is_safe_select("SELECT * FROM fact_sales; DROP TABLE fact_sales")
