import spacy
from sklearn.cluster import KMeans
import pandas as pd
import logging

nlp = spacy.load('en_core_web_lg')
logger = logging.getLogger(__name__)


def get_dummies(categories, n=5):
    #TODO: expose the kmeans arguments here so user can tweak the clustering behavior

    df = pd.DataFrame()
    unique_categories = pd.Series(pd.Series(categories).unique())

    logger.warning(f'Perform vectorization on {unique_categories.shape[0]} unique categories')
    df['embedding'] = unique_categories.apply(lambda x: nlp(x).vector)
    df['category'] = unique_categories

    # flatten the embedding column into 300 columns to prepare for Kmeans
    X = pd.DataFrame(df['embedding'].tolist(), index=df['embedding'].index)
    logger.warning(f'Running K-means clustering. Cluster N: {n}')
    kmeans = KMeans(n_clusters=n, n_init='auto').fit(X)

    # Run the prediction and tag the categories
    logger.warning(f'Generating clustering prediction')
    df['smart_category'] = kmeans.predict(X)
    df['smart_category'] = df['smart_category'].apply(lambda x: f'category_{x}')

    # rejoin to the original input sequence
    category_df = pd.DataFrame(categories, columns=['category']).merge(df, how='left', on='category', sort=False)

    # use pandas' function to produce consistent output format
    smart_dummies = pd.get_dummies(category_df['smart_category'])

    return smart_dummies



