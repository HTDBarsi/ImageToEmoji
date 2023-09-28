from PIL import Image
import discord
import os

imgsize = 256

if not os.path.isdir("./out"): os.mkdir("./out")
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as '+self.user.name)
        print('------')

    async def on_message(self,message : discord.Message):
        if len(message.attachments) != 0:
            await message.attachments[0].save("pic.png")
            im = Image.open("pic.png")
            countx = im.size[0] // imgsize
            if (im.size[0] % imgsize) != 0:
                countx += 1
            county = im.size[1] // imgsize
            if (im.size[1] % imgsize) != 0:
                county += 1
            print(countx,county)
            guild = message.guild
            returnmsg = ""
            for u in range(county):
                for i in range(countx):
                    r = (imgsize * i, imgsize * u, imgsize * (i + 1), imgsize * (u + 1))
                    cropped_image_path = f"out/{i}_{u}_out.png"
                    im.crop(r).save(cropped_image_path)
                    with open(cropped_image_path, "rb") as image_file:
                        image_data = image_file.read()
                        res = await guild.create_custom_emoji(name=f"{i}_{u}_out", image=image_data, reason=None)
                    print(r)
                    returnmsg = returnmsg+f"<:{i}_{u}_out:"+str(res.id)+">"
                returnmsg = returnmsg+"\n"

            os.remove("pic.png")
            await message.channel.send(returnmsg)
            return await message.add_reaction("😎")

client = MyClient(intents=discord.Intents.default())
client.run("token here!")
