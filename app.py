from chatbot import chatbot
from flask import Flask,render_template,request,session,make_response
import json
import os.path
import uuid
import datetime
from getmac import get_mac_address as gma

app = Flask(__name__)
app.secret_key = 'shailesh1792666'
app.static_folder = 'static'

expire_date = datetime.datetime.now()
expire_date = expire_date + datetime.timedelta(days=90)


@app.route("/")
def home():
    chatQueue = {}
    
    if request.cookies.get('ActiveChatSessionID') is not None:
        chatSessionID=request.cookies.get('ActiveChatSessionID')
    else:
        chatSessionID = hex(uuid.getnode())+" | "+gma() #"CHAT_"+str(uuid.uuid1())
           
   # chatSessionID="CHAT_"+str(uuid.uuid1())
    #Open chat file
    if os.path.exists('chat.json'):
        with open('chat.json') as chatMsg:
            chatQueue = json.load(chatMsg)
            
    if chatSessionID in chatQueue.keys():
        #Resume chat
        pass
    else:
        #Create new chat head
        chatQueue[chatSessionID] = {'conversation':{}}
        with open('chat.json','w') as chatMsgData:
            json.dump(chatQueue,chatMsgData)        
    #Check chat no. exists in db
    #If exists then resume the conversation
    #Else create new chat head and store in db
    if request.cookies.get('ActiveChatSessionID') is None:
        res = make_response(render_template("index.html",chatID=chatSessionID))
        res.set_cookie('ActiveChatSessionID',chatSessionID,expires=expire_date)
        return res
    else:
        return render_template("index.html",chatID=chatSessionID)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    BotResponse = str(chatbot.get_response(userText))
    chatSessionID=request.cookies.get('ActiveChatSessionID')
    chatQueue = {}
    if os.path.exists('chat.json'):
        with open('chat.json') as chatMsg:
            chatQueue = json.loads(chatMsg.read())
            
    if chatSessionID in chatQueue.keys():
        MyConversation = chatQueue[chatSessionID]
        NodeNum = len(MyConversation["conversation"])
        MyConversation["conversation"][NodeNum]={'user':userText,'bot':BotResponse}
        
        #Create new chat head
        chatQueue[chatSessionID] = MyConversation
        with open('chat.json','w') as chatMsgData:
            json.dump(chatQueue,chatMsgData)     


    return BotResponse
    


if __name__ == '__main__':
    app.run()