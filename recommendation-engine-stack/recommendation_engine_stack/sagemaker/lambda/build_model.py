import json
import os
import pickle
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    raw_data = [ pd.read_csv(file, encoding='cp1252') for file in event.input_files ]
    train_data = pd.concat(raw_data)

    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
    tfidf = tfidf_vectorizer.fit_transform(train_data['clean_text']).toarray()

    n_components = event['n_components']
    if n_components is not None:
        n_components = int(n_components)

    init_method = event['init_method']

    # Now use scikit-learn's decision tree classifier to train the model.
    nmf = NMF(n_components=n_components, random_state=0, init=init_method)
    nmf.fit(tfidf)

    # Need to update to actual good place to store
    model_path = event['model_path']

    # Save model
    with open(os.path.join(model_path, 'nmf_model.pkl'), 'wb') as out:
        pickle.dump(nmf, out)
    with open(os.path.join(model_path, 'tfidf_vectorizer.pkl'), 'wb') as out:
        pickle.dump(tfidf_vectorizer, out)

    return {
        'statusCode': 200,
        'headers': {
            'content-Type': 'text/plain'
        },
        'body': 'Model successfully built.'
    }