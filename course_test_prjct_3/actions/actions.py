# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text, List, Any, Dict
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType,SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import os
import requests

path = os.getcwd()

url =  "https://api.openai.com/v1/completions"

key = "API_key"

headers = {"Authorization": f"Bearer {key}"}
      
class ActionapiClass(Action):
    def name(self):
        return "action_call_openai"
    def run(self, dispatcher, tracker, domain):
        #dispatcher.utter_message(text= "message you want to display" )
        context= tracker.latest_message['text']
        model= 'text-davinci-003'
        prompt= context
        data = {'model':model ,'prompt': prompt,'temperature':0,'max_tokens' :256,'stop':[" Human:", " AI:"]}
        if context:
            response=requests.post(url, headers=headers, json=data,verify=False)
            msg=response.json()['choices'][0]['text']
        else:
            dispatcher.utter_message('pls retry asking question')
        dispatcher.utter_message(text=str(msg))        
        return []