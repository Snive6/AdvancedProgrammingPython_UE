import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def process_text(text, nlp):
    """
    This function takes in the text and the nlp object and returns a dictionary
    of word frequencies with words as keys and their frequency as values
    """
    doc = nlp(text)
    word_frequencies = count_word_frequencies(doc)
    filtered_frequencies = filter_stop_words_and_punctuation(word_frequencies)
    normalized_frequencies = normalize_frequencies(filtered_frequencies)
    return normalized_frequencies


def count_word_frequencies(doc):
    """
    This function takes in the doc object and returns a dictionary of word frequencies
    with words as keys and their frequency as values
    """
    word_frequencies = {}
    return {word.text: word_frequencies.get(word.text, 0) + 1 for word in doc}


def filter_stop_words_and_punctuation(word_frequencies):
    """
    This function takes in a dictionary of word frequencies and filters out the stop words and punctuation
    and returns a dictionary of filtered word frequencies.
    """
    return {word: freq for word, freq in word_frequencies.items()
            if word.lower() not in list(STOP_WORDS) and word.lower() not in punctuation}


def normalize_frequencies(word_frequencies):
    """
    This function takes in a dictionary of word frequencies and normalizes them
    by diving each frequency by the maximum frequency
    """
    max_frequency = max(word_frequencies.values())
    return {word: freq/max_frequency for word, freq in word_frequencies.items()}


# Function to calculate sentence scores
def calculate_sentence_scores(doc, word_frequencies):
    """
    This function takes in the doc object and a dictionary of word frequencies
    and returns a dictionary of sentence scores with sentences as keys and their scores as values
    """
    return {sent: sum(word_frequencies.get(word.text.lower(), 0) for word in sent) for sent in
            [sent for sent in doc.sents]}


# Function to create the summary
def extractive_summarizer(text, per, nlp):
    """
    This function takes in the text, the percentage and the nlp object,
    and returns a summary of the text
    """
    doc = nlp(text)
    word_frequencies = process_text(text, nlp)
    sentence_scores = calculate_sentence_scores(doc, word_frequencies)
    summary = generate_summary(text, per, nlp, sentence_scores)
    return summary


# The function to generate summary
def generate_summary(text, per, nlp, sentence_scores):
    """
    This function takes in the text, the percentage, the nlp object, and
    a dictionary of sentence scores and generates a summary of the text by selecting the top
    sentences based on their scores and returning them as a concatenated string.
    """
    select_length = int(len([sent for sent in nlp(text).sents])*per)
    summary = ' '.join(" ".join(sent.text for sent in
                                nlargest(select_length, sentence_scores, key=sentence_scores.get)).split())
    return summary


if __name__ == "__main__":
    text_example = open("example/text_example.txt", "r").read()

    # Loading the model once when the API is started
    nlp = spacy.load('en_core_web_sm')

    summarized_text = extractive_summarizer(text_example, 0.5, nlp)
    print(summarized_text)
    print(f'Text length: {len(text_example)}. Length of summarized text: {len(summarized_text)}')
