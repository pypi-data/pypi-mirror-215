import requests
import random
import time
import json


class ClientGPT:
  def __init__(self):
    self.chat_id = f"6{random.randint(1000, 9999)}5333004999ceadf1076"
    self.prompt = ""

  def send_message(self, message):
    data = {"question": f"({self.prompt}){message}","chat_id": self.chat_id,"timestamp": time.time()}

    res = requests.post('https://chat.chatgptdemo.net/chat_api_stream', json=data)
    res_parts = "["+res.text.replace('data: ', ',')[1:]+"]"
    load_data = json.loads(res_parts)

    response = ''
    for data in load_data[1:-1]:
      response += data['choices'][0]['delta']['content']
      
    return response
