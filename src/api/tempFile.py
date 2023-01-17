from ml_modules.pegasus import PegasusSummarizer

ps = PegasusSummarizer()
text_example = open("ml_modules/example/text_example.txt", "r").read()
summary = ps.summarize(text_example, max_length=100)
print(summary)