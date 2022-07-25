from nextcord.ext import commands
from nextcord_ormar import OrmarApp, AppModel
import ormar

ModelMeta = OrmarApp.create_app("another")


class AnotherExample(AppModel):
    class Meta(ModelMeta):
        pass

    id: int = ormar.BigInteger(primary_key=True, autoincrement=False)
    last_message: str = ormar.Text()


class Another(commands.Cog):
    def __init__(self, nextcord):
        self.nextcord = nextcord

    @commands.command("another")
    async def example(self, ctx: commands.Context, *args):
        new_example = await AnotherExample.objects.get_or_create(user=ctx.author.id)
        await new_example.update(last_message=" ".join(*args))
        await ctx.send("Hello!")


def setup(bot):
    bot.add_cog(Another(bot))
