from tqdm import tqdm
import json
import argparse
from rouge import Rouge
import nltk
import sys

sys.setrecursionlimit(9999*9999)

def label_data(data: dict, rouge: Rouge) -> dict:
    doc = data['doc']
    summaries = data['summaries']
    sents = [sent.strip().strip('\n') for sent in doc.split('\n') if sent not in (' ', '.', '')]
    sents = [s for s in sents if s]
    labels = [0] * len(sents)
    rouge_group = []
    score_mid, max_idx = 0, 0

    for i,sent_i in enumerate(sents):
        try:
            score = rouge.get_scores(sents[i],summaries.replace('\n', '.'))[0]['rouge-1']['f']
        except Exception as e:
            print(i)
            print('sent_i:',sent_i)
            print('sents:',sents)
            print(sents[max(0, i-1)])
            print('summarize:',summaries)
            print(e)
            continue
            #return sents
        if score > score_mid:
            score_mid = score
            max_idx = i
    rouge_group.append(sents[max_idx])
    labels[max_idx] = 1

    score_max = score_mid
    for j,sent_j in enumerate(sents):
        if j == max_idx:
            continue
        try:
            score = rouge.get_scores(' '.join(rouge_group+[sent_j]),summaries.replace('\n', '.'))[0]['rouge-1']['f']
        except Exception as e:
            print(e)
        if score > score_max:
            labels[j] = 1
            rouge_group.append(sent_j)
            score_max = score
        
    data['labels'] = '\n'.join([str(x) for x in labels])
    data['doc'] = '\n'.join(sents)

    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='Path to json file of documents to label')
    parser.add_argument('-o', required=True, help='The path to write the output to')

    args = parser.parse_args()

    with open(args.i, 'r', encoding='utf-8') as f:
        data = [json.loads(l) for l in f.readlines()]
    
    r = Rouge()

    result = [label_data(d, r) for d in tqdm(data)]

    with open(args.o, 'w', encoding='utf-8') as f:
        for d in result:
            json.dump(d, f)
            f.write('\n')

if __name__ == '__main__':
    main()