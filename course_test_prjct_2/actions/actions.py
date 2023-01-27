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
import re
class Validate_booking_form(FormValidationAction):

    def name(self) -> Text:
        return "validate_booking_form"

    def validate_count(self,slot_value:Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]):
                    if ((int(slot_value)>0)) and (int(slot_value)<10):
                        return {"count":slot_value}                    
                    else:
                        dispatcher.utter_message(text=f'Your count ,must be in between greater then 0 and less then 10')
                        return {"count":None}                            
                    
    def validate_city(self,slot_value:Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]):
                    p= '[A-Za-z]{2,25}( [A-Za-z]{2,25})?'
                    if (re.fullmatch(p,slot_value)) or (len(slot_value)<=2):
                        return {"city":slot_value}                    
                    else:
                        dispatcher.utter_message(text=f'Either your city name is short or misspelled.')
                        return {"city":None}   
