from chatterbot.logic import LogicAdapter 


class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = statement.text.split('::')
        if 'API_CMD' in words:
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import requests

        CMD_LIST = input_statement.text.split('::')
        BOT_RESPONSE = 'Sorry, I am not getting you.'
        confidence = 0
        
        #Fetch order info
        if CMD_LIST[1] == 'FETCH-ORDER-INFO':
            ORDER_ID = CMD_LIST[-1]
            #A list of AmazonOrderId values. An AmazonOrderId is an Amazon-defined order identifier, in 3-7-7 format.
            API_END_POINT = f'https://api.keywordkiller.com/rebateme/checkorder?orderid={ORDER_ID}'
            # Make a request to the Order Status API
            response = requests.get(API_END_POINT)
            data = response.json()
            # Let's base the confidence value on if the request was successful
            if response.status_code == 200:
                confidence = 1
            else:
                confidence = 0
                
            if data['status'] == True:
                BOT_RESPONSE_CMD = 'cmd_callback7::valid_order_id::cmd_callback8'
            else:
                BOT_RESPONSE_CMD = "cmd_callback7::invalid_order_id"     
                
                
            response_statement = Statement(text=str("CALL_BACK_CMD::")+BOT_RESPONSE_CMD)
            
            selected_statement = response_statement
            selected_statement.confidence = confidence
        #Fetch ASIN Info
        elif CMD_LIST[1] == 'FETCH-ASIN-INFO':
            ASIN = CMD_LIST[-1]
            API_END_POINT = f'https://api.keywordkiller.com/rebateme/verifyAsin?asin={ASIN}'
            # Make a request to the asin API
            response = requests.get(API_END_POINT)
            data = response.json()
            # Let's base the confidence value on if the request was successful
            if response.status_code == 200:
                confidence = 1
            else:
                confidence = 0
                
            if data['status'] == True:
                BOT_RESPONSE_CMD = 'cmd_callback1::cmd_callback2::cmd_callback3'
            else:
                BOT_RESPONSE_CMD = "invalid_asin"     
                
                
            response_statement = Statement(text=str("CALL_BACK_CMD::")+BOT_RESPONSE_CMD)
            
            selected_statement = response_statement
            selected_statement.confidence = confidence
            
        #Upload product pic
        elif CMD_LIST[1] == 'UPLOAD-IMG-DATA':
    
            API_END_POINT = 'https://api.keywordkiller.com/rebateme/checkorder?orderid=111-3178504-9510623'
            # Make a request to the asin API
            response = requests.get(API_END_POINT)
            data = response.json()
            # Let's base the confidence value on if the request was successful
            if response.status_code == 200:
                confidence = 1
            else:
                confidence = 0
                
            if data['status'] == True:
                BOT_RESPONSE_CMD = ''
            else:
                BOT_RESPONSE_CMD = ""     
                
                
            response_statement = Statement(text=str("CALL_BACK_CMD::")+BOT_RESPONSE_CMD)
            
            selected_statement = response_statement
            selected_statement.confidence = confidence   
     
        #Verify email id
        elif CMD_LIST[1] == 'VERIFY-PAYPAL-EMAIL':
    
            API_END_POINT = 'https://api.keywordkiller.com/rebateme/checkorder?orderid=111-3178504-9510623'
            # Make a request to the asin API
            response = requests.get(API_END_POINT)
            data = response.json()
            # Let's base the confidence value on if the request was successful
            if response.status_code == 200:
                confidence = 1
            else:
                confidence = 0
                
            if data['status'] == True:
                BOT_RESPONSE_CMD = "cmd_callback9::cmd_callback10"
            else:
                BOT_RESPONSE_CMD = "invalid_paypal_email"     
                
                
            response_statement = Statement(text=str("CALL_BACK_CMD::")+BOT_RESPONSE_CMD)
            
            selected_statement = response_statement
            selected_statement.confidence = confidence  
            
        return selected_statement