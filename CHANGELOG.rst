==========
Change Log
==========

- :release:`0.3.2 <2022/7/26>`
- :bug:`-` Fix MySQL/PostgreSQL connections not intializing
- :feature:`-` Don't generate empty migrations without --empty
- :bug:`-` Fix --empty and --message commands not working

- :release:`0.3.1 <2022/7/25>`
- :feature:`-` Publish to PyPI
- :bug:`-` Remove debug printing
- :bug:`-` Fix cogs deleting each other when migrating
- :feature:`-` Refactor :py:class:`nextcord_ormar.OrmarManager` to be more standalone friendly.

- :release:`0.3.0 <2022/7/24>`
- :feature:`-` New migration tool, NXAlembic
- :feature:`-` Rewrite from using Tortoise-ORM to Ormar

- :release:`0.2.4 <2022/7/15>`
- :bug:`-` Better shutdown order with Nextcord 2.0.0+
- :support:`-` Nextcord 2.0.0 is now required

- :release:`0.2.3 <2022/3/23>`
- :bug:`-` Missing async/await in close()

- :release:`0.2.2 <2022/3/23>`
- :feature:`-` Migrated to Poetry for packaging
- :bug:`-` Close Tortoise connections when Bot closes

- :release:`0.2.1 <2021/12/04>`
- :bug:`-` Fix another issue where apps might leak into each other's migrations

- :release:`0.2 <2021/12/04>`
- :bug:`-` Fix migration commands duplicating into multiple app's migrations

- :release:`0.1 <2021/11/30>`
- :feature:`-` Restructured Tortoise and model initializing around the Tortoise Bot subclass. Model files are now explicitly required in the ``add_cog()`` command ("Explicit is better than implicit.").
- :bug:`3` Avoid reinit-ing every time on_connection is called
- :bug:`1` Fix warnings with cogs that don't have Tortoise models