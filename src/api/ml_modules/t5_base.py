from transformers import pipeline
import os


def t5_summarizer(text, max_length):
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
    # summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=max_length)[0]['summary_text']
    return summary


if __name__ == '__main__':
    text_example = open("example/text_example", "r").read()
    summary_text = t5_summarizer(text_example, max_length=50)
    print(summary_text)
