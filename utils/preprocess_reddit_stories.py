import json
import argparse
import os
from tqdm import tqdm
import glob

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=False, help='The RedditStories dataset path', default='inputs/test')
    parser.add_argument('-l', required=False, help='The RedditStories label path', default='ext_labels/test')
    parser.add_argument('-s', required=False, help='The RedditStories ground-truth summaries path', default='human-extracts/test')
    parser.add_argument('-o', required=False, help='The file to output the results to', default='RedditStories_output.json')

    args = parser.parse_args()
    data = []

    for (dirpath, dirnames, filenames) in os.walk(args.i):
        for filename in filenames:
            with open(os.path.join(dirpath, filename), 'r', encoding='utf-8') as f:
                d_doc = [json.loads(l) for l in f.readlines()][0]
                doc = ''.join([l.get('text') for l in d_doc.get('inputs')])
                
                with open(os.path.join(args.l, filename), 'r', encoding='utf-8') as flabel:
                    d_labels = [json.loads(l) for l in flabel.readlines()][0] 
                    labels = '\n'.join([str(n) for n in d_labels.get('labels')])
                
                summ_names = glob.glob(os.path.join(args.s, f'{".".join(filename.split(".")[:-1])}*.txt'))

                with open(summ_names[0], 'r', encoding='utf-8') as fsumm:
                    d_summ = fsumm.readlines()[0]
                    summs = d_summ
                
                data.append({
                    'doc': doc.replace('\n', '').replace('..', '').replace('...', '').replace('.', '\n').lower().strip('\n'),
                    'summaries': summs.replace('\n', '').replace('.', '\n').strip('\n').lower(),
                    'labels': labels
                })

    with open(args.o, 'w', encoding='utf-8') as f:
        for d in data:
            json.dump(d, f)
            f.write('\n')

if __name__ == '__main__':
    main()