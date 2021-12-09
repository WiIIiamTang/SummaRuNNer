#!/usr/bin/env python3

import os
import argparse
from pyrouge import Rouge155

def remove_broken_files():
    error_id = []
    for f in os.listdir('ref'):
        try:
            open('ref/' + f).read()
        except:
            error_id.append(f)
    for f in os.listdir('hyp'):
        try:
            open('hyp/' + f).read()
        except:
            error_id.append(f)
    error_set = set(error_id)
    for f in error_set:
        os.remove('ref/' + f)
        os.remove('hyp/' + f)

def rouge(**kwargs):
    r = Rouge155()
    r.home_dir = '.'
    r.system_dir = 'hyp'
    r.model_dir =  'ref'

    r.system_filename_pattern = '(\d+).txt'
    r.model_filename_pattern = '#ID#.txt'

    command = f'-e ROUGE-1.5.5/data -a -c 95 -m -n 2 {"-b " + str(kwargs.get("bytes")) if kwargs.get("bytes") else ""}'
    output = r.convert_and_evaluate(rouge_args=command)
    print(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', default=0, type=int)
    args = parser.parse_args()
    remove_broken_files()
    rouge(bytes=args.b)
