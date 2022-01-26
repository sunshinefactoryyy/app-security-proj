from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot(
    'Johnny',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            "import_path": "chatterbot.logic.BestMatch",
            # "statement_comparison_function": chatterbot.comparisons.LevenshteinDistance,
            # "response_selection_method": chatterbot.response_selection.get_first_response
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'I need a quote for my computer.',
            'output_text': 'Please input your device model.'
        }
    ],
    #modify the input statement that a chat bot receives
    preprocessors=[ 
        'chatterbot.preprocessors.clean_whitespace'
    ],
    database_uri='sqlite:///database.sqlite3'
)

while True:
    try:
        bot_input = bot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break

response = bot.get_response('Help me!')
print(response)