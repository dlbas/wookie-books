# wookie-books

A bookstore REST API for the Wookies from Kashyyyk.

## How to run

Just run
```docker-compose up``` at the root of the repository to boot everything up. Then head to
http://localhost:8000/docs/ to see the OpenAPI interactive docs.

![OpenAPI interactive docs view](assets/interactive_docs.png?raw=true)

There will be some demo users: `luke`, `anakin` and `dartvaider`. Each user has no password set. The password will
be set the first time you log in with that username.

![Auth view](assets/authorize.png?raw=true)

For production usage you will probably need to tweak some environment variables.

> :warning: **It is highly recommended to change default values for the production usage!**

| Environment Variable       |                        Default                        |                                                  Description |
|:---------------------------|:-----------------------------------------------------:|-------------------------------------------------------------:|
| `POSTGRES_USER`            |                      `postgres`                       |                                A user login for the database |
| `POSTGRES_PASSWORD`        |                      `changeme`                       |                                            A user's password |
| `POSTGRES_DB`              |                         `app`                         | Database to be automatically created upon db container start |
| `PG_DATA`                  |                   `/data/postgres`                    |                                A directory for postgres data |
| `PG_DATA`                  |                   `/data/postgres`                    |                                A directory for postgres data |
| `DATABASE_URL`             | `postgresql+asyncpg://postgres:changeme@postgres/app` |                Database connection string for the python app |
| `TOKEN_SECRET_KEY`         |                     `replace me`                      |                                       Application secret key |
| `TOKEN_EXPIRES_IN_MINUTES` |                         `60`                          |                                                JWT token TTL |


## Development

1. Clone the repository: ```git clone https://github.com/dlbas/wookie-books.git```
2. Install dependencies: ```poetry install```

### Running tests
Just run ```pytest``` inside the repository's root.

