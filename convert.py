import csv
import random
import json
import os
import glob

train = {'mnli_synthetic_examples_v4_scores_v3_final':'train', 'anli_synthetic_examples_v4_scores_v3_final':'train'}
val = {'anli_synthetic_examples_v4_scores_v3_final':'val', 'snli_synthetic_examples_v4_scores_v3_final':'val', 'fnli_synthetic_examples_v4_scores_v3_final':'val'}
test = {'mnli_synthetic_examples_v4_scores_v3_final_test':'val', 'mnli_mm_synthetic_examples_v4_scores_v3_final':'val', 'anli_synthetic_examples_v4_scores_v3_final':'test', 'snli_synthetic_examples_v4_scores_v3_final':'test', 'snli_hard_synthetic_examples_v4_scores_v3_final':'test', 'fnli_synthetic_examples_v4_scores_v3_final':'test'}

def conv(filename):
    with open('./data/csv/%s.csv' % filename, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            book = {
                'id': row['id'],
                'context': row['text1'],
                'statement': row['text2'],
                'label': row['label']
            }
            with open('./data/contexts/%s.json' % book['id'], 'w') as f:
                json.dump(book, f, sort_keys=True, indent=4)

def read_top_n(filename, n):
    # key = ['id','split','text1','text2','label','property','hop']
    key = []
    value = {}
    with open('./data/%s.csv' % filename, 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        lcount = 0
        for row in reader:
            if lcount == 0:
                key = row
            else:
                value[lcount] = row
            lcount += 1

    order = list(value.keys())
    random.shuffle(order)
    random.shuffle(order)
    with open('./data/top_%d_of_%s.csv' % (n, filename), 'w', newline='', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, key)
        writer.writeheader()
        # for k,v in sorted(value.items()):
        lcount = 0
        for k in order:
            if lcount >= n:
                break
            v = value[k]
            writer.writerow(v)
            lcount += 1

    return 'top_%d_of_%s' %(n, filename)

def isSplit(path, split):
    with open(path, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        # for sample in reader:
        #     if sample['split'] == split:
        #         return sample

        # samples = []
        # for sample in reader:
        #     if sample['split'] == split:
        #         samples.append(sample)
        # random.shuffle(samples)
        # return samples[0:2]
        cnt = 0
        for sample in reader:
            if sample['split'] == split:
                cnt += 1
                if cnt == 2:
                    return sample

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj][0]

def search_all_file(path, pair, n):
    all_files = []
    for data in pair.keys():
        all_files.extend(glob.glob(path+data+'/*.csv', recursive=True))
    random.shuffle(all_files)
    # print(all_files[:10])
    sampled_n = [['id','split','text1','text2','label','property','hop']]
    for f in all_files:
        if len(sampled_n) > n:
            break
        split = pair[f.split('/')[-2]]
        if isSplit(f, split):
            sampled_n.append(isSplit(f, split).values())
            # sampled_n.append(isSplit(f, split)[0].values())
            # if len(isSplit(f, split)) > 1:
            #     sampled_n.append(isSplit(f, split)[1].values())
            print('%d / %d' %(len(sampled_n), n))
    with open('./data/sampled_%d_of_%s.csv' % (n, namestr(pair,globals())), 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerows(sampled_n)

def main():
    # read_top_n('annot-effect-pair', 10) 
    # conv(read_top_n('annot-effect-pair', 1000))
    # search_all_file('../data/', train, 500)
    # search_all_file('../data/', val, 1000)
    # search_all_file('../data/', test, 2584)
    # conv('sampled_1000_of_train(all)')
    # conv('sampled_1000_of_val')
    # conv('sampled_8000_of_test')
    # conv('sampled_2584_of_mnli')
    conv('sampled_1246_of_mnli')

if __name__ == "__main__":
    main()