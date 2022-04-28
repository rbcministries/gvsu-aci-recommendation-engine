from nltk.corpus import stopwords
import nltk
import re
import argparse
import os
import pandas as pd

nltk.download('stopwords')
word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem
stop_words = stopwords.words('english')
stop_words.extend(['daily', 'bread', 'crowder', 'collier', 'winn', 'bill', 'bookmark', 'site', 'cookies', 'ministries',
                'sign', 'cookies', 'us', 'one', 'make', 'god', 'gods', 'people', 'give', 'bible', 'jesus', 'life',
                'marvin', 'williams', 'like', 'also', 'settings', 'many', 'find', 'use', 'email', 'author', ':', 
                'today', 'v', '–', 'would', 'dave', 'branon'])

def clean_text(text):
  text = re.sub(':', ' ', text)
  text = re.sub('([0-9]+)', '', text)
  text_tokens = [word for word in text.split(' ')
                            if word not in stop_words]
  text_tokens = [word_rooter(word) for word in text_tokens]
  return ' '.join(text_tokens)

parser = argparse.ArgumentParser()

parser.add_argument('--train', type=str, default='data/train.csv')
parser.add_argument('--output', type=str, default=None)

args = parser.parse_args()

output_file = args.output
if output_file is None:
    output_file = args.train

train = pd.read_csv(os.path.join(os.path.dirname(__file__), args.train), encoding='cp1252')
train = train[train['url'].str.contains('\d{4}\/\d{2}\/\d{2}', regex=True) & train['url'].str.contains('https://odb.org')]
train['clean_text'] = train['text'].apply(clean_text)

train.to_csv(os.path.join(os.path.dirname(__file__), output_file))