import codecs
import json

from app.main.const import QUESTIONS_ADDR, AGGREGATED_ADDR
from flask import session
from random import randrange
from flask import request


def getData(survey):
    qs = []
    for key, item in survey.questions.items():
        answer = []
        if item.type == 'mult':
            for var in item.variants:
                if (request.form.get(var) is not None):
                    answer.append(request.form.get(var))
        else:
            answer.append(request.form.get(key))
        qs.append({"question_id": key, "answer": answer})
    return qs


def write_answer(qs):
    """
    This method writes the incoming data structure into json with a random hash number
    :param qs: structure od answers for raw files
    """
    hash = randrange(2197000)
    with open('app//data//raw//result_' + str(hash) + '.json', 'w') as fp:
        json.dump(qs, fp, sort_keys=True, indent=4)


def write_aggregated(qs):
    # with open('app//data//raw//result_' + str(hash) + '.json', 'w') as fp:
    #     for element in qs:
    #         for key, value in element:
    aggregated = json.load(codecs.open(AGGREGATED_ADDR, 'r', 'utf-8-sig'))
    questions = json.load(codecs.open(QUESTIONS_ADDR, 'r', 'utf-8-sig'))
    for element in qs:
        id_ = element["question_id"]
        # Ответ к id
        type_ = questions[id_]["type"]
        if id_ not in aggregated:
            agg_answer = list()
        else:
            agg_answer = aggregated[id_]['answer']
        print(element)
        print(type(id_), id_)
        print(type_)
        answer = element['answer']
        # Проверить три типа вопросов, добавить ответы для каждого
        if type_ == "num":
            # if this question was not answered before
            if not agg_answer:
                min_ = questions[id_][session['lang']]['variants'][0]
                max_ = questions[id_][session['lang']]['variants'][1]
                step_ = questions[id_][session['lang']]['variants'][2]
                # fill list with zeroes
                agg_answer = [0] * int((max_ - min_ + 1) / step_)
            agg_answer[int(answer[0]) - 1] += 1
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
