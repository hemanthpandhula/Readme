FORBIDDEN = {"insert", "update", "delete", "drop", "alter", "truncate", "create", ";", "--", "/*", "*/"}


def is_safe_select(sql: str) -> bool:
    s = sql.strip().lower()
    if not s.startswith("select"):
        return False
    return not any(token in s for token in FORBIDDEN)
