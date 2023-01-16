from transformers import pipeline


def bart_summarizer(text, max_length):
    bart_summarizer_model = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary = bart_summarizer_model(text, max_length=max_length)[0]['summary_text']
    return summary


if __name__ == '__main__':
    text_example = open("example/text_example", "r").read()
    summary_text = bart_summarizer(text_example, max_length=100)
    print(summary_text)
