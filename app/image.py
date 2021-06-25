import flickrapi
import random
import requests
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO

def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        # split the line by spaces to get words
        words = text.split(' ')  
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''        
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word,
            # add the line to the lines array
            lines.append(line)    
    return lines
 

api_key = '885f801ff9e12134faa4b5a6fbdd27bb'
api_secret = 'fb4d2caea0bd362d'
photos = []
flickr=flickrapi.FlickrAPI(api_key,api_secret,cache=True)

for photo in flickr.walk_set('72157639585298964', extras ='url_o'):
    x = photo.get('url_o')
    if x != 'None': 
        photos.append(x)

photo_select = random.choice(photos)
print(photo_select)

im = Image.open("D:/Gatsby/archives/static/backgrounds/25.jpg")
logo = Image.open(requests.get("https://srishtiarchive.com/white-logo.png", stream=True).raw)
logo = logo.resize((round(logo.size[0]*0.15), round(logo.size[1]*0.15)))
converter = ImageEnhance.Color(im)
im =  converter.enhance(4.0)
print("Photo Fetched! Cropping...")
width, height = im.size   # Get dimensions

aspect = width / float(height)

ideal_width = 800
ideal_height = 600

ideal_aspect = ideal_width / float(ideal_height)

if aspect > ideal_aspect:
    # Then crop the left and right edges:
    new_width = int(ideal_aspect * height)
    offset = (width - new_width) / 2
    resize = (offset, 0, width - offset, height)
else:
    # ... crop the top and bottom:
    new_height = int(width / ideal_aspect)
    offset = (height - new_height) / 2
    resize = (0, offset, width, height - offset)

im = im.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)
n_width, n_height = im.size   # Get dimensions

black = Image.new('RGB',im.size,(0,0,0))
mask = Image.new('RGBA',im.size,(0,0,0,200))


im = Image.composite(im,black,mask).convert('RGB')
im.paste(logo, (100,100), logo)
req = requests.get("https://github.com/thedivtagguy/files/raw/main/Inter-UI-Black.otf")
font = ImageFont.truetype(BytesIO(req.content), 85)
text = "A bit of text to tell you "
lines = text_wrap(text, font, 600)
y_text = 200
draw = ImageDraw.Draw(im)

for line in lines:
    width, height = font.getsize(line)
    draw.text(((900 - n_width), y_text),line, font=font, fill="#ffffff")
    y_text += height

im.save("og.png")