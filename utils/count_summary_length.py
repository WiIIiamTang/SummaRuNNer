import json


total_summary_length = 0
total_document_length = 0

total_summary_length_words = 0
total_document_length_words = 0

total_books = 0
with open("../data/test.json", "r") as fp:
    for line in fp.readlines():
        total_books += 1
        entry = json.loads(line)
        total_document_length += len(entry["doc"].split("\n"))
        total_summary_length += len(entry["summaries"].split("\n"))

        total_document_length_words += len(entry["doc"].split(" "))
        total_summary_length_words += len(entry["summaries"].split(" "))


print("Average summary length sentences: " + str(total_summary_length / total_books))
print("Average document length sentences: " + str(total_document_length / total_books))
print("Average summary length words: " + str(total_summary_length_words / total_books))
print("Average document length words: " + str(total_document_length_words / total_books))
