<div align = "center">

# Project Data | Extension of Clerk Authentication

[![Python](https://img.shields.io/badge/Python-%203.11%2B-003B57?style=plastic&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-%20async-003B57?style=plastic&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%20multi--schema-003B57?style=plastic&logo=postgresql)](https://www.postgresql.org/)
[![Clerk](https://img.shields.io/badge/Clerk-%20webhooks-003B57?style=plastic&logo=clerk)](https://clerk.com/docs/webhooks/overview)

</div>

<div align = "justify">

The repository extend's **`Clerk Authentication`** with project basis data using `FastAPI` based webhooks (delivered and signed
via `Svix`) and creates a normalized user identity into a multi-schema PostgreSQL database - that anchors on `User ID` for
every other sub-project related schema (`demography`, `profile`, ...) through cross-schema foreign key.

## 📜 Getting Started

Requires Python v3.12+ a reachable PostgreSQL instance and an webhook endpoints from Clerk Authentication that asynchronously
setup the module and do a testing.

```shell
$ python -m pip install -e ".[dev]"
$ cp .env.example .env   # Setup Environment Variables
```

Set the two required environment variables in `.env` and install [`ngrok`](https://ngrok.com/download) to test the data in
`localhost` environment.

  * `DATABASE_URL` - Asynchronous DSN for PostgreSQL Database
  * `CLERK_WEBHOOK_SIGNING_SECRET` - Secret Key from Clerk Dashboard for `webhook` Endpoint

The `ngrok` allows localhost to be hosted and allows public access for webhook to be rechable. Once *migrations* are applied,
start the server as:

```shell
$ alembic upgrade head
$ uvicorn app.main:app --reload
```

### 🖥️ Monitoring Endpoints

The following endpoints are inbuilt to check the status and post data into a PostgreSQL database endpoint using SQL Alchemy
ORM as:

  * `GET /health` - liveness probe.
  * `GET /health/ready` - readiness probe (checks database connectivity).
  * `POST /webhooks/clerk` - the Clerk/Svix ingress.
  * `GET /users/{clerk_id}` - read the identity row.
  * `GET|PATCH /users/{clerk_id}/demography` - read or enrich demographic attributes.
  * `GET|PATCH /users/{clerk_id}/profile` - read or enrich personal profile.

</div>
