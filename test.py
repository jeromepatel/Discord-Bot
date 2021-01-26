
# download image from this person doesnt exist website
# import requests
# def download(fileName):
#     f = open(fileName,'wb')
#     f.write(requests.get('https://thispersondoesnotexist.com/image', headers={'User-Agent': 'My User Agent 1.0'}).content)
#     f.close()
# download('a.jpg')

# import io
# import aiohttp

# async with aiohttp.ClientSession() as session:
#     async with session.get('https://thispersondoesnotexist.com/image') as resp:
#         if resp.status != 200:
#             return await channel.send('Could not download file...')
#         data = io.BytesIO(await resp.read())
#         await channel.send(file=discord.File(data, 'cool_image.png'))

import requests
r = requests.get('https://www.reddit.com/r/EizaGonzalez/random.json',headers = {'User-agent': 'test bot 0.1'})
print(r.json())