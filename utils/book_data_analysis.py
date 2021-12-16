"""
The goal of this script is to analyze the summaries we have received.

There are 5 sources where the summaries can come from: Bookwolf, cliffsnotes, gradesaver, novelguide and pinkmonkey
We have 90 books in total.

We wish to create a table with 90 rows representing the books and columns indicating information about the books.
"""

import os
import json
import pandas as pd
import pickle
import numpy as np


PICKLE_LOCATION = os.path.join(os.pardir, "example_datasets", "pks")

# Read Raw chapters and summaries
raw_texts_list = pickle.load(open(os.path.join(PICKLE_LOCATION, "raw_texts_cleaned.pk"), "rb"))
bookwolf = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_bookwolf_all.pk"), "rb"))
cliffsnotes = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_cliffsnotes.pk"), "rb"))
gradesaver = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_gradesaver.pk"), "rb"))
novelguide = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_novelguide.pk"), "rb"))
pinkmonkey = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_pinkmonkey_all.pk"), "rb"))

list_summaries = [bookwolf, cliffsnotes, gradesaver, novelguide, pinkmonkey]
string_summaries = ["Bookwolf", "Cliffsnotes", "Gradesaver", "Novelguide", "Pinkmonkey"]


def get_book_data():
    all_book_data = {}

    for book in raw_texts_list:
        all_book_data[book] = {"Number of Summaries": len(raw_texts_list[book]), "Total": 0}

    for index, summaries in enumerate(list_summaries):
        for book in summaries:
            if book.title not in all_book_data.keys():
                continue
            length = len(book.section_summaries)

            all_book_data[book.title][string_summaries[index]] = length
            all_book_data[book.title]["Total"] += length

    df = pd.DataFrame(all_book_data).transpose()
    df["Cliffsnotes"] = df["Cliffsnotes"].apply(lambda x: 0 if x == np.nan else x)

    for summary in string_summaries:
        df[summary] = df[summary].fillna(0)
        df[summary] = df[summary].apply(lambda x: int(x))

    df["Number of Summaries"] = df["Number of Summaries"].apply(lambda x: int(x))
    df["Total"] = df["Total"].apply(lambda x: int(x))
    df["Book"] = df.index
    df = df[["Book"] + [col for col in df.columns if col != "Book"]]
    return df, sum(df["Total"])


def clean_summary(summary):
    """
    This function will remove all books that are not in raw_texts_list from the summary.
    Args:
        summary:
        file_name:

    Returns:

    """
    pop_indexes = []
    for index, book in enumerate(summary):
        if book.title not in raw_texts_list.keys():
            pop_indexes.append(index)

    new_summary = []
    print(pop_indexes)
    for i in range(len(summary)):
        if i not in pop_indexes:
            new_summary.append(summary[i])

    return new_summary


def get_summary_data():
    all_summary_data = {}
    for index, summaries in enumerate(list_summaries):
        new_summary = clean_summary(summaries)
        num_summaries = 0
        for book in new_summary:
            num_summaries += len(book.section_summaries)

        all_summary_data[string_summaries[index]] = {"Number of Books": len(new_summary), "Number of Summaries": num_summaries,
                                                     "Average Number of Summaries per Book": num_summaries / len(new_summary)}

    df = pd.DataFrame(all_summary_data).transpose()
    for col in df:
        df[col] = df[col].apply(lambda x: int(x))
    df["Summary Source"] = df.index
    df = df[["Summary Source"] + [col for col in df.columns if col != "Summary Source"]]
    return df

def main():

    all_book_data, total_summaries = get_book_data()

    print("ALL BOOK DATA\n\n")
    print(all_book_data)
    print("\nTotal number of summaries: " + str(total_summaries))

    summary_data = get_summary_data()

    print(summary_data)

if __name__ == "__main__":
    main()

