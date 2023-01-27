# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Text, List, Any, Dict
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType,SlotSet,Restarted,FollowupAction,ConversationPaused,ReminderScheduled
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import pandas as pd
import io
import re
import os
import numpy as np
import datetime


# query inspection part

PATH=os.getcwd()
FILE='\TVSMOTOR.csv'

raw_data= pd.read_csv(PATH+FILE)
raw_data['Date']=pd.to_datetime(raw_data['Date'], infer_datetime_format=True)
raw_data['Day']=raw_data['Date'].dt.day
raw_data['month']=raw_data['Date'].dt.month
raw_data['year']=raw_data['Date'].dt.year


valid_month={'january':1,'febraury':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,'october':10,'november':11,
            'december':12,'jan':1,'feb':2,'mar':3,'apr':4,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}


 
class Validate_Personal_info_form(FormValidationAction):

    def name(self) -> Text:
        return "validate_personal_info_form"

    def validate_name(self,
                    slot_value:Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                    p= '[A-Za-z]{2,25}( [A-Za-z]{2,25})?'
                    if (re.fullmatch(p,slot_value)) or (len(slot_value)<=2):
                        #dispatcher.utter_message(text=f'We have saved your name as {slot_value}')
                        return {"name":slot_value}                    
                    else:
                        dispatcher.utter_message(text=f'Either your name is short or i am assuming you miss-spelled.')
                        return {"name":None}                            
                    
    def validate_mail(self,
                    slot_value:Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    if(re.fullmatch(regex, slot_value)):
                        #dispatcher.utter_message(text=f'We have saved your mail id as {slot_value}')
                        return {"mail":slot_value}
                    else:
                        dispatcher.utter_message(text=f'Either your mail id is not valid or i am assuming you miss-spelled')
                        return {"mail":None}

class Validate_Simple_Query_form(FormValidationAction):

    def name(self) -> Text:
        return "validate_simple_query_form"

    def validate_month(self,
                    slot_value:Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                   
                    if slot_value.lower()in valid_month.keys():
                        #dispatcher.utter_message(text=f'Requesting for the report of the month {slot_value}')
                        m=valid_month[slot_value]
                        return {"month":m}
                    else:
                        dispatcher.utter_message(text=f'Please check the month ,please rephrase it??')
                        return {"month":None}

    def validate_year(self,
                    slot_value:Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                    
                    if slot_value and slot_value.isdigit():
                        if int(slot_value)>=1900 and int(slot_value)<=2022:
                            #dispatcher.utter_message(text=f'Requesting for the report of {slot_value}')
                            return {"year":int(slot_value)}
                        else:
                            dispatcher.utter_message(text=f'Choose the valid year b/w (1900-2022)')
                            return {"year":None}
                                         
                                         
class Validate_Simple_Query_form_2(FormValidationAction):

    def name(self) -> Text:
        return "validate_simple_query_2_form"

    def validate_month(self,
                    slot_value:Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                   
                    if slot_value.lower()in valid_month.keys():
                        #dispatcher.utter_message(text=f'you are requesting for the report of the month {slot_value}')
                        m=valid_month[slot_value]
                        return {"month":m}
                    else:
                        dispatcher.utter_message(text=f'Please check the month ,please rephrase it??')
                        return {"month":None}

    def validate_year(self,
                    slot_value:Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                    
                    if slot_value and slot_value.isdigit():
                        if int(slot_value)>=1900 and int(slot_value)<=2022:
                            #dispatcher.utter_message(text=f'you are requesting for the report of {slot_value}')
                            return {"year":int(slot_value)}
                        else:
                            dispatcher.utter_message(text=f'Choose the valid year b/w (1900-2022)')
                            return {"year":None}                                         
                                         
                              
# This part will ans the query user has asked

class Action_Report_gen(Action):

    def name(self) -> Text:
        return "action_report_gen"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        #current_query= tracker.get_slot('query_sub')
        current_month = int(tracker.get_slot('month'))
        current_year = int(tracker.get_slot('year'))        
        rep=raw_data.loc[(raw_data['year']==current_year) & (raw_data['month']==current_month)]
        rep.to_csv(PATH+'\ouput_report.csv',index=False)
        msg='successfully exported the report'
        dispatcher.utter_message(text=msg)
            
        return[]

class Action_sing_line_q1(Action):

    def name(self) -> Text:
        return "action_single_line_query_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        #current_query= tracker.get_slot('query_sub')
        current_high= tracker.get_slot('high')
        current_low = tracker.get_slot('low')

        current_column_open = tracker.get_slot('column_open')       
        current_column_close = tracker.get_slot('column_close')
        current_column_volume = tracker.get_slot('column_volume')        
    
        if current_high and current_column_open:
            index=np.argmax(raw_data["Open"])
            value=raw_data.iloc[index][['Open','Date']]
            dispatcher.utter_message(text=f'Here is the highest opening value of {value["Open"]} on {str(value["Date"])[:11]}')
        elif current_low and current_column_open:
            index=np.argmin(raw_data["Open"])
            value=raw_data.iloc[index][['Open','Date']]
            dispatcher.utter_message(text=f'Here is the lowest opening value of {value["Open"]} on {str(value["Date"])[:11]}')  
            
        elif current_high and current_column_close:
            index=np.argmax(raw_data["Close"])
            value=raw_data.iloc[index][['Close','Date']]
            dispatcher.utter_message(text=f'Here is the highest closing value of {value["Close"]} on {str(value["Date"])[:11]}')
        elif current_low and current_column_close:
            index=np.argmin(raw_data["Close"])
            value=raw_data.iloc[index][['Close','Date']]
            dispatcher.utter_message(text=f'Here is the lowest closing value of {value["Close"]} on {str(value["Date"])[:11]}')  
            
        elif current_high and current_column_volume:
            index=np.argmax(raw_data["Volume"])
            value=raw_data.iloc[index][['Volume','Date']]
            dispatcher.utter_message(text=f'Here is the highest traded value of {value["Volume"]} units on {str(value["Date"])[:11]}')
        elif current_low and current_column_volume:
            index=np.argmin(raw_data["Volume"])
            value=raw_data.iloc[index][['Volume','Date']]
            dispatcher.utter_message(text=f'Here is the lowest traded value of {value["Volume"]} units on {str(value["Date"])[:11]}') 
        else:
            dispatcher.utter_message(text=f'Please rephrase the question')
            return [FollowupAction("action_listen")]
            
               
        
        
        
class Action_Fresh_start(Action):

    def name(self):
        return "action_fresh_start"

    def run(self, dispatcher:CollectingDispatcher, tracker, domain):
        
        dispatcher.utter_message(text=f'chatbot restarting...')
    
        return [Restarted()]
        

        
class ActionTalkToAgent(Action):
    def name(self):
        return "action_talk_to_agent"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text=f'Okay!..i will handover to our Techincal assistant')
        return [ConversationPaused()] 


class ActionSetReminder(Action):
    def name(self):
        return "action_set_reminder"
    async def run(self, dispatcher, tracker, domain):    
        date=datetime.datetime.now()+datetime.timedelta(seconds=5)
        entities=tracker.latest_message.get('entities')
        reminder_name='EXTERNAL_'+tracker.sender_id
        reminder= ReminderScheduled(
                  "EXTERNAL_reminder",
                   trigger_date_time= date,
                   entities=entities,
                   kill_on_user_message=False,
        )
        dispatcher.utter_message(text=f'reminder_set')
        return[reminder]
        
class ActionReactReminder(Action):
    def name(self):
        return "action_react_to_reminder"
    async def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text='conversation are resumed...')
        return[ConversationResumed()]
 

class Action_avg_value(Action):

    def name(self) -> Text:
        return "action_avg_value"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            

        current_month = int(tracker.get_slot('month'))
        current_year = int(tracker.get_slot('year')) 

        current_column_open = tracker.get_slot('column_open')       
        current_column_close = tracker.get_slot('column_close')
        current_column_volume = tracker.get_slot('column_volume')
         
        keys= list(valid_month.keys())
        values=list(valid_month.values())
        month_index=values.index(current_month)
        month_name=keys[month_index]        
        
        rep=raw_data.loc[(raw_data['year']==current_year) & (raw_data['month']==current_month)]

        if current_column_open:
            avg=round(rep['Open'].mean(),2)
            dispatcher.utter_message(text=f'Here is the average opening value of {avg} for the month {month_name}') 
            
        elif current_column_close:
            avg=rep['Close'].mean()
            dispatcher.utter_message(text=f'Here is the average closing value of {avg} for the month {month_name}')

        elif current_column_volume:
            avg=rep['Volume'].mean()
            dispatcher.utter_message(text=f'Here is the average traded volume of {avg} for the month {month_name}')
            
        else:
            dispatcher.utter_message(text=f'Please rephrase the question')
            return [FollowupAction("action_listen")]
         
        



class ResetSlotOrder(Action):
    """Sets slotvalue to None"""
    def name(self):
        return "action_reset_slot_order"

    def run(self, dispatcher, tracker, domain):
        reset_slots=['low','high','month','year','column_close','column_open','column_volume','query','avg']
        return_slots = []
        for slot in tracker.slots:
            if slot in reset_slots:
                return_slots.append(SlotSet(slot, None))
        
        dispatcher.utter_message(text=f'.........................................................')
          
        return return_slots
        
class ActionSaveConversation(Action):
    def name(self):
        return "action_save_conversation"
    def run(self, dispatcher, tracker, domain):
        f=int(tracker.get_slot('feed'))
        print(f)
        chat_data=''
        conversation=tracker.events
        file=open('conv_histrory\chats.txt','w')
                
        for i in conversation:
            if i['event']=='user':
                intent_name=i['parse_data']['intent']['name']
                user_text=i['text']
                file.write('intent_name: '+ intent_name)
                file.write('\n')
                file.write('user_input: '+ user_text)
                file.write('\n')
                #print('user:{}'.format(i['text']))
  
            elif i['event']=='bot':
                file.write('bot_reply: '+i['text'])
                file.write('\n')
             
        file.close()
            
        #dispatcher.utter_message(text=f'all conversation saved')
        return []   