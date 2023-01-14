from transformers import pipeline
import os


def bart_summarizer(text, max_length):
    # summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary = summarizer(text, max_length=max_length)[0]['summary_text']
    return summary


if __name__ == '__main__':
    text_example = open("example/text_example", "r").read()
    summary_text = bart_summarizer(text_example, max_length=100)
    print(summary_text)
