import json
import os.path

botFlowQueue = ''
if os.path.exists('raw.json'):
    with open('raw.json') as botFlow:
        botFlowQueue= json.load(botFlow)

#print(botFlowQueue['drawflow']['Home']['data'])

#Extract botFlow data
botFlowQueue = botFlowQueue['drawflow']['Home']['data']
#Arrange data in sequence via Travarsal tree
BotResSequence = []
#1 Identify first node
FirstNode = botFlowQueue['1']
#2 Make stack of nodes in sequence
def TreeTravarsal(FirstNode):
    global BotResSequence
    OUT_PUTS = FirstNode['outputs']
    #Count outputs
    if len(OUT_PUTS)>0:
        for eachOutputNode,Connections in OUT_PUTS:
            pass
            

#3 Build a queue for cmd ploting
print(botFlowQueue['1']['outputs'])
#NODE>CMDS>FLOW
PlugPins = []
BotFlow = []
for key,eachFlow in botFlowQueue.items():
    #print(eachFlow)
    MD_AND_CLBKs = ''
    BOT_RESPONSES = {}
    
    #//Identify next nodes 
    OUT_PUTS = FirstNode['outputs']
    #Count outputs
    if len(OUT_PUTS)>0:
        for eachOutputNode,Connections in OUT_PUTS.items():
            pass
    
    
    #//For message block
    #CALL_BACK_CMD::cmd_callback1::cmd_callback2::cmd_callback3
    if eachFlow['name'] == 'send_message':
        singleBlockFlow = eachFlow['data']['text']
        nodeNum = key
        if len(singleBlockFlow)>1:
            CMD_AND_CLBKs = 'CALL_BACK_CMD'
        for FlowPoint,FlowPointValue in singleBlockFlow.items():
            CMD_STR = "::cmd_callback"+nodeNum+"_"+FlowPoint
            CMD_AND_CLBKs+=CMD_STR
            BOT_RESPONSES[CMD_STR] = FlowPointValue.strip()
        BOT_RESPONSES['BLOCK'+key] = CMD_AND_CLBKs
        
    #//For bot_buttons    
    if eachFlow['name'] == 'bot_buttons':
        nodeNum = key
        #Show message about button
        CMD_AND_CLBKs = 'CALL_BACK_CMD'
        BtnMsg = eachFlow['data']['button_message']
        FlowPoint = "btnmsg"
        CMD_STR = "::cmd_callback"+nodeNum+"_"+FlowPoint
        CMD_AND_CLBKs+=CMD_STR
        BOT_RESPONSES[CMD_STR] = BtnMsg.strip()
        
        #Output connections
        NEXT_CMD_STR = eachFlow["outputs"]["output_1"]["connections"]
        NEXT_CMD_STR = NEXT_CMD_STR[0]["node"]
        print(NEXT_CMD_STR)
        #SHow buttons
        singleBlockFlow = eachFlow['data']['button_title']
        for FlowPoint,FlowPointValue in singleBlockFlow.items():
            CMD_STR = "::cmd_callback"+nodeNum+"_"+FlowPoint
            CMD_AND_CLBKs+=CMD_STR
            BOT_RESPONSES[CMD_STR] = '<button class="cmdText_Button" data-cmd="BLOCK'+NEXT_CMD_STR+'">'+FlowPointValue.strip()+'</button>'
        BOT_RESPONSES['BLOCK'+key] = CMD_AND_CLBKs    
        #print(CMD_AND_CLBKs)
        #print(BOT_RESPONSES)
    BotFlow.append(BOT_RESPONSES)

print(BotFlow)

#Write BotFlow file
if len(BotFlow)>0:
    f = open("BotFlow.txt", "w")
    for x in BotFlow:
        if len(x)>0:
            for k,v in x.items():
                f.write(k+"\n"+v+"\n")
    f.close()




