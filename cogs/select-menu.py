import disnake
from disnake.ext import commands


# Определяем класс "SelectGames", который наследуется от disnake.ui.Select.
class SelectGames(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label="Dota 2",
                value="1136750503661932546",
                emoji="<:check_mark8:1155134578789470208>"
            ),
            disnake.SelectOption(
                label="Valorant",
                value="1136750590710521897",
                emoji="<:check_mark8:1155134578789470208>"
            ),
            disnake.SelectOption(
                label="Genshin Impact",
                value="1136750667206242445",
                emoji="<:check_mark8:1155134578789470208>"
            )
        ]
        super().__init__(placeholder="Укажите игру", options=options, custom_id="games", min_values=0, max_values=3)

    # Создаем метод callback для обработки взаимодействия пользователя с меню выбора ролей.
    async def callback(self, interaction: disnake.MessageInteraction):
        # Отправляем ответ, чтобы показать, что бот обрабатывает взаимодействие.
        await interaction.response.defer()

        # Задаем множество всех возможных ролей для выбора.
        all_roles = {1136750503661932546, 1136750590710521897, 1136750667206242445}

        # Инициализируем списки для ролей, которые нужно добавить и убрать у пользователя.
        to_remove = []
        to_add = []

        # Проверяем, выбрал ли пользователь какие-либо роли.
        if not interaction.values:
            # Если пользователь не выбрал ролей, то убираем все роли из множества all_roles.
            for role_id in all_roles:
                role = interaction.guild.get_role(role_id)
                to_remove.append(role)

            # Убираем все роли у пользователя и указываем причину.
            await interaction.author.remove_roles(*to_remove, reason="Удаление ролей")

        else:
            # Если пользователь выбрал роли, то сравниваем их с множеством all_roles.
            chosen_roles = {int(value) for value in interaction.values}

            # Определяем роли, которые нужно убрать (не выбраны пользователем).
            ids_to_remove = all_roles - chosen_roles

            for role_id in ids_to_remove:
                role = interaction.guild.get_role(role_id)
                to_remove.append(role)

            # Определяем роли, которые нужно добавить (выбраны пользователем).
            for role_id in chosen_roles:
                role = interaction.guild.get_role(role_id)
                to_add.append(role)

            # Убираем ненужные роли и добавляем выбранные роли у пользователя, указываем причину.
            await interaction.author.remove_roles(*to_remove, reason="Удаление ролей")
            await interaction.author.add_roles(*to_add, reason="Добавление ролей")


# Определяем класс "SelectRoles", который является расширением (Cog) для бота.
class SelectRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    # Создаем команду "games", которая будет выводить сообщение с вложенным меню выбора ролей.
    # ВНИМАНИЕ: Тут нет проверки на то, является ли пользователь администратором сервера или просто создателем.
    # Сделайте самостоятельно проверку на администратора или создателя бота.
    # Подсказка: Можно использовать декоратор @has_permissions() или if ctx.author.id == ...
    @commands.command()
    async def games(self, ctx):
        view = disnake.ui.View(timeout=None)
        view.add_item(SelectGames())
        embed = disnake.Embed(color=0x2F3136)
        embed.set_author(name="Игровые роли:")
        embed.description = "В этом посте Вы можете выбрать свою роль, нажав на кнопку " \
                            "соответствующей роли в меню выбора.\n\n" \
                            "<:check_mark8:1155134578789470208> - Dota 2\n" \
                            "<:check_mark8:1155134578789470208> - Valorant\n" \
                            "<:check_mark8:1155134578789470208> - Genshin Impact"
        embed.set_image(url="https://i.imgur.com/QzB7q9J.png")
        await ctx.send(embed=embed, view=view)

    # Создаем слушателя события "on_ready", который добавляет персистентное меню выбора ролей.
    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistent_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(SelectGames())
        # Message ID сообщения, где будет меню, добавляется после отправки команды.
        # Нужно будет скопировать ID сообщения и вставить вместо "...", после выполнения данных действий
        # необходимо перезапустить бота.
        self.bot.add_view(view, message_id=1156315288791425136)


# Функция setup, которая добавляет класс GameRoles как Cog (команду-расширение) в бота.
def setup(bot):
    bot.add_cog(SelectRoles(bot))