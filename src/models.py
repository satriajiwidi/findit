import os
import json
import random
import pickle
from collections import OrderedDict

from flask import Flask, \
    render_template, request, send_file


def get_all_attracts(query=None):
    file_path = os.getcwd()+'/data/attracts_list.txt'

    with open(file_path, 'r') as file:
        data = file.read().split('\n')

    indices = [d for index, d in enumerate(data) if index%2 == 0]
    names = [d for index, d in enumerate(data) if index%2 == 1]

    if query is not None:
        indices = [index+1 for index, d in enumerate(names)
            if query.lower() in d.lower()]
        names = [d for index, d in enumerate(names)
            if query.lower() in d.lower()]

    return names, indices

def get_attract_names(count=4):
    names, indices = get_all_attracts()
    attracts, indices = zip(*random.sample(
        list(zip(names, indices)), count))

    return attracts, indices

def get_images_path():
    pass

def get_attract_name(id):
    names, _ = get_all_attracts()

    return names[id-1]

def get_data_per_attract(attract):
    file_path = os.getcwd()+'/data/'

    with open(file_path+'data_new.json', 'r') as file:
        data = file.read().split('\n')
        data = data[:-1]
    
    attract = get_attract_name(attract)

    data = [json.loads(d) for d in data]
    data = [d for d in data if d['place'] == attract]

    return data

def get_result_criteria(data, id_attract):
    file_path = os.getcwd()+'/data/'

    with open(file_path+'aspek_umum.txt', 'r') as file:
        aspek_umum = file.read().split(',')
        
    with open(file_path+'sinonim.txt', 'r') as file:
        sinonim = file.read()
        
    with open(file_path+'kata_neg.txt', 'r') as file:
        kata_neg = file.read()
        
    sinonim = [baris.split(',') for baris in sinonim.split('\n')]
    kata_neg = [baris.split(',') for baris in kata_neg.split('\n')]

    file_path = os.getcwd()+ \
        '/data/dinamics/aspekresult{}.pkl'.format(id_attract)

    if not os.path.isfile(file_path):
        komentar_per_aspek = {}

        for d in data:
            for kalimat in d['text'].split('.'):
                kalimat = kalimat.strip()
                kalimat = ' '.join(
                    [kata.lower() for kata in kalimat.split()])
                for index_aspek, aspek in enumerate(aspek_umum):
                    for index_sin, sin in enumerate(sinonim[index_aspek]):
                        for index_neg, neg in enumerate(kata_neg[index_aspek]):
                            sin_yes, neg_yes = False, False

                            len_sin = len(sin.split())
                            len_neg = len(neg.split())

                            if len_sin == 1:
                                kalimat = kalimat.split()
                            if sin in kalimat:
                                sin_yes = True
                            if len_sin == 1:
                                kalimat = ' '.join(kalimat)

                            is_ketemu_tidak = False
                            if len_neg == 1:
                                kalimat = kalimat.split()
                            if neg in kalimat:
                                if len_neg == 1:
                                    is_ketemu_tidak = kalimat[kalimat.index(neg)-1] == 'tidak'
                                if not is_ketemu_tidak:
                                    neg_yes = True
                            if len_neg == 1:
                                kalimat = ' '.join(kalimat)

                            if sin_yes and neg_yes:
                                komentar_per_aspek[aspek, neg] = d['text']

        komentar_per_aspek = OrderedDict(sorted(komentar_per_aspek.items()))

        keys = [key[0] for key in komentar_per_aspek]
        counter = {key: keys.count(key) for key in set(keys)}

        aspeks = [aspek for aspek, _ in komentar_per_aspek]
        adjs = [adj for _, adj in komentar_per_aspek]
        komentars = [komentar_per_aspek[key] for key in komentar_per_aspek]

        with open(file_path, 'wb') as file:
            pickle.dump([counter, aspeks, adjs, komentars], file)

    else:
        with open(file_path, 'rb') as file:
            counter, aspeks, adjs, komentars = pickle.load(file)

    return counter, aspeks, adjs, komentars

def print_aspeks(aspeks):
    if len(aspeks) == 1:
        return aspeks[0]
    elif len(aspeks) == 2:
        return '{} dan {}'.format(aspeks[0], aspeks[1])
    else:
        string_aspek = ''
        for i in range(len(aspeks) - 1):
            string_aspek += aspeks[i] + ', '
        string_aspek += 'dan ' + aspeks[-1]

    return string_aspek

def get_text_for_sentiment(attract):
    data = get_data_per_attract(attract)

    return data

def get_model_sentiment():
    file_path = os.getcwd()+'/data/model_sentiment.pkl'

    with open(file_path, 'rb') as file:
        model = pickle.load(file)

    return model