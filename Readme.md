# Nextcord-Tortoise

This is a library to help developers integrate the [Tortoise ORM database library](https://github.com/tortoise/tortoise-orm) 
with their Nextcord bot. It's designed to be integrated with a bot that is using Nextcord's cog system. It also 
provides integration with Tortoise ORM's migration tool, Aerich, to allow for easy database migrations.

This library is currently in alpha, there may be breaking changes as the library is polished up. For now, if you 
would like to install it, run `pip install git+https://github.com/pmdevita/nextcord-tortoise`.

## Usage

Before starting, you'll want to be familiar with Nextcord's Bot class and how to use `load_extension()` to load cogs 
on your bot. You will also want to take a look at [Tortoise-ORM's docs](https://tortoise-orm.readthedocs.io/) and 
at least be familiar with configuring Tortoise and how to create models.

There's a small demo project in the example folder, take a look at
[demo.py](https://github.com/pmdevita/nextcord-tortoise/blob/master/example/demo.py).

Instead of subclassing or initializing `nextcord.ext.commands.Bot`, you'll need to use `nextcord_tortoise.Bot`. 
You'll also need to pass it your Tortoise configuration settings with the `tortoise_config` argument. An example 
Tortoise config can be seen [here](https://tortoise-orm.readthedocs.io/en/latest/setup.html#tortoise.Tortoise.init). 
Note that the `apps` section will be auto-generated from your cogs so you probably won't need to add anything 
yourself here.

Finally, you will need to add command line arguments to your main bot script for Aerich, Tortoise's database migration 
tool. Nextcord-Tortoise comes with an [argparse](https://docs.python.org/3/library/argparse.html) group you can attach
to a pre-existing (or new) argparse parser with `attach_argparse_group()`. Then, if Aerich arguments are given by the 
user, call `run_aerich()` instead of `bot.run()` to run the Aerich command.

### Creating and Adding Models

Models can be created alongside your Cog in the same file or in a separate file such as `models.py`.

To register your models, pass a string, or a list of strings of module import paths to `bot.add_cog()` as the 
`models` argument.

Examples:

```python
bot.add_cog(Example(bot), models=".")  # Imports models from the same file as the cog
bot.add_cog(Example(bot), models=".models")  # Imports models from the file "models.py" located in the same package as this cog
bot.add_cog(Example(bot), models=[".", "general.models"])  # Imports models from the same file as the cog and from another package called "general.models"
```


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

Nextcord-Tortoise's Aerich works a little differently than Tortoise's.

- `init-db` only generates migrations for Aerich's management table to prevent each Cog/App from sharing the same main 
migration file. You'll need to call `migrate` afterwards too.
  
- Database files are stored in a subdirectory per database type and below that in per-cog applications.

- `migrate` and `upgrade` automatically apply to all Cogs/Apps if no app is specified

- Each application is named after it's respective cog's name.





