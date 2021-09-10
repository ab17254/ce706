import csv
import string
import sys
import warnings
from collections import Counter

import numpy as np
from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
warnings.filterwarnings('ignore', category=DeprecationWarning)
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation
lemmatiser = WordNetLemmatizer()


def sentence_tokens_nostopwords(s):
    """
    Purpose: Splits input text into sentence tokens and removes the punctuation and stopwords
    :param s: Raw text from a file
    :return no_stopwords array: List of sentence tokens without stopwords
    """
    s = s.lower()
    tokens = sent_tokenize(s)
    no_stopwords = []
    for sent in tokens:
        no_stopwords.append(' '.join(w for w in word_tokenize(sent) if w not in stop))
    return no_stopwords


def tokens_nostopwords(s):
    """
    Purpose: Splits input text into word tokens and removes stopwords
    :param s: Raw text from file
    :return nostopwords array: List of tokens without stopwords
    """
    s = s.lower()
    tokens = word_tokenize(s)
    nostopwords = [word for word in tokens if not word in stop]
    return nostopwords


def stemming(s):
    """
    Purpose: Applies the WordNetLemmatizer to an list of sentence tokens
    :param s: Raw text from a file
    :return stemmed array: List of sentence tokens with stemmed words and raw text
    """
    stemmed = [s]
    s_tokens = sentence_tokens_nostopwords(s)
    for word in s_tokens:
        stemmed.append(lemmatiser.lemmatize(word))
    return stemmed


def freq(s):
    """
    Purpose: Counts the frequency of a word in a document for calcualting the DF
    :param s: word to be counted
    :return count int: count of the word
    """
    count = 0
    try:
        count = df[s]
    except:
        pass
    return count


def search(field, parameter):
    """
    Purpose: Used to search the indexed items
    :param string field: The search field the user wishes to search through
    :param string parameter: The item the user wishes to search for
    :return result array: Array of results from search query
    """
    field = field.lower()
    parameter = parameter.lower()
    query = {
        "query": {
            "match": {
                field: parameter
            }
        },
        "fields": ['cord_uid', 'title', field]
    }
    result = es.search(index='covid_data', body=query, size=1000)
    # pprint(result)
    return result


def format_search(results, field):
    """

    :param results string: The search field the user wishes to search through
    :param field string: The item the user wishes to search for
    """
    result_data = [doc for doc in results['hits']['hits']]
    if len(results['hits']['hits']) == 0:
        print("No search results")
    print("Total Results ", len(results["hits"]["hits"]))
    for doc in result_data:
        print("\n(ID: %s)" % (doc['_id']) + "\nSearch Result: %s" % (doc['_source'][field]) + "\nTF-IDF Score: %s" % (
            doc['_score']))


# opens file
with open('metadata.csv', encoding='utf-8') as f:
    index_name = 'covid_data'
    doctype = 'covid_open_research_data'
    reader = csv.reader(f)

    headers = []
    tf_idf = {}
    index = 0
    # deletes documents first to prevent overwriting
    es.indices.delete(index=index_name, ignore=[400, 404])
    es.indices.create(index=index_name, ignore=400)
    # creates the indices using the schema set out
    es.indices.put_mapping(
        index=index_name,
        doc_type=doctype,
        ignore=400,
        body={
            doctype: {
                "mappings": {
                    "properties": {
                        "cord_uid": {
                            "type": "text"
                        },
                        "sha": {
                            "type": "text"
                        },
                        "source_x": {
                            "type": "text"
                        },
                        "title": {
                            "type": "text"
                        },
                        "doi": {
                            "type": "text"
                        },
                        "pmcid": {
                            "type": "text"
                        },
                        "pubmed_id": {
                            "type": "text"
                        },
                        "license": {
                            "type": "text"
                        },
                        "abstract": {
                            "type": "text",
                            "similarity": 'BM25'
                        },
                        "publish_time": {
                            "type": "text"
                        },
                        "authors": {
                            "type": "text"
                        },
                        "journal": {
                            "type": "text"
                        },
                        "pdf_json_files": {
                            "type": "text"
                        },
                        "pmc_json_files": {
                            "type": "text"
                        },
                        "url": {
                            "type": "text"
                        }
                    }
                }
            }
        }
    )
    for row in reader:
        try:
            if index == 0:
                # ensures first row of csv is identified as the header
                headers = row
            if index == 1000:
                # skip anything over the 1000th item
                continue
            else:
                doc = {}
                for i, val in enumerate(row):
                    # perform stemming on documents
                    doc[headers[i]] = stemming(val)

                    # calculate TF-IDF for each document
                    if index != 0:
                        tokens = tokens_nostopwords(val)
                        counter = Counter(tokens)
                        token_count = len(tokens)
                        for token in np.unique(tokens):
                            tf = counter[token] / token_count
                            df = freq(token)
                            idf = np.log((1000 + 1) / (df + 1))
                            tf_idf[index, token] = tf * idf
                # index document
                es.index(index=index_name, doc_type=doctype, body=doc)

        except Exception as e:
            print('error: ' + str(e) + ' in ' + str(index))
        # print("Indexing Item: " + str(index))
        index = index + 1
    print("\nIndexed " + str(index) + " items")
f.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter an search field and a search query')
        sys.exit(0)
    else:
        search_field = sys.argv[1]
        search_query = sys.argv[2]
        format_search(search(search_field, search_query), search_field)
