# Nextcord-Tortoise

This is a library to help developers integrate the [Tortoise ORM database library](https://github.com/tortoise/tortoise-orm) 
with their Nextcord bot. It heavily integrates with and relies on the Nextcord's Cog system. It also provides integration 
with Tortoise ORM's migration tool, Aerich, to allow for easy database migrations.

## Adding to your bot

Before starting, you'll want to be familar with Nextcord's Bot class and how to use `load_extension()` to load cogs 
on your bot.

Check out [demo.py](https://github.com/pmdevita/nextcord-tortoise/blob/master/example/demo.py) for the full example. You just need to call `connect_tortoise()` during the `on_connect` event 
of your bot.

You will also need to add command line arguments to your bot for Aerich. Nextcord-Tortoise supplies 
[argparse](https://docs.python.org/3/library/argparse.html) support with `attach_argparse_group`. If Aerich 
arguments are given by the user, you then call `run_aerich()` instead of `bot.run()`

## Usage

Once set up, using nextcord-tortoise is easy. Create or edit models in your cogs and then

### Creating Models

Models should be created alongside your Cog in the same file as your `setup()` function or imported from another file 
into that file. For information on how to create models, consult the [Tortoise-ORM docs](https://tortoise-orm.readthedocs.io/).

### Aerich

After you have set up your models, you'll need to create database migrations and then upgrade your database. You'll 
want to look at how the [Aerich migrations tool](https://tortoise-orm.readthedocs.io/en/latest/migration.html?highlight=aerich#) 
works as well.

If you set up Aerich like the demo file, the commands will look like this.

```shell
# Intial setup of migrations
python demo.py --aerich init-db
python demo.py --aerich migrate
# Upgrade the database
python demo.py --aerich upgrade
# Migrate a specific cog. The app name is the same as your cog's name
python demo.py --aerich migrate --app Example
# Downgrade a specific cog. --delete will delete the migration file too
python demo.py --aerich downgrade --app Example --delete
```


#### Notable differences with normal Aerich

Nextcord-Tortoise changes a few parts of Aerich's functionality to improve functionality.

- `init-db` only generates migrations for Aerich's management table to prevent each Cog/App from sharing the same main 
migration file. You'll need to call `migrate` afterwards too.
  
- Database files are stored in a subdirectory per database type and below that in per-cog applications.

- `migrate` and `upgrade` automatically apply to all Cogs/Apps if no app is specified





