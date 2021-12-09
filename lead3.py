import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-test_dir',type=str,default='data/test.json')
    parser.add_argument('-ref',type=str,default='outputs/ref')
    parser.add_argument('-hyp',type=str,default='outputs/hyp')
    args = parser.parse_args()

    with open(args.test_dir, 'r', encoding='utf-8') as f:
        data = [json.loads(l) for l in f.readlines()]
    
    hyp = [doc['doc'].split('\n')[:3] for doc in data]
    ref = [doc['summaries'] for doc in data]

    for i, hyp_i in enumerate(hyp):
        with open(os.path.join(args.ref,str(i+1)+'.txt'), 'w') as f:
                f.write(ref[i])
        with open(os.path.join(args.hyp,str(i+1)+'.txt'), 'w') as f:
            f.write('\n'.join(hyp_i))

if __name__ == '__main__':
    main()