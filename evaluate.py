import os
import json
import csv
import statistics
from shutil import copyfile

response_path = './output/response'
responses = {}
evaluates = {}

def get_response_ids():
    response_filenames = os.listdir('%s' % response_path)
    response_ids = []
    for filename in response_filenames:
        if filename.endswith('.json'):
            filename_strip = filename[:-5]
            response_ids.append(filename_strip)
    return response_ids

def get_response_dict():
    response_ids = get_response_ids()
    for response_id in response_ids:
        file_path = '%s/%s.json' % (response_path, response_id)
        with open(file_path, 'r', encoding='UTF-8') as f:
            response_dict = json.load(f)
        if response_dict['uid'] in responses:
            responses[response_dict['uid']].append(response_dict)
        else:
            responses[response_dict['uid']] = [response_dict]

def evaluate():
    get_response_dict()
    uids = responses.keys()
    for uid in uids:
        evaluates[uid] = {}
        evaluates[uid]['uid'] = uid
        evaluates[uid]['wid'] = responses[uid][0]['wid']
        evaluates[uid]['valid'] = responses[uid][0]['isValid']

def conv(filename):
    with open('./output/%s_evaluated.csv' % filename, 'w', newline='', encoding='UTF-8') as f:
        lcount = 0
        for _,e in evaluates.items():
            w = csv.DictWriter(f, e.keys())
            if lcount == 0:
                w.writeheader()
            w.writerow(e)
            lcount += 1

def manage_turker(filename, answercode):
    mturks = {}
    
    with open('./output/%s.csv' % filename, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f) # skipinitialspace=True
        for row in reader:
            mturks[row['Answer.surveycode']] = row

    for _,mturk in mturks.items():
        if (mturk['Answer.surveycode'].startswith(answercode)):
            for uid in evaluates:
                if uid == mturk['Answer.surveycode'][8:]:
                    if evaluates[uid]['valid'] == False:
                        mturks[answercode+uid]['Reject'] = 'You failed in a validation question.'
                    else:
                        mturks[answercode+uid]['Approve'] = 'x'

    with open('./output/%s_evaluated.csv' % filename, 'w', encoding='UTF-8', newline='') as f:
        lcount = 0
        for _, m in mturks.items():
            w = csv.DictWriter(f, m.keys())
            if lcount == 0:
                w.writeheader()
            w.writerow(m)
            lcount += 1

def main():
    evaluate()
    conv('evaluate_response')
    # manage_turker('Batch_4307245_batch_results', 'example_')

if __name__ == '__main__':
    main()