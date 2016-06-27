from app.main.data_processor import getRawData, getData, write_answer, write_aggregated


raw = getRawData()
for hash_, sur in raw.items():
    rec = dict()
    rec['result'] = list()
    rec['surveyed'] = 0
    rec['total'] = 0
    rec['comments'] = 'no comments'
    for a in sur:
        if a['question_id'] == 1:
            rec['name'] = a['answer'][0]
        elif a['question_id'] == 8:
            rec['comments'] = a['answer'][0] if a['answer'][0] else 'no comments'
        else:
            rec['result'].append(int(a['answer'][0]))
    rec['total'] = sum(rec['result'])
    print(rec)
    with open('results.csv', 'a') as csv:
        csv.write(':'.join((rec['name'],
                            str(rec['result'][0]),
                            str(rec['result'][1]),
                            str(rec['result'][2]),
                            str(rec['result'][3]),
                            str(rec['result'][4]),
                            str(rec['result'][5]),
                            rec['comments'])))
        csv.write('\n')
