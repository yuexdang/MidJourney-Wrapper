import os

#strings

DAVINCI_TOKEN = os.environ.get('DAVINCI_TOKEN')

SERVER_ID = os.environ.get('SERVER_ID')

SALAI_TOKEN = os.environ.get('SALAI_TOKEN')

CHANNEL_ID = os.environ.get('CHANNEL_ID')

#boolean
USE_MESSAGED_CHANNEL = True if(os.environ.get('CHANNEL_SIGN')=="True") else False

#don't edit the following variable
HAS_RUN = False

MID_JOURNEY_ID = "936929561302675456"  #midjourney bot id
targetID       = ""
targetHash     = ""
