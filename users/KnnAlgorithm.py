import os
import time
import gc
import argparse

# data science imports
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# utils import
from fuzzywuzzy import fuzz


class KnnRecommender:
    rsdict = {}

    def __init__(self, path_services, path_ratings):

        self.path_services = path_services
        self.path_ratings = path_ratings
        self.movie_rating_thres = 0
        self.user_rating_thres = 0
        self.model = NearestNeighbors()

    def set_filter_params(self, movie_rating_thres, user_rating_thres):

        self.movie_rating_thres = movie_rating_thres
        self.user_rating_thres = user_rating_thres

    def set_model_params(self, n_neighbors, algorithm, metric, n_jobs=None):

        if n_jobs and (n_jobs > 1 or n_jobs == -1):
            os.environ['JOBLIB_TEMP_FOLDER'] = '/tmp'
        self.model.set_params(**{
            'n_neighbors': n_neighbors,
            'algorithm': algorithm,
            'metric': metric,
            'n_jobs': n_jobs})

    def _prep_data(self):
        # read data
        df_movies = pd.read_csv(
            os.path.join(self.path_services),
            usecols=['serviceId', 'servicename'],
            dtype={'serviceId': 'int32', 'servicename': 'str'})
        df_ratings = pd.read_csv(
            os.path.join(self.path_ratings),
            usecols=['userId', 'serviceId', 'rating'],
            dtype={'userId': 'int32', 'serviceId': 'int32', 'rating': 'float32'})
        # filter data
        df_movies_cnt = pd.DataFrame(
            df_ratings.groupby('serviceId').size(),
            columns=['count'])
        popular_movies = list(set(df_movies_cnt.query('count >= @self.movie_rating_thres').index))  # noqa
        movies_filter = df_ratings.serviceId.isin(popular_movies).values

        df_users_cnt = pd.DataFrame(
            df_ratings.groupby('userId').size(),
            columns=['count'])
        active_users = list(set(df_users_cnt.query('count >= @self.user_rating_thres').index))  # noqa
        users_filter = df_ratings.userId.isin(active_users).values

        df_ratings_filtered = df_ratings[movies_filter & users_filter]

        # pivot and create movie-user matrix
        movie_user_mat = df_ratings_filtered.pivot(
            index='serviceId', columns='userId', values='rating').fillna(0)
        # create mapper from movie servicename to index
        hashmap = {
            movie: i for i, movie in
            enumerate(list(df_movies.set_index('serviceId').loc[movie_user_mat.index].servicename))  # noqa
        }
        # transform matrix to scipy sparse matrix
        movie_user_mat_sparse = csr_matrix(movie_user_mat.values)

        # clean up
        del df_movies, df_movies_cnt, df_users_cnt
        del df_ratings, df_ratings_filtered, movie_user_mat
        gc.collect()
        return movie_user_mat_sparse, hashmap

    def _fuzzy_matching(self, hashmap, fav_movie):
        match_tuple = []
        # get match
        for servicename, idx in hashmap.items():
            ratio = fuzz.ratio(servicename.lower(), fav_movie.lower())
            if ratio >= 60:
                match_tuple.append((servicename, idx, ratio))
        # sort
        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            print('Oops! No match is found')
            return 1
        else:
            print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
            #print('This man ',match_tuple[0][1])
            return match_tuple[0][1]

    def _inference(self, model, data, hashmap,fav_movie, n_recommendations):

        # fit
        model.fit(data)
        # get input movie index
        print('You have input movie:', fav_movie)
        idx = self._fuzzy_matching(hashmap, fav_movie)
        #print('Result is ', idx)
        if idx == None:
            idx = 1
        # inference
        print('Recommendation system start to make inference')
        print('......\n')
        t0 = time.time()
        distances, indices = model.kneighbors(data[idx],n_neighbors=n_recommendations + 1)
        # get list of raw idx of recommendations
        raw_recommends = \
            sorted(
                list(
                    zip(
                        indices.squeeze().tolist(),
                        distances.squeeze().tolist()
                    )
                ),
                key=lambda x: x[1]
            )[:0:-1]
        print('It took my system {:.2f}s to make inference \n\
              '.format(time.time() - t0))
        # return recommendation (serviceId, distance)
        return raw_recommends

    def make_recommendations(self, fav_movie, n_recommendations):
        rsdict={}
        # get data
        movie_user_mat_sparse, hashmap = self._prep_data()
        # get recommendations
        raw_recommends = self._inference(self.model, movie_user_mat_sparse, hashmap,fav_movie, n_recommendations)
        # print results
        reverse_hashmap = {v: k for k, v in hashmap.items()}
        #print('Recommendations for {}:'.format(fav_movie))
        for i, (idx, dist) in enumerate(raw_recommends):
            #print('{0}: {1}, with distance of {2}'.format(i + 1, reverse_hashmap[idx], dist))
            #return reverse_hashmap[idx],dist
            rsdict.update({reverse_hashmap[idx]:dist})
        return rsdict


