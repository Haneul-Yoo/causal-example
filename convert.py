import csv
import random
import json

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
            elif lcount > n:
                break
            else:
                value[lcount] = row
            lcount += 1

    with open('./data/top_%d_of_%s.csv' % (n, filename), 'w', newline='', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, key)
        writer.writeheader()
        for k,v in sorted(value.items()):
            writer.writerow(v)

    return 'top_%d_of_%s' %(n, filename)

def main():
    # read_top_n('annot-effect-pair', 10) 
    # conv(read_top_n('annot-effect-pair', 1000))
    conv('20201210_215913_ForkPoolWorker-1') 

if __name__ == "__main__":
    main()