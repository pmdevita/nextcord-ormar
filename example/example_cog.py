from nextcord.ext import commands
from datetime import datetime
from tortoise.models import Model
from tortoise import fields

# Define tortoise models here or import them from another file


class ExampleCounter(Model):
    id = fields.IntField(pk=True)
    user = fields.BigIntField()
    time = fields.DatetimeField()


class Example(commands.Cog):
    def __init__(self, nextcord):
        self.nextcord = nextcord

    @commands.command("example")
    def example(self, ctx: commands.Context, *args):
        new_example = await ExampleCounter.create(user=ctx.author.id, time=datetime.now())
        await ctx.send("Hello!")


def setup(bot):
    bot.add_cog(Example(bot))
