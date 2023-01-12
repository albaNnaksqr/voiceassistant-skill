import sys

sys.path.append('/home/ai-user/mycroft-core/skills/voiceassistant-skill')

from util import callAPI, encode_image_from_file
from getObjLabel import getObjectsThenLabel, getLabel

image_file = './1.jpeg'
image_base64 = encode_image_from_file(image_file)
response = getLabel(image_base64)
#response = getObjectsThenLabel(image_file)
print(response)
