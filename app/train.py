from chatbot import bot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

trainer = ChatterBotCorpusTrainer(bot)
trainer = ListTrainer(bot)

trainer.train([
    'How can I help you?',
    'I want to get a quote for my damaged laptop',
    'Have you checked out the set pricing for repairs yet?',
    'No, I have not',
    'This should help get you started: http://chatterbot.rtfd.org/en/latest/quickstart.html'
])

trainer.train(
    "chatterbot.corpus.english"
)