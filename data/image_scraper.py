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
import time
import os


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
    if re.match(r'(?=(.*discordapp\.com.*))(?=.*\.png.*|.*\.jpg.*|.*\.jpeg.*)(?=(?!.*levelUp.*))(?=(?!.*levelup.*))(?=(?!.*avatars.*))(?=(?!.*profile.*))(?=(?!.*rank.*))', string, flags=re.I) == None:
        return False
    else:
        return True
        
def get_url(string):
    
    m = re.match(r'(?=(.*discordapp\.com.*))(?=.*\.png.*|.*\.jpg.*|.*\.jpeg.*)', string, flags = re.I)
    
    return m.group(1)

f = open("MENA.txt", "r", encoding="utf8")
mena = f.readlines()
f.close()

images = []
seen = set()
user = ''
current_url = ''
captions = []
image_user = 'e'
attachment = False
counter = 0
current_path = 'D:/Repos/mena-image-captioning/data/train_images'
for c in np.arange(1,len(mena)-3):
    if is_user(mena[c]):
        user = get_user(mena[c])
        continue
    if is_url(mena[c]) & (re.search(r'Attachments', mena[c-1]) != None):
        current_url = get_url(mena[c])
        if current_url not in seen:
            if (not is_user(mena[c-3])) & (mena[c-3] != '\n') & np.all(np.array([ord(ch) for ch in mena[c-3]]) < 255):
                seen.add(current_url)
                # Make a dictionary
                images.append(current_url + '\n')
                r = requests.get(current_url)
                name_of_file = '%id.jpg' % (counter)
                
                completeName = os.path.join(current_path, name_of_file)
                with open(completeName, 'wb') as outfile:
                    outfile.write(r.content)
                time.sleep(1)
                counter += 1
                image_user = user
                caption = {}
                caption['caption'] = mena[c-3] + '\n'
                caption['image_path'] = completeName
                captions.append(caption)
                
            else:
                pass
    else:
        pass
    
f = open("mena_images.txt","w", encoding="utf8")
f.writelines(images)
f.close()

f = open("mena_captions.txt","w", encoding="utf8")
captions = [caption.lower() for caption in captions]
f.writelines(captions)
f.close()

# Example image
response = requests.get(np.random.choice(images)[:-1])
img = Image.open(BytesIO(response.content))

# Download image


url = np.random.choice(images)[:-1]
