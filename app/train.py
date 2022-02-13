from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

bot = ChatBot("Johnny", read_only=True)

trainer = ListTrainer(bot)
trainer.train(['What services do you provide?', 'We provide electronic repairs, two-way delivery services, computer diagnostic and many more! Head to our home page to find out.'])
trainer.train(['How do I contact Vision Core?', 'Apart from our hotline that is open during office hours, our website offers a chatbot that allows you to either chat with a bot online or with one of our customer service staff!' ])
trainer.train(['What steps are involved when I decide to repair with Vision Core?', '1. Request for repair -> 2. Await for item status -> 3.Collect repair item'])
trainer.train(['What are the payment methods accepted?', 'We accept Paypal, Mastercard or your preferred bank app.'])
trainer.train(['How much is two-way delivery fee?', 'Two-way delivery fee has a $10 flat fee.'])
trainer.train(['What to do when I cannot drop off the product myself?', 'No problem! Just engage our two-way delivery service that will deliver to and from your doorstep at any time slot you choose.'])
trainer.train(['Thank you', "You're welcome!"])
trainer.train(['Thank you', 'I got you buddy!'])
trainer = ChatterBotCorpusTrainer #allows the chat bot to be trained using data from the ChatterBot dialog corpus.
trainer.train("chatterbot.corpus.english")