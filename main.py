import os
import json
import time
import random
from collections import Counter
from flask import Flask, redirect, request, render_template

app = Flask(__name__)
data_path = './data'
output_path = './output'
context_count_per_user = 11
user_count_per_context = 3
secret_code = 'example_'


def init_paths():
    paths = [
        '%s/contexts' % data_path,
        '%s/response' % output_path,
        '%s/no_response' % output_path,
        '%s/user_ids' % output_path,
    ]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


@app.route('/')
def index():
    return redirect('/tasks')


def get_all_context_ids():
    context_filenames = os.listdir('%s/contexts' % data_path)
    context_ids = []
    for filename in context_filenames:
        if filename.endswith('.json'):
            filename_strip = filename[:-5]
            context_ids.append(filename_strip)
    return context_ids


def get_context_response_count_dict():
    context_ids = get_all_context_ids()
    response_filenames = os.listdir('%s/response' % output_path)
    counter = {cid: 0 for cid in context_ids}
    for filename in response_filenames:
        if '__res__' not in filename:
            continue
        if filename.startswith('valid__') and filename.endswith('.json'):
            split_filename = filename.split('__res__')[0].split('valid__')
            if len(split_filename) != 2:
                continue
            context_id = split_filename[1]
            counter[context_id] += 1
    return counter


def get_response_by_wid(wid):
    response_filenames = os.listdir('%s/response/' % output_path)
    response_by_wid = []
    for filename in response_filenames:
        if filename.endswith('.json'):
            if filename.split('__')[3] == wid:
                response_by_wid.append(filename.split('__')[1])
    return response_by_wid


def draw_context_ids(wid):
    count_dict = get_context_response_count_dict()
    context_wids = get_response_by_wid(wid)
    context_ids = []
    while len(context_ids) < context_count_per_user:
        # Draw a context that currently has minimum number of responses.
        # valid_counts = [count for cid, count in count_dict.items() if cid not in context_ids]
        # if not valid_counts:
        #     break
        # min_count = min(valid_counts)
        # draw_box = [cid for cid, count in count_dict.items() if (count == min_count) and (cid not in context_ids)]
        # context_ids.append(random.choice(draw_box))
        # draw_box = [cid for cid, count in count_dict.items() if (count < user_count_per_context) and (cid not in context_ids) and (cid not in context_wids)]
        # context_ids.append(random.choice(draw_box))
        draw_box = [cid for cid, count in count_dict.items() if (count < user_count_per_context) and (cid not in context_ids) and (cid not in context_wids)]
        if len(draw_box) == 0:
            break
        # context_ids.append(draw_box[0])
        context_ids.append(random.choice(draw_box[0:39]))
    return context_ids


def get_context_dict(context_id):
    file_path = '%s/contexts/%s.json' % (data_path, context_id)
    with open(file_path, 'r') as f:
        context_dict = json.load(f)
    if 'id' not in context_dict:
        context_dict['id'] = context_id
    return context_dict


def get_questions():
    with open('%s/questions.json' % data_path, 'r') as f:
        questions = json.load(f)
    return questions


def get_validate_texts():
    with open('%s/validate_texts.json' % data_path, 'r') as f:
        validate_texts = json.load(f)
    return validate_texts


def draw_context_dicts(wid):
    context_ids = draw_context_ids(wid)
    return [get_context_dict(cid) for cid in context_ids]


def is_user_id(uid):
    file_path = '%s/user_ids/%s.json' % (output_path, uid)
    return os.path.exists(file_path)


def generate_user_id():
    while True:
        uid = ''.join(random.choice('abcedfghijklmnopqrstuvwxyz0123456789') for i in range(16))
        if not is_user_id(uid):
            break
    file_path = '%s/user_ids/%s.json' % (output_path, uid)
    with open(file_path, 'w') as f:
        f.write('!')
    return uid


def save_response(res_output_path, id, worker_id, user_id, result, isPassed):
    if isPassed:
        file_path = '%s/valid__%s__res__%s__%s.json' % (res_output_path, id, worker_id, user_id)
    else:
        file_path = '%s/invalid__%s__res__%s__%s.json' % (res_output_path, id, worker_id, user_id)
    with open(file_path, 'w') as f:
        f.write(json.dumps(result, sort_keys=True, indent=4))


@app.route('/tasks')
def task_index():
    return render_template('task_index.html')


@app.route('/tasks/')
def task_():
    return redirect('/tasks')

@app.route('/tasks/instruction')
@app.route('/tasks/instruction/')
def task_instruction():
    return render_template('task_instruction.html')

@app.route('/tasks/draw')
def task_draw():
    uid = generate_user_id()
    wid = request.args['workerId']
    context_dicts = draw_context_dicts(wid)
    questions = get_questions()
    # validate_texts = get_validate_texts()
    return render_template(
        'task_draw.html',
        uid=uid,
        contexts=context_dicts,
        questions=questions)
        # ,validate_texts=validate_texts)


@app.route('/tasks/submit', methods=['POST'])
def task_submit():
    data = json.loads(request.data)
    response = data['response']
    user_id = data['uid']
    isPassed = data['isPassed']
    # message = data['message']
    contexts = data['contexts']
    context_id = data['contextIndex']
    worker_id = data['workerId']
    validateValue = data['validateValue']
    validateContext = data['validateContext']
    timestamp = data['timestamp']
    
    validator = {'intend': str(validateValue),
                'answer': response[contexts[validateContext]['id']]}
    isValid = (validator['intend'] == validator['answer'])
    # validatorValues = data['validatorValues']
    
    if isPassed:
        res_output_path = output_path + "/response/"
    else:
        res_output_path = output_path + "/no_response/"
        result = dict(context="", statement="", qid = "", uid=user_id, strength=-1, wid=worker_id, timestamp=timestamp)
        # save_response(res_output_path, "attention", user_id, validatorValues, isPassed)
        save_response(res_output_path, "attention", worker_id, user_id, result, isPassed)

    # for context_id, value in response.items():
    #     save_response(res_output_path, context_id, user_id, value, isPassed)

    # for id, value in response.items():
    #     result = dict(original=original, cause=cause, effect=effect, edited=edited, strength=value)
    #     save_response(res_output_path, id, user_id, result, isPassed)
        # save_response(res_output_path, context_id, user_id, response, message, isPassed)
    # save_response(res_output_path, context_id, user_id, response, message, isPassed)

    for cid in range(0,context_id+1):
        if cid == validateContext:
            continue

        context = contexts[cid]['context']
        statement = contexts[cid]['statement']
        label = contexts[cid]['label']
        qid = contexts[cid]['id']
        value = response[qid] if qid in response else -1
        
        # value = response[contexts[cid[id]]]

        result = dict(context=context, statement=statement, label=label,
            qid = qid, uid=user_id, strength=value, wid=worker_id, isValid=isValid, validator=validator, timestamp=timestamp)
        save_response(res_output_path, qid, worker_id, user_id, result, isValid)

    return 'done:%s' % (secret_code + user_id)


@app.route('/tasks/done')
def task_done():
    code = request.args.get('code')
    return render_template('task_done.html', code=code)


init_paths()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)