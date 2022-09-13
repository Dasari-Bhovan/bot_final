import os
import json
import pandas as pd
from telegram.ext import *
x={
  "API_KEY": "5751319983:AAHiDMjsHUx5SSTV_r4m0yKErPJSYcOobyo"
}
my_secret = x['API_KEY']

def sample_responses(input_text):
  x=str(input_text).upper()
  if x[0:2]=="19":
    BRANCH={"01":"CIV","02":"EEE","03":"MEC","04":"ECE","05":"CSE","12":"IT"}
  else:
    BRANCH={"01":"CIV","02":"EEE","03":"MEC","04":"ECE","05":"CSE","12":"IT","42":"CM","47":"CC","49":"CO","54":"AD"}
  
  if x in ("hi","hello","start"):
    return "Hey,how it's going?"
  if x in ("Who are you?","What do you do?","Why you?"):
    return "Hey,how it's going? I am results bot.I will tell your results."
  
  if len(x)==10 and (x[0:4]=="20BQ" or x[0:4]=="19BQ"):
    if x[6:8] in BRANCH:
      result=""
      for i in os.listdir(x[0:4]+"/"+BRANCH[x[6:8]]):
        df=pd.read_csv(x[0:4]+"/"+BRANCH[x[6:8]]+"/"+i)
        y=df.loc[df["HallTicket No"]==x]
        z=y.to_dict("list")
        result+=i[:-4]+" Sem Result\n"
        try:
          for i,j in z.items():
            result+=str(i)+" : "+str(j[0])+"\n"  
          result+="\n"  
        except:
          pass
      return result
    else:
      return "Enter hallticket number in the specific format\nTo check your all semester-end results type'<ROLL NUMBER> for example '20BQ1A42XX' OR To check about a single sem-end results type</ROLL NUMBER <SPACE> SEMESTER> for example '20BQ1A42XX 1-2'"
  elif len(x)==14 and (x[0:4]=="20BQ" or x[0:4]=="19BQ"):
    if x[6:8] in BRANCH:
      result=""
      df=pd.read_csv(x[0:4]+"/"+BRANCH[x[6:8]]+"/"+x[11:14]+".csv")
      y=df.loc[df["HallTicket No"]==x[0:10]]
      z=y.to_dict("list")
      result+=x[11:14]+" Sem Result\n"
      try:
        for i,j in z.items():
          result+=str(i)+" : "+str(j[0])+"\n"  
        result+="\n"  
      except:
        pass
    return result
      
      
  return "Welcome to Results_Bot.\nTo check your all semester-end results type'<ROLL NUMBER> for example '20BQ1A42XX' OR To check about a single sem-end results type</ROLL NUMBER <SPACE> SEMESTER> for example '20BQ1A42XX 1-2'"
        
        
          
          
    
def start_command(update,context):
  update.message.reply_text('Type hi to start')
  
def handle_messages(update,context):
  text=str(update.message.text).lower()
  response =sample_responses(text)
  update.message.reply_text(response)
  
def thank_you_command(update,context):
  text="Thank you for using bot.If any results are wrong.Let us know ."

def main():
  updater=Updater(my_secret,use_context=True)
  dp=updater.dispatcher
  dp.add_handler(CommandHandler("start",start_command))
  dp.add_handler(MessageHandler(Filters.text,handle_messages))
  updater.start_polling()
  updater.idle()
main()