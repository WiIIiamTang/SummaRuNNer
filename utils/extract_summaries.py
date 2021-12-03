"""
Goal is to create JSON data with keys: ["doc", "labels", "summaries"] for every chapter / chapter summary
for every book obtained from [1].

[1] : https://github.com/manestay/novel-chapter-dataset

Once the bash script from [1] is run, it will create the folder pks.

The contents of the pks:

gutenberg_catalog.pk        -----> Stores data (author, id, book format and url to retrieve book)
                                of 127 books from the Guttenberg project
gutenberg_catalog_raw.pk    -----> Stores data of 98 books from the Guttenberg project
                                    (IM ASSUMING THESE ARE THE 98 BOOKS [1] FINDS SUMMARIES FOR)
raw_texts.pk                -----> stores the actual books (71 MB) : we have 90 books scraped
summaries_x.pk              -----> stores the summaries for certain books from source x
summaries_x_all.pk          -----> stores the summaries for certain books from source x with extra
                                    content such as epilogue and other book name (if book is split into smaller ones)

We will use raw_texts.pk to find the chapter text and summaries_x.pk to get the summaries.
Note that the objects stored in the pk files (for summaries) are list of BookSummary objects.

Lets start by exporting one chapter as correct JSON.
"""

import pandas as pd
import pickle
import json
import os


# Global variables
PICKLE_LOCATION = os.path.join(os.pardir, "example_datasets", "pks")
NUM_BOOKS = "all"
MAX_NUM_CHAPTERS_PER_BOOK = 5

# Read Raw chapters and summaries
raw_texts_list = pickle.load(open(os.path.join(PICKLE_LOCATION, "raw_texts_cleaned.pk"), "rb"))
bookwolf = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_bookwolf_all.pk"), "rb"))
cliffsnotes = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_cliffsnotes.pk"), "rb"))
gradesaver = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_gradesaver.pk"), "rb"))
novelguide = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_novelguide.pk"), "rb"))
pinkmonkey = pickle.load(open(os.path.join(PICKLE_LOCATION, "summaries_pinkmonkey_all.pk"), "rb"))

source_summaries = [bookwolf, cliffsnotes, gradesaver, novelguide, pinkmonkey]
output_jsons = []


def clean_summary(summary, file_name):
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
    print(file_name)
    print(pop_indexes)
    for i in range(len(summary)):
        if i not in pop_indexes:
            new_summary.append(summary[i])

    return new_summary


def extract_one_summary(chapter_summary):
    """
    This method will extract the summary and list of chapters present in "chapter_summary"
    Args:
        chapter_summary:

    Returns:
        Array where first element is a list of chapters in the summary, second element is string of the summary.
    """

    chapters, summary_list = chapter_summary
    summary_string = ' '.join(summary_list)

    # We assume chapters is a string of form either: Chapter x or Chapter x - y , where x and y are both ints
    chapter_list = chapters.split(" ")
    chapter_list = [int(c) for c in chapter_list if c.isdigit()]
    if len(chapter_list) > 1:
        chapter_list = list(range(chapter_list[0], chapter_list[1] + 1))

    return chapter_list, summary_string


def extract_all_summaries(summary_soure, data_list_json):
    for book_summary in summary_soure:

        # if len(output_jsons) > 9:
        #     break

        book_title = book_summary.title
        # skip if the book was removed during cleaning.
        if book_title not in raw_texts_list.keys():
            continue

        for chapter_summary in book_summary.section_summaries:
            # Get summary and list of chapters in that summary
            list_chapters, summary = extract_one_summary(chapter_summary)

            # Get actual chapter(s) text
            actual_chapter = ""
            for chapter in list_chapters:
                try:
                    actual_chapter += "\n".join(raw_texts_list[book_title]["Chapter " + str(chapter)])
                except KeyError:
                    print("h")
            if actual_chapter != "":
                output_json = {}
                output_json["doc"] = actual_chapter
                output_json["labels"] = "1\n1\n1\n0\n1\n0\n0\n0\n1\n0\n0\n0\n0"
                output_json["summaries"] = summary

                data_list_json.append(output_json)


def main():

    for source in source_summaries:
        extract_all_summaries(source, output_jsons)

    # Will remove all ones that do not have \n character. This is needed in the script
    output_jsons2 = [x for x in output_jsons if "\n" in x["doc"]]

    with open("./test.json", "w") as fp:
        for j in output_jsons2:
            json.dump(j, fp)
            fp.write("\n")


if __name__ == "__main__":
    main()
