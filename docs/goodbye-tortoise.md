# Goodbye Tortoise ORM

When I initially started looking for async-compatible ORMs, my search led me to Tortoise ORM. It promised a 
Django-like ORM experience, which was enough for me to be sold on it. However, using the library in practice 
reveals several core issues with the library and the direction of its maintenance. And really, a lot of Python ORMs 
are inspired by the Django ORM nowadays.

## Issues with the Tortoise ORM

Tortoise ORM for the most part has been a decent experience. It tends to operate just like Django. However, there are 
many "gotchas" that can ruin the experience.

- Number types differ between backends. The `IntField` has two different sizes compared between SQLite and MySQL, you
actually should be using `BigIntField` if you have numbers that large. Django takes care of this for you, but 
Tortoise waits until you switch databases to spring this on you.
- `IntField` always auto increments. You cannot have a non-autoincrementing int field. This can cause serious problems 
if you need to store particular values to this field.

Again, Tortoise ORM isn't the worst but these surprises can happen quite often. However, by far the worst part of 
working with Tortoise is Aerich

## Issues with Aerich

Aerich is not only unfinished, it is seriously flawed, to a point where this library had to write an entire new 
front-end and create multiple hacks to make it usable.

- Aerich does not support per-app migrations. All apps are combined together into one migration file when you migrate.
- Aerich outputs SQL files for migrations. This makes migrations non-portable between backends.
- Aerich doesn't order table creations correctly. If you are creating tables with foreign keys, you can bet you are 
going to need to edit that migration yourself to make it actually execute.
- Aerich doesn't order table deletion commands correctly. Again, foreign keys are not considered at all.
- Aerich has second-class support for SQLite and some changes will simply fail, leaving you high and dry. Contrast this 
to Django where there is little difference in experience between database backends.
- Aerich can only create one new migration (per app in Nextcord-Tortoise) at a time. If you make a migration, then make 
more changes, making migrations again will delete and remake the current migration file.

I originally also complained that Aerich could not create migrations without comparing against a live database, while 
Django could do it just from the migration files. However, this feature is highly uncommon due to how difficult 
it is to develop such a feature, so they get a pass for it.

## Issues with project direction

As mentioned above with Aerich, many of these decisions are core strategies taken by the library developers. If you 
want to fix them, you might as well write your own migration library. Aerich doesn't see much development to begin 
with, and with no roadmap, we can only assume these decisions were intentional. Tortoise-ORM as well, while in a 
better state than Aerich, still makes troubling short-sighted decisions. At this point, it is simply not worth the 
pain of using this library, and it would be best to move to something else.

## Going forward

The solution will be to choose a different ORM library to pair with Nextcord. At the moment, the decision will likely 
be [ormar](https://github.com/collerek/ormar), which has a full-featured Django-like API, and is backed 
by the highly mature SQLAlchemy library. This will then support SQLAlchemy's Alembic tool for migrations. This will 
likely still require some new front-end work as Alembic doesn't support per-application migrations out of the box, 
but the underlying tool should be solid enough to produce good migrations when fed properly.


