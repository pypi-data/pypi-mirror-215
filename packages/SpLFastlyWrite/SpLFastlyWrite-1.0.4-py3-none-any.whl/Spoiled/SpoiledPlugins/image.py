from PIL import Image, ImageDraw, ImageFont
import glob
import requests
import os
from Spoiled.Shannu.config import BACKGROUND_IMAGE_URL as BIU

def init_bg():
  g = requests.get(BIU)
  try:
    os.mkdir("Images")
  except:
    pass
  with open("Images/bg.jpg", "wb") as f:
    f.write(g.content)

def make_image(text, username):
  text = text.capitalize()
  username = 'by @' + username
  x = './Images/bg.jpg'
  f = './Fonts/font.ttf'
  im = glob.glob('./saved_images/*')
  if f'{text}.jpg' in im:
    return f'saved_images/{text}.jpg'
  i = Image.open(x)
  wi, he = i.size
  d = ImageDraw.Draw(i)
  font = ImageFont.truetype(f, 120)
  font1 = ImageFont.truetype(f, 60)
  w, h = d.textsize(text, font)
  new_w = (wi - w) / 2
  new_h = (he - h) / 2
  d.text((new_w, new_h), text, fill="black", font=font)
  d.text((5, 5), username, fill="black", font=font1)
  i.save(f'saved_images/{text}.jpg')
  return f'saved_images/{text}.jpg'
