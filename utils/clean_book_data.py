"""
The purpose of this script is to:

1.) Only keep books that have the correct format
Incorrect format included things like BOOK 1: Chapter 1. or PART 1: Chapter 1 or Sieve 1...

2.) Remove all summaries of books that were removed.


Note that raw_texts_cleaned.pk was produced by removing entries that did not conform to correct syntax in raw_texts.pk.
The number of books reduced from 90 to 64. This is ok since this will include plenty of summaries to test on.
"""

import os
import json
import pandas as pd
import pickle
import numpy as np


PICKLE_LOCATION = os.path.join(os.pardir, "example_datasets", "pks_original")

# Read Raw chapters and summaries
raw_texts_list = pickle.load(open(os.path.join(PICKLE_LOCATION, "raw_texts.pk"), "rb"))
bookwolf = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_bookwolf_all.pk"), "rb"))
cliffsnotes = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_cliffsnotes.pk"), "rb"))
gradesaver = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_gradesaver.pk"), "rb"))
novelguide = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_novelguide.pk"), "rb"))
pinkmonkey = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_pinkmonkey_all.pk"), "rb"))

summary_list = [bookwolf, cliffsnotes, gradesaver, novelguide, pinkmonkey]
new_summary_name = ["bookwolf.pk", "cliffsnotes.pk", "gradesaver.pk", "novelguide.pk", "pinkmonkey.pk"]

def remove_bad_syntax():
    """
    Will remove all books that don't have the correct syntax for our scripts.
    Returns:

    """
    remove_items = []

    for key, book_dict in raw_texts_list.items():
        for chapter_key, summary in book_dict.items():
            if ":" in chapter_key:
                remove_items.append(key)
                continue

    for item in remove_items:
        raw_texts_list.pop(remove_items)

    pickle.load(raw_texts_list, open("./raw_texts_cleaned.pk", "wb"))


def clean_summary(summary, file_name):
    pop_indexes = []
    for index, book in enumerate(summary):
        if book.title not in raw_texts_list.keys():
            pop_indexes.append(index)

    new_summary = []
    print(file_name)
    print(pop_indexes)
    for i in range(len(summary)):
        if i not in pop_indexes:
            new_summary.append(summary[i])

    pickle.dump(new_summary, open(file_name, "wb"))

def clean_summaries():
    for index, s in enumerate(summary_list):
        clean_summary(s, new_summary_name[index])

def main():
    #remove_bad_syntax()
    clean_summaries()


if __name__ == "__main__":
    main()