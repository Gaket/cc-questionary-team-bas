import codecs
import json
import os

from config import QUESTIONS_ADDR, AGGREGATED_ADDR
from flask import session
from random import randrange
from flask import request


def getData(survey):
    qs = list()
    for key, item in survey.questions.items():
        answer = list()
        if item.type == 'mult':
            for var in item.variants:
                if request.form.get(var):
                    answer.append(request.form.get(var))
        else:
            answer.append(request.form.get(str(key)))
        qs.append({"question_id": key, "answer": answer})
    return qs


def getRawData():
    res = dict()
    for file in os.listdir('app//data//raw//'):
        if 'result' in file:
            key = file[:-5].split('_')[1]
            with open('app//data//raw//'+file, 'r') as fp:
                res[key] = json.load(fp)
    return res


def write_answer(qs):
    """
    This method writes the incoming data structure into json with a random hash number
    :param qs: structure od answers for raw files
    """
    hash = randrange(2197000)
    with open('app//data//raw//result_' + str(hash) + '.json', 'w') as fp:
        json.dump(qs, fp, sort_keys=True, indent=4)


def write_aggregated(qs):
    aggregated = json.load(codecs.open(AGGREGATED_ADDR, 'r', 'utf-8-sig'))
    questions = json.load(codecs.open(QUESTIONS_ADDR, 'r', 'utf-8-sig'))
    for element in qs:
        id_ = str(element["question_id"])
        # Ответ к id
        type_ = questions[id_]["type"]
        if id_ not in aggregated:
            aggregated[id_] = dict()
            agg_answer = list()
        else:
            agg_answer = aggregated[id_]['answer']
        print(element)
        print(type(id_), id_)
        print(type_)
        answer = element['answer']
        # Проверить три типа вопросов, добавить ответы для каждого
        if type_ == "num":
            min_ = int(questions[id_][session['lang']]['variants'][0])
            max_ = int(questions[id_][session['lang']]['variants'][1])
            step_ = int(questions[id_][session['lang']]['variants'][2])
            # if this question was not answered before
            if not agg_answer:
                agg_answer = [0] * int((max_ - min_ + 1) / step_ + 1)
            agg_answer[int(answer[0]) - min_] += 1
        elif type_ == 'open':
            agg_answer.append(answer[0])
        elif type_ == 'mult':
            # if this question was not answered before
            if not agg_answer:
                # fill list with zeroes
                agg_answer = [0] * len(questions[id_][session['lang']]['variants'])
            for ans in answer:
                index = questions[id_][session['lang']]['variants'].index(ans)
                agg_answer[index] += 1
        aggregated[id_]['answer'] = agg_answer
    # записать агрегированные данные
    with open(AGGREGATED_ADDR, 'w') as fh:
        json.dump(aggregated, fh, sort_keys=True, indent=4)
