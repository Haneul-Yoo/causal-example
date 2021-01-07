import csv
import random
import json
import os
import glob

def conv(filename):
    with open('./data/%s.csv' % filename, 'r', encoding='UTF-8') as csvfile:
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
        sample = next(reader)
        if sample['split'] == split:
            # print(sample)
            return sample

def search_all_file(path, split, n):
    all_files = glob.glob(path+'**/*.csv', recursive=True)
    random.shuffle(all_files)
    sampled_n = [['id','split','text1','text2','label','property','hop']]
    for f in all_files:
        if len(sampled_n) > n:
            break
        if isSplit(f, split):
            sampled_n.append(isSplit(f, split).values())
    with open('./data/sampled_%d_of_all_files.csv' %n, 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerows(sampled_n)


def main():
    # read_top_n('annot-effect-pair', 10) 
    # conv(read_top_n('annot-effect-pair', 1000))
    # search_all_file('../data/', 'test', 100)
    conv('sampled_100_of_all_files')

if __name__ == "__main__":
    main()