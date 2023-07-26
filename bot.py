import discord
from image_manipulator import ImageManipulator
from discord.ext import commands
import os
import shutil
import secret_key

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)
imgM = ImageManipulator()
channel_id = secret_key.get_channel_id()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(channel_id)
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Making your images look beautiful!"))
    await channel.send(f"{client.user} Online!")

    
@client.command()
async def image(ctx, *args):
    if(not ctx.message.attachments):
        return await ctx.send('No image attached!')
    elif(len(args) == 0):
        return await ctx.send('No parameters specified!')

    folder_name = str(ctx.message.author.id)
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.makedirs(folder_name)

    await ctx.message.attachments[0].save(folder_name + "/img.png")
    
    filter_stack = await imgM.process_image(folder_name, *args)
    await send_edited_image(ctx, filter_stack, folder_name)
    await ctx.message.delete()


async def send_edited_image(ctx, filter_stack, folder_name):
    folder_directory = folder_name + "/img2.png"
    file = discord.File(fp=folder_directory)
    embed = discord.Embed(title="Converted Image", color=0x1abc9c)
    embed.set_image(url="attachment://img2.png")
    embed.add_field(name="Filter Stack", value=filter_stack, inline=False)
    embed.add_field(name="Command", value=ctx.message.content, inline=False)
    embed.add_field(name="Requested by", value=ctx.message.author.mention, inline=False)
    await ctx.send(file = file, embed=embed)

    
@client.command()
async def commands(ctx, *args):
    embed = discord.Embed(title="Commands", color=0x56f061)
    embed.add_field(name="Main command", value=".image {parameters}", inline=False)
    embed.add_field(name="Greyscale Converter", value="grey", inline=False)
    embed.add_field(name="Adding Blur", value="blur", inline=False)
    embed.add_field(name="Resizing Image", value="resize=100x100 or resize=40 (where 40 is the percent to be scaled by.)", inline=False)
    embed.add_field(name="Toonify", value="toonify", inline=False)
    embed.add_field(name="Oil Painting", value="oilpainting", inline=False)
    embed.add_field(name="Invert", value="invert", inline=False)
    embed.add_field(name="Noise", value="noise", inline=False)
    embed.add_field(name="Memeify", value="memeify=me_when_the (where words are seperated by underscores).", inline=False)
    embed.add_field(name="Pixelate", value="pixelate", inline=False)
    embed.add_field(name="Stacking commands", value="**.image grey blur resize=30** \n\n This will greyscale the image, blur it and then resize it to 30%. Feel free to add as little or as many paramters as you'd like!", inline=False)
    await ctx.send(embed=embed)


client.run(secret_key.get_key())
