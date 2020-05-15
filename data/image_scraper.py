# Initialize a list
# Go through the file line by line
# if it's a message: check if it's an url
# if it's an url: check if it contains discordapp.com and ends with .jpg/png/etc.
# if it contains discordapp.com, make a new dictionary, set its url and append to list
# Also store the message two lines above it c-3 (if any) in the dictionary as its caption value
# Also check the user at c+2
# if that user is the same as current user, get message at c+3 and store it as well in the caption value


import re
import numpy as np
from PIL import Image
import requests
from io import BytesIO


def is_user(string):
    if re.match(r'^(\[\d\d-.*\] .*#.*)$', string) != None:
        return True
    else:
        return False
    
def get_user(string):
    m = re.search(r'\] (.+?)#', string)
    if m:
        user = m.group(1)
    else:
        raise Exception('Not a user')
    
    return user

def is_url(string):
    if re.match(r'(?=(.*discordapp\.com.*))(?=.*\.png.*|.*\.jpg.*|.*\.jpeg.*)(?=(?!levelUp))', string, flags=re.I) == None:
        return False
    else:
        return True
        
def get_url(string):
    
    m = re.match(r'(?=(.*discordapp\.com.*))(?=.*\.png.*|.*\.jpg.*|.*\.jpeg.*)', string, flags = re.I)
    
    return m.group(1)

f = open("blogspot.txt", "r", encoding="utf8")
mena = f.readlines()
f.close()

images = []
seen = set()
user = ''
current_url = ''
captions = []
image_user = 'e'
image_found = False
caption_found = False
for c in np.arange(0,len(mena)-3):
    if is_user(mena[c]):
        user = get_user(mena[c])
        continue
    if (image_found) & (not caption_found) & (image_user == user) & (mena[c] != '\n'):
        captions.append(mena[c] + '\n')
        image_found = False
        caption_found = True
    if is_url(mena[c]):
        current_url = get_url(mena[c])
        if current_url not in seen:
            seen.add(current_url)
            # Make a dictionary
            images.append(current_url + '\n')
            image_found = True
            image_user = user
            if not is_user(mena[c-3]):
                captions.append(mena[c-3] + '\n')
                caption_found = True
            else:
                caption_found = False
    else:
        pass
    
f = open("blogspot_images.txt","w", encoding="utf8")
f.writelines(images)
f.close()

f = open("blogspot_captions.txt","w", encoding="utf8")
f.writelines(captions)
f.close()

# Example image
response = requests.get(np.random.choice(images)[:-1])
img = Image.open(BytesIO(response.content))

# Download image


url = np.random.choice(images)[:-1]
r = requests.get(url)
with open('random.jpg', 'wb') as outfile:
    outfile.write(r.content)