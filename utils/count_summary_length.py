import json


total_summary_length = 0
total_document_length = 0

total_summary_length_chars = 0
total_document_length_chars = 0

total_books = 0
with open("../data/test.json", "r") as fp:
    for line in fp.readlines():
        total_books += 1
        entry = json.loads(line)
        total_document_length += len(entry["doc"].split("\n"))
        total_summary_length+= len(entry["summaries"].split("\n"))

        total_document_length_chars += len(entry["doc"])
        total_summary_length_chars += len(entry["summaries"])

print("Average summary length: " + str(total_summary_length / total_books))
print("Average doument length: " + str(total_document_length / total_books))
print("Average summary length chars: " + str(total_summary_length_chars / total_books))
print("Average doument length chars: " + str(total_document_length_chars / total_books))
