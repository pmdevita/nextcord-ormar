import ormar
from nextcord.ext import commands
from nextcord_ormar import OrmarApp, AppModel
from datetime import datetime

# Define tortoise models here or import them from another file

ModelMeta = OrmarApp.create_app("example")


class ExampleCounter(AppModel):
    class Meta(ModelMeta):
        pass

    id = ormar.Integer(primary_key=True)
    user = ormar.BigInteger()
    time = ormar.DateTime()
    # another_column = ormar.Text()


class Example(commands.Cog):
    def __init__(self, nextcord):
        self.nextcord = nextcord

    @commands.command("example")
    async def example(self, ctx: commands.Context, *args):
        new_example = await ExampleCounter.objects.create(user=ctx.author.id, time=datetime.now())
        await ctx.send("Hello!")


def setup(bot):
    # bot.add_cog(Example(bot), models=".")
    bot.add_cog(Example(bot))
