#!/usr/bin/env python3

import os
import argparse
from pyrouge import Rouge155

def remove_broken_files(ref_file_path, hyp_file_path):
    error_id = []
    for f in os.listdir(ref_file_path):
        try:
            open(ref_file_path + f).read()
        except:
            error_id.append(f)
    for f in os.listdir(hyp_file_path):
        try:
            open(hyp_file_path + f).read()
        except:
            error_id.append(f)
    error_set = set(error_id)
    for f in error_set:
        os.remove(ref_file_path + f)
        os.remove(hyp_file_path + f)

def rouge(**kwargs):
    r = Rouge155()
    r.home_dir = '.'
    r.system_dir = kwargs.get("hyp")
    r.model_dir =  kwargs.get("ref")

    r.system_filename_pattern = '(\d+).txt'
    r.model_filename_pattern = '#ID#.txt'

    command = f'-e ROUGE-1.5.5/data -a -c 95 -m -n 2 {"-b " + str(kwargs.get("bytes")) if kwargs.get("bytes") else ""}'
    output = r.convert_and_evaluate(rouge_args=command)
    print(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', default=0, type=int)
    parser.add_argument('-ref', default='ref/', type=str)
    parser.add_argument('-hyp', default='hyp/', type=str)
    args = parser.parse_args()
    remove_broken_files(args.ref, args.hyp)
    rouge(bytes=args.b, hyp=args.hyp, ref=args.ref)
