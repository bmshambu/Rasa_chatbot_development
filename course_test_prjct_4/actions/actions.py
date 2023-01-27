# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text, List, Any, Dict
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType,SlotSet,Restarted,FollowupAction,ConversationPaused,ReminderScheduled
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import datetime


class ActionSetReminder(Action):
    def name(self):
        return "action_set_reminder"
    async def run(self, dispatcher, tracker, domain):
        time_slot= tracker.get_slot('time')
        print(time_slot)
        time_val= datetime.datetime.strptime(time_slot, "%Y-%m-%dT%H:%M:%S.%f%z")
        date=time_val
        print(date)
        entities=tracker.latest_message.get('entities')
        #reminder_name='EXTERNAL_'+tracker.sender_id
        reminder= ReminderScheduled(
                  "EXTERNAL_reminder",
                   trigger_date_time= date,
                   entities=entities,
                   kill_on_user_message=False,
        )
        dispatcher.utter_message(text=f'reminder is set for {date}')
        return[reminder]
        
class ActionReactReminder(Action):
    def name(self):
        return "action_react_to_reminder"
    async def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response='utter_remind')
        return[]