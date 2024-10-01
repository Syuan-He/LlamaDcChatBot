import enum

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

import torch
from transformers import pipeline

MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"

class DeleteWait(enum.IntEnum):
    message = 0
    history = 1
    system = 2

class LlamaChat(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        print("Fliter Cog Loaded")
        self.bot = bot
        self.pipe = pipeline(
            "text-generation",
            model=MODEL_ID,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.messages = []
        self.delete_wait = [5, 10, 3]

    @commands.hybrid_command()
    async def delete_history(self, ctx: commands.Context):
        del self.messages
        self.messages = []
        await ctx.send("clear message history was done", delete_after=self.delete_wait[DeleteWait.system])

    @commands.hybrid_command()
    async def show_history(self, ctx: commands.Context):
        history_messages_context = [f'{msg["role"]}: {msg["content"]}' for msg in self.messages]
        await ctx.send('\n'.join(history_messages_context) if len(history_messages_context) > 0 else "history is empty", delete_after=self.delete_wait[DeleteWait.history])
        
    @commands.hybrid_command()
    async def set_delete_wait(self, ctx: commands.Context, msg: DeleteWait, wait_time: int):
        self.delete_wait[msg] = wait_time
        await ctx.send(f"set {msg.name} as {wait_time}", delete_after=self.delete_wait[DeleteWait.system])
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        self.messages.append({"role": "user", "content": message.content})
        output=[]
        async with message.channel.typing():
            output = await self.__generate_answer__()
        await message.delete()
        output_text = output[0]["generated_text"][-1]
        await message.channel.send(output_text["content"], delete_after=self.delete_wait[DeleteWait.message])
        self.messages.append(output_text)
    
    async def __generate_answer__(self):
        return self.pipe(self.messages, max_new_tokens=256)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Filter(bot))
