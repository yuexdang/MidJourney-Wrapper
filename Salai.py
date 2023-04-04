import Globals
import requests

def PassPromptToSelfBot(prompt : str):
    payload ={"type":2,"application_id":Globals.MID_JOURNEY_ID,"guild_id":Globals.SERVER_ID,
              "channel_id":Globals.CHANNEL_ID,"session_id":"2fb980f65e5c9a77c96ca01f2c242cf6",
              "data":{"version":"1077969938624553050","id":"938956540159881230","name":"imagine","type":1,"options":[{"type":3,"name":"prompt","value":prompt}],
                      "application_command":{"id":"938956540159881230",
                                             "application_id":Globals.MID_JOURNEY_ID,
                                             "version":"1077969938624553050",
                                             "default_permission":True,
                                             "default_member_permissions":None,
                                             "type":1,"nsfw":False,"name":"imagine","description":"Create images with Midjourney",
                                             "dm_permission":True,
                                             "options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True}]},
              "attachments":[]}}
    
    {"type":2,"application_id":Globals.MID_JOURNEY_ID,
     "guild_id":"1091688748728733777","channel_id":"1091688749877969052","session_id":"a1dd523030181a4c27005dd743b50a28",
     "data":{"version":"1077969938624553050","id":"938956540159881230","name":"imagine","type":1,"options":[{"type":3,"name":"prompt","value":"girl"}],"application_command":{"id":"938956540159881230","application_id":Globals.MID_JOURNEY_ID,"version":"1077969938624553050","default_permission":True,"default_member_permissions":None,"type":1,"nsfw":False,"name":"imagine","description":"Create images with Midjourney","dm_permission":True,"options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True}]},"attachments":[]},"nonce":"1092673769505292288"}

    header = {
        'authorization' : Globals.SALAI_TOKEN
    }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header)
    return response

def Upscale(index : int, messageId : str, messageHash : str):
    payload = {"type":3,
    "guild_id":Globals.SERVER_ID,
    "channel_id":Globals.CHANNEL_ID,
    "message_flags":0,
    "message_id": messageId,
    "application_id":Globals.MID_JOURNEY_ID,
    "session_id":"45bc04dd4da37141a5f73dfbfaf5bdcf",
    "data":{"component_type":2,
            "custom_id":"MJ::JOB::upsample::{}::{}".format(index, messageHash)}
        }  
    header = {
        'authorization' : Globals.SALAI_TOKEN
    }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header)
    return response




def MaxUpscale(messageId : str, messageHash : str):
    payload = {"type":3,
            "guild_id":Globals.SERVER_ID,
            "channel_id":Globals.CHANNEL_ID,
               "message_flags":0,
               "message_id": messageId,
               "application_id":Globals.MID_JOURNEY_ID,
               "session_id":"1f3dbdf09efdf93d81a3a6420882c92c","data": 
         {"component_type":2,"custom_id":"MJ::JOB::upsample_max::1::{}::SOLO".format(messageHash)}}
    header = {
          'authorization' : Globals.SALAI_TOKEN
      }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header)
    return response


def Variation(index : int,messageId : str, messageHash : str):
    payload = {"type":3, "guild_id":Globals.SERVER_ID,
                "channel_id": Globals.CHANNEL_ID,
                "message_flags":0,
                "message_id": messageId,
                "application_id": Globals.MID_JOURNEY_ID,
                "session_id":"1f3dbdf09efdf93d81a3a6420882c92c",
                "data":{"component_type":2,"custom_id":"MJ::JOB::variation::{}::{}".format(index, messageHash)}}
    header = {
            'authorization' : Globals.SALAI_TOKEN
        }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header)
    return response


def BlendImg(image: list, dimensions: str):
    options = []
    attachments = []

    for _imgObj in image:
        options.append({"type":11,"name":"image{}".format(_imgObj['id']+1),"value":_imgObj['id']})
        attachments.append({"id":str(_imgObj['id']),"filename":_imgObj['filename'],"uploaded_filename":_imgObj['uploaded_filename']})

    options.append({"type":3,"name":"dimensions","value":dimensions})    
    
    payload = {
        "type":2,"application_id":Globals.MID_JOURNEY_ID,
        "guild_id":Globals.SERVER_ID,"channel_id":Globals.CHANNEL_ID,
        "session_id":"5da55e5780df4df1f4775c464245cba1",
        "data":{
            "version":"1067631020041580584","id":"1062880104792997970",
            "name":"blend","type":1,"options":options,
                "application_command":{
                    "id":"1062880104792997970","application_id":Globals.MID_JOURNEY_ID,
                    "version":"1067631020041580584",
                    "default_permission":True,
                    "default_member_permissions":None,"type":1,"nsfw":False,
                    "name":"blend","description":"Blend images together seamlessly!",
                    "dm_permission":True,"options":[
                        {"type":11,"name":"image1","description":"First image to add to the blend","required":True},
                        {"type":11,"name":"image2","description":"Second image to add to the blend","required":True},
                        {"type":3,"name":"dimensions","description":"The dimensions of the image. If not specified, the image will be square.","choices":[{"name":"Portrait","value":"--ar 2:3"},{"name":"Square","value":"--ar 1:1"},{"name":"Landscape","value":"--ar 3:2"}]},
                        {"type":11,"name":"image3","description":"Third image to add to the blend (optional)"},
                        {"type":11,"name":"image4","description":"Fourth image to add to the blend (optional)"},
                        {"type":11,"name":"image5","description":"Fifth image to add to the blend (optional)"}]},
                        "attachments":attachments,
                },"nonce":"1092666314859741184"
    }
    header = {
        'authorization' : Globals.SALAI_TOKEN
    }
    response = requests.post("https://discord.com/api/v9/interactions",
                            json = payload, headers = header)
    return response
