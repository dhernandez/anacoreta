import os

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from app.storage.StorageManager import StorageManager
from app.utils.utils import get_stopwords


class Trendings:
    @staticmethod
    def get_trendings():
        text_to_extract = StorageManager.get_last_texts(float(os.getenv('MINUTES_FOR_EXTRACT_TRENDINGS')))
        if len(text_to_extract) < 1:
            return []
        cv = CountVectorizer(stop_words=get_stopwords(), analyzer='word', ngram_range=(1, 2), min_df=1, max_df=0.7)
        word_count_vector = cv.fit_transform(text_to_extract)
        tfidf_transformer = TfidfTransformer(smooth_idf=False, use_idf=True)
        tfidf_transformer.fit(word_count_vector)
        feature_names = cv.get_feature_names()
        tf_idf_vector = tfidf_transformer.transform(cv.transform(text_to_extract))
        sorted_items = Trendings._sort_coo(tf_idf_vector.tocoo())

        # extract only the top n; n here is 10
        keywords = Trendings._extract_topn_from_vector(feature_names, sorted_items, 10)
        return keywords

    @staticmethod
    def _sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    @staticmethod
    def _extract_topn_from_vector(feature_names, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""

        # use only topn items from vector
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        # word index and corresponding tf-idf score
        for idx, score in sorted_items:
            # keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        # create a tuples of feature,score
        # results = zip(feature_vals,score_vals)
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results
