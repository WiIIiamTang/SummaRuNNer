import argparse
import json
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='The WebisTLDR17 dataset path')
    parser.add_argument('-o', required=True, help='The file to output the results to')

    args = parser.parse_args()

    with open(args.i, 'r', encoding='utf-8') as f:
        data = [json.loads(l) for l in f.readlines()]
    
    results = []

    for d in tqdm(data):
        results.append({
            'doc': d.get('content').replace('\n', '').replace('..', '').replace('...', '').replace('.', '\n').lower().strip('\n'),
            'summaries': d.get('summary').replace('\n', '').replace('.', '\n').strip('\n').lower()
        })
    
    with open(args.o, 'w', encoding='utf-8') as f:
        for d in results:
            json.dump(d, f)
            f.write('\n')

if __name__ == '__main__':
    main()