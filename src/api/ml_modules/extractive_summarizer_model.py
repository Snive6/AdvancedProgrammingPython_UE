import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


# Function to process the text, removing stop words and punctuation and creating a word frequency dictionary
def process_text(text, nlp):
    doc = nlp(text)
    word_frequencies = {}

    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    return word_frequencies


# Function to calculate sentence scores
def calculate_sentence_scores(doc, word_frequencies):
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    return sentence_scores


# Function to create the summary
def extractive_summarizer(text, per, nlp):
    doc = nlp(text)
    word_frequencies = process_text(text, nlp)
    sentence_scores = calculate_sentence_scores(doc, word_frequencies)
    sentence_tokens = [sent for sent in doc.sents]
    select_length = int(len(sentence_tokens)*per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    summary = " ".join(summary.split())

    return summary


if __name__ == "__main__":
    text_example = open("example/text_example", "r").read()

    # Loading the model once when the API is started
    nlp = spacy.load('en_core_web_sm')

    summarized_text = extractive_summarizer(text_example, 0.5, nlp)
    print(summarized_text)
    print(f'Text length: {len(text_example)}. Length of summarized text: {len(summarized_text)}')
