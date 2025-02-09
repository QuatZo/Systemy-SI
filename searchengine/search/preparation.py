import time
import re

# region Functions


# ------------------------------------------- FUNKCJA PRZYGOTOWUJACA DANE -------------------------------------------- #
def prepare(arg_dataset, arg_path_to_stop_words):
    print("Preparing/Cleaning data, please wait...")
    marks = ['#', '$', '%', '&', '\'', '\'s', '(', ')', '*', '+', '-', '/', ':', ';',
             ',', '<', '=', '>', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~']  # znaki specjalne
    corpus = list()

    start = time.time()
    try:
        stop_words = open(arg_path_to_stop_words, encoding='utf8').read().split()  # czytaj stop wordsy, zrob liste
    except FileNotFoundError:
        stop_words = list()
    stop_words.append('')  # dodaj pusty element do usuniecia

    for row in arg_dataset:  # wyciagnij informacje
        temp_str = ""
        for i in range(len(row)):
            if i == 1:  # pomijamy rok
                continue
            if str(row[i]).casefold() != 'nan':  # przepisujemy tylko niepuste dane
                temp_str += str(row[i]).replace('.', ',').casefold() + '.'

        corpus.append(temp_str)  # jeden wpis to jeden film

    print(f"Info downloaded in: {time.time() - start} secs")

    start = time.time()
    corpus = "".join(corpus)  # tworzy dokument
    for mark in marks:  # usun znaki specjalne
        corpus = corpus.replace(mark, '')
    corpus = corpus.replace('?', '.').replace('!', '.').replace('_', ' ').split('.')  # autorzy na normalny format
    tokenized_sentences = [sentence.replace('.', '').split() for sentence in corpus]  # wyrazy z sentencji
    print(f"Sentences tokenization was done within: {time.time() - start} secs")

    # usuwanie stop-words z corpusu
    print("Removing unnecessary characters (f.e. 'a', 'the')")
    start = time.time()
    for sentence in range(len(tokenized_sentences)):
        for word in range(len(tokenized_sentences[sentence])):  # usuwanie liczb
            tokenized_sentences[sentence][word] = re.sub(r'[0-9\.]+', '', tokenized_sentences[sentence][word])

        # list comprehensions instead of typical loop, almost 10x faster (from 290secs to 33secs)
        # lista wyrazen zamiast petli, redukuje czas z ~300s do ~30s
        tokenized_sentences[sentence] = [x for x in tokenized_sentences[sentence]
                                         if x.casefold() not in stop_words]

    print("Preparation/Cleaning completed, time:", time.time() - start, "secs")
    return tokenized_sentences
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion
