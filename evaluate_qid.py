import csv
import json
import os
# from statistics import multimode
from statistics import mode, StatisticsError

response_path = './output/response'
labels = {'ent':0, 'con':1, 'neu':2, 'brk':3, 'hid':-1}
responses = {}
evaluates = {}

def get_response_ids():
    response_filenames = os.listdir('%s' % response_path)
    response_ids = []
    for filename in response_filenames:
        if filename.endswith('.json') and filename.startswith('valid__'):
        # if filename.endswith('.json'):
            filename_strip = filename[:-5]
            response_ids.append(filename_strip)
    return response_ids

def get_response_dict():
    response_ids = get_response_ids()
    for response_id in response_ids:
        file_path = '%s/%s.json' % (response_path, response_id)
        with open(file_path, 'r', encoding='UTF-8') as f:
            response_dict = json.load(f)
        if response_dict['qid'] in responses:
            responses[response_dict['qid']].append(response_dict)
        else:
            responses[response_dict['qid']] = [response_dict]

def evaluate():
    get_response_dict()
    qids = responses.keys()
    for qid in qids:
        evaluates[qid] = {}
        evaluates[qid]['qid'] = qid
        evaluates[qid]['label'] = labels[responses[qid][0]['label']]
        evaluates[qid]['res0'] = int(responses[qid][0]['strength'])
        evaluates[qid]['res1'] = int(responses[qid][1]['strength']) if len(responses[qid]) > 1 else None
        evaluates[qid]['res2'] = int(responses[qid][2]['strength']) if len(responses[qid]) > 2 else None
        res = [evaluates[qid]['res0'],evaluates[qid]['res1'],evaluates[qid]['res2']]
        # evaluates[qid]['majority'] = multimode(res)[0] if len(multimode(res)) == 1 else None
        try:
            evaluates[qid]['majority'] = mode(res)
        except StatisticsError:
            evaluates[qid]['majority'] = None

        if evaluates[qid]['majority'] is not None:
            if evaluates[qid]['label'] == evaluates[qid]['majority']:
                evaluates[qid]['result'] = 'same'
            else:
                evaluates[qid]['result'] = str(evaluates[qid]['label'])+'->'+str(evaluates[qid]['majority'])
        else:
            evaluates[qid]['result'] = 'no majority'

def conv(filename):
    with open('./output/%s_evaluated.csv' % filename, 'w', newline='', encoding='UTF-8') as f:
        lcount = 0
        for _,e in evaluates.items():
            w = csv.DictWriter(f, e.keys())
            if lcount == 0:
                w.writeheader()
            w.writerow(e)
            lcount += 1

def main():
    evaluate()
    conv('response-valid')

if __name__ == '__main__':
    main()