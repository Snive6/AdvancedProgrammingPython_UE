from transformers import pipeline


class BartSummarizer:
    def __init__(self):
        self.model = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        self.model.model.eval()

    def summarize(self, text, max_length):
        summary = self.model(text, max_length=max_length)[0]['summary_text']
        return summary


# def bart_summarizer(text, max_length):
#     bart_summarizer_model = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
#     summary = bart_summarizer_model(text, max_length=max_length)[0]['summary_text']
#     return summary


if __name__ == '__main__':
    text_example = open("example/text_example", "r").read()
    bs = BartSummarizer()
    summary_text = bs.summarize(text_example, max_length=100)
    # summary_text = bart_summarizer(text_example, max_length=100)
    print(summary_text)
