import os, sys 
import argparse
import json
'''
The script accepts an input that has one json object per line.
Each JSON object should have a `"doc"` and `"summaries"` key.
The sentences must be separated by new lines (`\n`).
See the example input and output in ``extractive_labeler``.

{
 doc: "the document text",
 summaries: "the document summary"
 }

doc -> a paragraph in the related work section of a paper Q
summaries -> concatenated abstract from paper Q, and abstracts from reference documents 
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    with open(args.input, 'r', encoding = 'utf-8') as fh:
        root = json.load(fh)

    data = []
    # end of sentence punctuation
    eos = ['. ', '? ', '! ']
    for i, item in enumerate(root):
        cleaned = {'doc': '', 'summaries': ''}
        cleaned['doc'] = root[i]['related_work']
        cleaned['summaries'] = root[i]['abstract'] + " "
        for ref in root[i]['ref_abstract']:
            for ab in root[i]['ref_abstract'][ref]:
                cleaned['summaries'] == root[i]['ref_abstract'][ref]['abstract']
        for j in eos:
            cleaned['doc'] = cleaned['doc'].replace(j, '\n')
            cleaned['summaries'] = cleaned['summaries'].replace(j, '\n')
        data.append(cleaned)
            
    with open(args.output, 'w', encoding='utf-8') as f:
        for d in data:
            json.dump(d, f)
            f.write('\n')

if __name__ == "__main__":
    main()
