import argparse
import json
import os
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-test_dir',type=str,default='data/test.json')
    parser.add_argument('-ref',type=str,default='outputs/ref')
    parser.add_argument('-hyp',type=str,default='outputs/hyp')
    parser.add_argument('-b', type=int, help='byte cutoff', default=0)
    parser.add_argument('-max_sent', type=int, default=4)
    args = parser.parse_args()

    with open(args.test_dir, 'r', encoding='utf-8') as f:
        data = [json.loads(l) for l in f.readlines()]
    
    hyp = [doc['doc'].split('\n') for doc in data]

    for i, hypo in enumerate(hyp):
        limit = args.b if args.b else 9999999
        all_sentences = hypo
        hypo = []
        for _ in range(args.max_sent):
            if len(all_sentences) > 1:
                select = all_sentences.pop(random.randint(0, len(all_sentences)-1))
            else:
                select = all_sentences.pop(0)
            hypo.append(select)
            limit -= len(select.encode('utf-8'))
            if limit <= 0 or not all_sentences:
                break
        
        hyp[i] = hypo

    ref = [doc['summaries'] for doc in data]

    for i, hyp_i in enumerate(hyp):
        with open(os.path.join(args.ref,str(i+1)+'.txt'), 'w') as f:
                f.write(ref[i])
        with open(os.path.join(args.hyp,str(i+1)+'.txt'), 'w') as f:
            f.write('\n'.join(hyp_i))

if __name__ == '__main__':
    main()
