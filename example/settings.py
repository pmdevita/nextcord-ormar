# Similar to regular Tortoise-ORM, you'll want to define a configuration dictionary for Tortoise somewhere.
# We aren't supplying an apps key because nextcord-tortoise will be building that from our cogs
TORTOISE_CONFIG = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    }
}
