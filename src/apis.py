import os
import json

from .models import *
from .sentiment import *

from flask import Flask, \
    render_template, request, send_file



def get_attract(index_name):
    pass

def get_attracts(query=None):
    attracts, _ = get_all_attracts(query)

    return json.dumps(list(attracts))

def get_attracts_index():
    attracts, indices = get_attract_names()

    data = {
        'atttracs': attracts,
        'indices': indices,
    }

    return json.dumps(data)

def get_index_images_url():
    attracts, indices = get_attract_names()
    file_paths = [
        'apis/image/{}'.format(index) for index in indices]

    data = {
        'attracts': attracts,
        'file_paths': file_paths,
    }

    return json.dumps(data)

def get_all_images_url(query=None):
    attracts, indices = get_all_attracts(query)
    file_paths = [
        'apis/image/{}'.format(index) for index in indices]

    data = {
        'attracts': attracts,
        'file_paths': file_paths,
    }

    return json.dumps(data)

def get_image(index):
    file_path = os.getcwd()+ \
        '/static/img/thumbnails/'+str(index)+'.jpg'
    
    return send_file(file_path)

def get_data_criteria(attract):
    data = get_data_per_attract(attract)

    counter, aspeks, adjs, komentars = get_result_criteria(
        data, attract)

    place = get_attract_name(attract)

    data = {
        'counter': counter,
        'aspeks': aspeks,
        'adjs': adjs,
        'komentars': komentars,
        'place': place
    }

    return json.dumps(data)


def get_suggestions(attract):
    data = get_data_per_attract(attract)

    counter, _, _, _ = get_result_criteria(
        data, attract)

    counter = [(k, counter[k]) for k in sorted(
        counter, key=counter.get, reverse=True)]

    place = data[0]['place']

    aspeks = [key for key, val in counter]

    suggestions = []
    if len(aspeks) == 0:
        suggestions.append('Hingga saat ini belum ada respon negatif dari pengunjung, sehingga pengelola diharapakan dapat mempertahankan dan meningkatkan pelayanan serta mutu sarana dan prasarana yang ada pada {}.'.format(place))
    elif len(aspeks) == 1:
        suggestions.append('Dengan tingginya respon negatif dari pengunjung objek wisata {}, sebaiknya pengelola wisata segera memperbaiki segala sarana dan prasarana yang berkaitan dengan: {}.'.format(place, aspeks[0]))
    elif len(aspeks) == 2:
        suggestions.append('Dengan tingginya respon negatif dari pengunjung objek wisata {}, sebaiknya pengelola wisata segera memperbaiki segala sarana dan prasarana yang berkaitan dengan: {}.'.format(place, aspeks[0]))
        suggestions.append('Sebagian pengunjung memberikan respon negatif terhadap {}, sebaiknya pengelola wisata memperbaiki sarana dan prasarana yang berkaitan dengan: {}.'.format(place, aspeks[1]))
    else:
        suggestions.append('Dengan tingginya respon negatif dari pengunjung objek wisata {}, sebaiknya pengelola wisata segera memperbaiki segala sarana dan prasarana yang berkaitan dengan: {}.'.format(place, aspeks[0]))
        suggestions.append('Sebagian pengunjung memberikan respon negatif terhadap {}, sebaiknya pengelola wisata memperbaiki sarana dan prasarana yang berkaitan dengan: {}.'.format(place, aspeks[1]))
        suggestions.append('Pengunjung mengeluh saat mengunjungi {}, pengelola wisata diharapkan memeriksa sarana dan prasarana mengenai: {}.'.format(place, print_aspeks(aspeks[2:])))

    data = {
        'counter': counter,
        'suggestions': suggestions,
    }

    return json.dumps(data) 

def get_attract_name_by_id(id):
    return get_attract_name(id)

def get_sentiment(attract):
    file_path = os.getcwd()+ \
        '/data/dinamics/sentimentresult{}.pkl'.format(attract)

    if not os.path.isfile(file_path):
        data = get_text_for_sentiment(attract)
        texts = [d['text'] for d in data][:10]

        stopwords = get_stopwords()
        tokenized = normalize(texts, stopwords)
        vocabs = get_vocabs()
        X = vectorize(tokenized, vocabs)

        model = get_model_sentiment()
        preds = model.predict(X).tolist()

        with open(file_path, 'wb') as file:
            pickle.dump([texts, preds], file)
    else:
        with open(file_path, 'rb') as file:
            texts, preds = pickle.load(file)

    data = {
        'texts': texts,
        'preds': preds,
    }

    return json.dumps(data)
