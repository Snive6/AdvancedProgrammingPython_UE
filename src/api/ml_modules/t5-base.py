from transformers import pipeline
import os

summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")

if __name__ == '__main__':
    text_example = open("example/text_example.txt", "r").read()
    summary_text = summarizer(text_example, max_length=100, min_length=5, do_sample=False)[0]['summary_text']
    print(summary_text)