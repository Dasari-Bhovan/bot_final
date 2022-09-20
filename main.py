import os
import json
from re import X
import pandas as pd
from telegram.ext import *
x={
  "API_KEY": "5751319983:AAHiDMjsHUx5SSTV_r4m0yKErPJSYcOobyo"
}
my_secret = x['API_KEY']

def sample_responses(input_text):
  x=str(input_text).upper()
  if x[0:2]=="19" or (x[0:2]=="20" and x[4:6]=="5A"):
    BRANCH={"01":"CIV","02":"EEE","03":"MEC","04":"ECE","05":"CSE","12":"IT"}
  elif x[0:2]=="20" or (x[0:2]=="21" and x[4:6]=="5A"):
    BRANCH={"01":"CIV","02":"EEE","03":"MEC","04":"ECE","05":"CSE","12":"IT","42":"CM","47":"CC","49":"CO","54":"AD"}
  elif x[0:2]=="21" or (x[0:2]=="22" and x[4:6]=="5A"):
    BRANCH={"01":"CIV","02":"EEE","03":"MEC","04":"ECE","05":"CSE","12":"INF","42":"CSM","47":"CIC","49":"CSO","54":"AID","61":"AIM"}
  else:
    return "check year correctly"
  if x in ("hi","hello","start"):
    return "Hey,how it's going?"
  if x in ("Who are you?","What do you do?","Why you?"):
    return "Hey,how it's going? I am results bot.I will tell your results."
  try:
    if len(x)==10 and (x[0:4]=="20BQ" or x[0:4]=="19BQ" or x[0:4]=="21BQ"):
      if x[6:8] in BRANCH and  (x[4:6]=="5A" or x[4:6]=="1A"):
        result=""
        y1=x[0:4]
        if x[0:6]=="21BQ5A":
          y1="20BQ"
        elif  x[0:6]=="20BQ1A":
          y1="20BQ"
        elif  x[0:6]=="20BQ5A":
          y1="19BQ"
        dir=os.listdir(y1+"/"+str(BRANCH[x[6:8]]))
        dir.sort()
        for sem in dir:
          if sem[:-4]=="1-2" and x[4:6]=="5A":
            continue
          df=pd.read_csv(str(y1)+"/"+str(BRANCH[x[6:8]])+"/"+str(sem))
          y=df.loc[df["HallTicket No"]==x]
          z=y.to_dict("list")
          result+=sem[:-4]+" Sem Result\n"
          try:
            for i,j in z.items():
              result+=str(i)+" : "+str(j[0])+"\n"
          except:
            result+="Not Found"
            pass
          
          result+="\n"  
        return result
      else:
        return "Enter hallticket number in the specific format\nTo check your all semester-end results type'<ROLL NUMBER> for example '20BQ1A42XX' OR To check about a single sem-end results type</ROLL NUMBER <SPACE> SEMESTER> for example '20BQ1A42XX 1-2'"
    elif len(x)==14 and (x[0:4]=="20BQ" or x[0:4]=="19BQ" or x[0:4]=="21BQ" ):
      if x[6:8] in BRANCH and (x[4:6]=="5A" or x[4:6]=="1A"):
        result=""
        y1=x[0:4]
        if x[0:6]=="21BQ5A":
          y1="20BQ"
        elif  x[0:6]=="20BQ5A":
          y1="19BQ"
          
        df=pd.read_csv(y1+"/"+BRANCH[x[6:8]]+"/"+x[11:14]+".csv")
        y=df.loc[df["HallTicket No"]==x[0:10]]
        z=y.to_dict("list")
        result+=x[11:14]+" Sem Result\n"
        try:
          for i,j in z.items():
            result+=str(i)+" : "+str(j[0])+"\n"  
          result+="\n"
        except:
          result+="Data Not Found"
        return result
  except FileNotFoundError:
    return "Enter roll number correctly"
      
  return "Welcome to Results_Bot.\nTo check your all semester-end results type'<ROLL NUMBER> for example '20BQ1A42XX' OR To check about a single sem-end results type</ROLL NUMBER <SPACE> SEMESTER> for example '20BQ1A42XX 1-2'"
        
def start_command(update,context):
  update.message.reply_text('Type hi to start')
def results_command(update,context):
      update.message.reply_text('Type your roll number to know your result')
      
def handle_messages(update,context):
  text=str(update.message.text).upper()
  response =sample_responses(text)
  update.message.reply_text(response)
  update.message.reply_text("If your result is wrong.Let us know")
  
def thank_you_command(update,context):
  text="Thank you for using bot.If any results are wrong.Let us know ."

def main():
  updater=Updater(my_secret,use_context=True)
  dp=updater.dispatcher
  dp.add_handler(CommandHandler("start",start_command))
  dp.add_handler(CommandHandler("results",results_command))
  dp.add_handler(MessageHandler(Filters.text,handle_messages))
  updater.start_polling()
  updater.idle()
main()
  
