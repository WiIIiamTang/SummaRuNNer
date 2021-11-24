import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='The WebisTLDR17 dataset path')
    parser.add_argument('-o', required=True, help='The file to output the results to')

    args = parser.parse_args()

    with open(args.i, 'r', encoding='utf-8') as f:
        data = [json.loads(l) for l in f.readlines()]
    
    results = []

    for d in data:
        results.append({
            'doc': d.get('content'),
            'summaries': d.get('summary')
        })
    
    with open(args.o, 'w', encoding='utf-8') as f:
        for d in results:
            json.dump(d, f)
            f.write('\n')

if __name__ == '__main__':
    main()