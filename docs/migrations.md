# Migrations

Ormar's query engine is backed by SQLAlchemy, so it also uses Alembic. Alembic is fully compatible with 
Nextcord-Ormar, but it's recommended to use NXAlembic, which is a wrapper around Alembic preconfigured to work with 
your bot.

## FAQ

These weren't necessarily asked to me, but they were questions I had during development.

### Why can't I create database migrations without a database (ala Django?)

[Here's a whole write up from SQLAlchemy's lead, Mike Bayer](https://github.com/sqlalchemy/alembic/issues/792#issuecomment-774556013).
In short, Alembic lacks the funding and manpower to implement the feature. Even Django had to put a Kickstarter 
together in order to fund one of their developers to work on it.

