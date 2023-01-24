import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


# Function to process the text, removing stop words and punctuation and creating a word frequency dictionary
def process_text(text, nlp):
    doc = nlp(text)
    word_frequencies = {}
    word_frequencies = {word.text: word_frequencies.get(word.text, 0) + 1 for word in doc if word.text.lower()
                        not in list(STOP_WORDS) and word.text.lower() not in punctuation}
    max_frequency = max(word_frequencies.values())
    return {word: freq/max_frequency for word, freq in word_frequencies.items()}


# Function to calculate sentence scores
def calculate_sentence_scores(doc, word_frequencies):
    return {sent: sum(word_frequencies.get(word.text.lower(), 0) for word in sent) for sent in
            [sent for sent in doc.sents]}


# Function to create the summary
def extractive_summarizer(text, per, nlp):
    doc = nlp(text)
    word_frequencies = process_text(text, nlp)
    sentence_scores = calculate_sentence_scores(doc, word_frequencies)
    select_length = int(len([sent for sent in doc.sents])*per)
    summary = ' '.join(" ".join(sent.text for sent in nlargest(select_length, sentence_scores, key=sentence_scores.get)).split())
    return summary


if __name__ == "__main__":
    text_example = open("example/text_example.txt", "r").read()

    # Loading the model once when the API is started
    nlp = spacy.load('en_core_web_sm')

    summarized_text = extractive_summarizer(text_example, 0.5, nlp)
    print(summarized_text)
    print(f'Text length: {len(text_example)}. Length of summarized text: {len(summarized_text)}')
