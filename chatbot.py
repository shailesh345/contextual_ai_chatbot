from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

# Enable info level logging
logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    'Rebate me',
     preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    #storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
         'import_path' : 'mylogicadapter.MyLogicAdapter'
        },
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.TimeLogicAdapter',
    ],
    #database_uri='sqlite:///database.sqlite3'
) 

#Conversation Qst & Ans
training_data_quesans = open('training_data/rebate_quest_ans.txt').read().splitlines()
training_data_personal = open('training_data/qst.txt').read().splitlines()

training_data = training_data_quesans + training_data_personal
trainer = ListTrainer(chatbot)
trainer.train(training_data)  


# Training with english corpus data
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train(
    'chatterbot.corpus.english'
)