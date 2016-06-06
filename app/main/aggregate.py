

def aggregate(answers, aggregated):
    answers_ = answers['answers']
    for aggr_answer in aggregated:
        answer = [a for a in answers if a['key'] == aggr_answer['key']][0]
