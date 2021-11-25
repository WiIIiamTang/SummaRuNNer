from rouge import Rouge
import os
import json


# Global Vars
rouge = Rouge()

OUTPUT_FOLDER = os.path.join(os.getcwd(), "hyp")
REFERENCE_FOLDER = os.path.join(os.getcwd(), "ref")


def main():
    rouge1_scores = {'recall': 0, 'precision': 0, "f1-score": 0}
    rouge2_scores = {'recall': 0, 'precision': 0, "f1-score": 0}
    rougel_scores = {'recall': 0, 'precision': 0, "f1-score": 0}

    total_files = 0
    thousand_count = 0

    for file_name in os.listdir(OUTPUT_FOLDER):

        output_file = open(os.path.join(OUTPUT_FOLDER, file_name))
        output_text = output_file.read()
        output_file.close()

        reference_file = open(os.path.join(REFERENCE_FOLDER, file_name))
        reference_text = reference_file.read()
        reference_file.close()

        try:
            score = rouge.get_scores(output_text, reference_text)
        except ValueError:
            print(file_name)
            continue

        rouge1_scores["recall"] += score[0]["rouge-1"]["r"]
        rouge1_scores["precision"] += score[0]["rouge-1"]["p"]
        rouge1_scores["f1-score"] += score[0]["rouge-1"]["f"]

        rouge2_scores["recall"] += score[0]["rouge-1"]["r"]
        rouge2_scores["precision"] += score[0]["rouge-1"]["p"]
        rouge2_scores["f1-score"] += score[0]["rouge-1"]["f"]

        rougel_scores["recall"] += score[0]["rouge-l"]["r"]
        rougel_scores["precision"] += score[0]["rouge-l"]["p"]
        rougel_scores["f1-score"] += score[0]["rouge-l"]["f"]

        total_files += 1

        if total_files % 1000 == 0:
            thousand_count += 1
            print("Read: " + str(1000*thousand_count) + " files")


    rouge1_scores = {key: value / total_files for key, value in rouge1_scores.items()}
    rouge2_scores = {key: value / total_files for key, value in rouge2_scores.items()}
    rougel_scores = {key: value / total_files for key, value in rougel_scores.items()}

    print("ROUGE 1 scores: ")
    print(json.dumps(rouge1_scores, indent=4))
    print("\n")
    print("ROUGE 2 scores: ")
    print(json.dumps(rouge2_scores, indent=4))
    print("\n")
    print("ROUGE L scores: ")
    print(json.dumps(rougel_scores, indent=4))


if __name__ == "__main__":
    main()