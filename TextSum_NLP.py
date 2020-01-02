import bs4 as bs
import urllib.request
import re
import nltk


# Scrape the Text from Website
scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article, 'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text


# Removing Square Brackets and Extra Spaces in Texts
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)


# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


# Find Weighted Frequency of Occurrence
stopwords = nltk.corpus.stopwords.words('english')
stopwords += ['many', 'also', 'use', 'used', 'one']

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    word = word.lower()
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)


# Sort the word_frequencies by values
word_frequencies = {k: v for k, v in sorted(word_frequencies.items(), reverse=True, key=lambda item: item[1])}
top_20_keywords = dict(list(word_frequencies.items())[0: 20])  # the 20 words with highest scores
print('Top 20 Keywords:')
print(top_20_keywords)


# Calculating Sentence Scores
sentence_list = nltk.sent_tokenize(article_text)
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:  # since we don't want a long sentence in the summary
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]


# Sort the word_frequencies by values
sentence_scores = {k: v for k, v in sorted(sentence_scores.items(), reverse=True, key=lambda item: item[1])}


# Get the Summary
summary = list(sentence_scores.keys())[:5]  # top 5 sentences with highest scores
summary = ' '.join(summary)
print('\nSummary:')
print(summary)

