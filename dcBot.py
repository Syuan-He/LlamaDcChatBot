import os
import asyncio

import dotenv
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")
    await bot.change_presence(activity=discord.Game(name="LaMaMa"))

@bot.command()
async def synccommand(ctx: commands.Context):
    slash = await bot.tree.sync()
    await ctx.send(f"同步 {len(slash)} 個斜線指令")

# 載入指令程式檔案
@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx: commands.Context , extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# 卸載指令檔案
@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx: commands.Context, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

# 重新載入程式檔案
@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx: commands.Context, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    dotenv.load_dotenv()
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DC_TOKEN"))

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())