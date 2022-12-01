import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def summarize(text_process, per):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text_process)
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
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens)*per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)

    return summary


if __name__ == "__main__":
    text_example = 'Machine learning (ML) is the scientific study of algorithms and statistical models that computer ' \
                   'systems use to progressively improve their performance on a specific task. Machine learning ' \
                   'algorithms build a mathematical model of sample data, known as “training data”, in order to make ' \
                   'predictions or decisions without being explicitly programmed to perform the task. Machine ' \
                   'learning algorithms are used in the applications of email filtering, detection of network ' \
                   'intruders, and computer vision, where it is infeasible to develop an algorithm of specific ' \
                   'instructions for performing the task. Machine learning is closely related to computational ' \
                   'statistics, which focuses on making predictions using computers. The study of mathematical ' \
                   'optimization delivers methods, theory and application domains to the field of machine learning. ' \
                   'Data mining is a field of study within machine learning and focuses on exploratory data analysis ' \
                   'through unsupervised learning. In its application across business problems, machine learning is ' \
                   'also referred to as predictive analytics.'

    summarized_text = summarize(text_example, 0.5)
    print(summarized_text)
    print(f'Text length: {len(text_example)}. Length of summarized text: {len(summarized_text)}')
