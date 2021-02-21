import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic = dict()
    files = os.listdir(directory)
    for file in files:
        with open(os.path.join(directory, file)) as txt:
            t = txt.read()
            dic[file] = t
    return dic


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    li = []
    s = nltk.word_tokenize(document)
    for w in s:
        if w in nltk.corpus.stopwords.words("english"):
            continue

        for l in w:
            b = True
            if l not in string.punctuation:
                break
            b = False
        if b:
            li.append(w.lower())
    return li

    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    words = set()
    words_lists = []
    N = len(documents)

    for file in documents:
        words.update(documents[file])
        words_lists.append(documents[file])

    for word in words:
        c = 0
        for words_list in words_lists:
            if word in words_list:
                c += 1
        idf = math.log(N/c)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    l = []
    for file in files:
        tfidf = 0
        for word in query:
            tf = files[file].count(word)
            idf = idfs[word]
            tfidf += (tf * idf)
        l.append((file, tfidf))
    
    l.sort(key=lambda x: x[1] , reverse=True)

    topfiles = []
    for i in range(n):
        topfiles.append(l[i][0])

    return topfiles


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    l = []
    for sentence in sentences:
        c = 0
        matching_word = 0
        for word in sentences[sentence]:
            if word in query:
                c += 1
                matching_word += idfs[word]
        q_term_density = c/len(sentences[sentence])
        l.append( (sentence, matching_word, q_term_density) )
    
    l.sort(key=lambda x: (x[1],x[2]), reverse=True)

    top = []
    for i in range(n):
        top.append(l[i][0])

    return top


if __name__ == "__main__":
    main()
