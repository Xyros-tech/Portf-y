import discord
from discord.ext import commands
from discord import ui, ButtonStyle, TextStyle
from config import TOKEN
from logic import DB_Manager, DATABASE  # logic.py'den DB_Manager ve DATABASE'i import ediyoruz

# Veritabanı yöneticisini oluştur
db_manager = DB_Manager(DATABASE)

# Modal pencere tanımlama
class ProjectModal(ui.Modal, title='Yeni Proje Ekle'):
    # Modal pencerede metin alanları tanımlama
    project_name = ui.TextInput(label='Proje Adı', placeholder='Proje adını girin...')
    project_url = ui.TextInput(label='Proje Linki', placeholder='Proje linkini girin...', required=False)
    status_name = ui.TextInput(label='Geliştirme Aşaması', placeholder='Geliştirme aşamasını seçin...')

    async def on_submit(self, interaction: discord.Interaction):
        # Geliştirme aşamasının ID'sini al
        status_id = db_manager.get_status_id(self.status_name.value)
        if not status_id:
            await interaction.response.send_message("Geçersiz geliştirme aşaması!", ephemeral=True)
            return

        # Projeyi veritabanına ekle
        db_manager.insert_project([(interaction.user.id, self.project_name.value, self.project_url.value, status_id)])
        await interaction.response.send_message(f"Proje başarıyla eklendi: {self.project_name.value}", ephemeral=True)

# Buton tanımlama
class ProjectButton(ui.Button):
    def __init__(self, label="Proje Ekle", style=ButtonStyle.blurple, row=0):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, interaction: discord.Interaction):
        # Modal pencereyi açma
        await interaction.response.send_modal(ProjectModal())

# Buton içeren bir pencere (görünüm) nesnesi tanımlama
class ProjectView(ui.View):
    def __init__(self):
        super().__init__()
        # Görünüme bir buton ekleme
        self.add_item(ProjectButton(label="Proje Ekle"))

# Bot yapılandırması
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Bot hazır olduğunda gönderilen bir olay
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı')

# Butonu gösteren bir komut
@bot.command()
async def test(ctx):
    # Bir buton içeren görünüm ile mesaj gönderme
    await ctx.send("Yeni proje eklemek için aşağıdaki butona tıklayın:", view=ProjectView())

# Botu çalıştır
bot.run(TOKEN)