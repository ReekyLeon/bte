import disnake
from disnake.ext import commands

class ButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @disnake.ui.button(label="✅ Верификация", style=disnake.ButtonStyle.green, custom_id="button1")
    async def button1(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        
        role = interaction.guild.get_role(1154406425691426958)
       
        if role in interaction.author.roles:
            await interaction.author.remove_roles(role)
        else:
            await interaction.author.add_roles(role)
            await interaction.response.send_message("Вы успешно прошли верификацию.\n " \
                                                    "Приятного общения и успешной торговли", ephemeral=True)
       
        await interaction.response.defer()

class ButtonsRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    @commands.command()
    async def buttons(self, ctx):
        view = ButtonView()

       
        role = ctx.guild.get_role(1154406425691426958)

        embed = disnake.Embed(color=disnake.Colour.from_rgb(0,255,0))
        embed.description = f"Чтобы общаться и видеть все чаты, вам нужно пройти верификацию.\n " \
                            "Для того чтобы пройти верификацию, нажмите кнопку снизу.\n "
        embed.set_image(url="https://media.discordapp.net/attachments/1136262252685689003/1156325978092621865/Media_230926_232548.gif?ex=65148ffc&is=65133e7c&hm=a41da4785c4a588364fbb52fd7177952e3f5352b7416f4f5de2b118ff17d8dc9&=")
        await ctx.send(embed=embed, view=view)
  
    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistent_views_added:
            return

        
        self.bot.add_view(ButtonView(), message_id=1156327288644845568)

def setup(bot):
    bot.add_cog(ButtonsRole(bot))