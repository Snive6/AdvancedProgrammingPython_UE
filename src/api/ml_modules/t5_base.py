from transformers import pipeline
import os


def t5_summarizer(text, length):
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
    # summarizer = pipeline("summarization")
    summary = summarizer(text_example, max_length=length)[0]['summary_text']
    return summary


if __name__ == '__main__':
    text_example = open("src/api/example/text_example", "r").read()
    summary_text = t5_summarizer(text_example, length=100)
    print(summary_text)