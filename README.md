# ERP Shop

A small ERP backend for a retail shop: products and stock, with more modules
added through pull requests.

Built with FastAPI and SQLite.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for the API.

| Variable | Default | Meaning |
|---|---|---|
| `ERP_DB_PATH` | `erp.db` | SQLite database file |
| `ERP_API_KEY` | `dev-key` | Key staff send as `X-API-Key` on write endpoints |

## Test

```bash
pytest
```

## Conventions

- Money is stored and computed in integer cents (`price_cents`), never floats.
- Every endpoint that changes data requires the API key (`Depends(require_api_key)`).
- SQL always uses `?` parameters, never string formatting.
- Stock changes must be atomic: a single conditional `UPDATE`, not read-then-write.
