

def aggregate(answers, aggregated):
    answers_ = answers['answers']
    for aggr_answer in aggregated:
        answer = [a for a in answers if a['key'] == aggr_answer['key']][0]
        if answer['type'] == 'num':
            pass
        elif answer['type'] == 'open':
            pass
        elif answer['type'] == 'mult':
            pass