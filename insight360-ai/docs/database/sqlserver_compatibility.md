# SQL Server Compatibility Notes

- Replace `BIGSERIAL` with `BIGINT IDENTITY(1,1)`.
- Replace `ON CONFLICT DO NOTHING` with `MERGE` or `IF NOT EXISTS` patterns.
- Replace `TO_CHAR(date, 'YYYYMMDD')::INT` with `CONVERT(INT, FORMAT(date, 'yyyyMMdd'))`.
- Replace PostgreSQL JSONB with NVARCHAR(MAX) JSON payload if needed.
