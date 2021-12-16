# PyTorch SummaRuNNer
A fork of hpzhao's work, which includes [no-execution's extractive labeler](https://github.com/no-execution/Summa_label).

## Test to see if installation is correct
Tested on Ubuntu 18.04 (WSL2) without CUDA.  After [downloading the sample data](https://drive.google.com/file/d/1JgsboIAs__r6XfCbkDWgmberXJw8FBWE/view?usp=sharing) and putting it in the ``data`` folder,

### Setup
1. Use Python 3.6

2. ``python3 -m pipenv install``
    - One of the requirements is PyTorch 0.3.1. This does not seem to work on Windows, but seems to work on Linux distributions (and maybe Mac). See https://pytorch.org/get-started/previous-versions/

3. ``python3 -m pipenv shell``
    You should see something like
    ``((SummaRuNNer) ) user@PC:/mnt/c/Users/user$``
    at the prompt

### Run SummaRuNNer
4. Test without gpu: 
    ```
    python main.py -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt
    ```

    Test with gpu: 

    ```
    python main.py -device 0 -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt
    ```

    Results of predictions are stored in ``outputs/hyp`` while the "gold-standard" summaries are stored in ``outputs/ref``.

### Install rouge
5. Point pyrouge to the rouge folder (in ``outputs``): 
    ```
    pyrouge_set_rouge_path absolute/path/to/ROUGE-1.5.5/
    ```

6.  If you need Perl,
    ```
    sudo apt-get install libxml-parser-perl
    ```
    Or the equivalent on other OS.


    You might also need to install pyrouge/rouge:
    ```
    pip install pyrouge rouge
    ```

7. 
    ```
    cpan install XML::DOM
    ``` 
    to install XML::DOM (Perl package).

8. Go into ``outputs/ROUGE-1.5.5/data``, then

    ```
    rm WordNet-2.0.exc.db

    ./WordNet-2.0-Exceptions/buildExeptionDB.pl ./WordNet-2.0-Exceptions ./smart_common_words.txt ./WordNet-2.0.exc.db
    ```

9. Evaluate rouge scores: 
    ```
    cd outputs
    python eval.py
    ```

    The output should correspond to something similar to Table 1 of the SummaRuNNer paper (the last row).

    ```
    ---------------------------------------------
    1 ROUGE-1 Average_R: 0.26252 (95%-conf.int. 0.25844 - 0.26658)
    1 ROUGE-1 Average_P: 0.26497 (95%-conf.int. 0.26087 - 0.26889)
    1 ROUGE-1 Average_F: 0.26268 (95%-conf.int. 0.25861 - 0.26666)
    ---------------------------------------------
    1 ROUGE-2 Average_R: 0.11812 (95%-conf.int. 0.11451 - 0.12158)
    1 ROUGE-2 Average_P: 0.11944 (95%-conf.int. 0.11583 - 0.12298)
    1 ROUGE-2 Average_F: 0.11835 (95%-conf.int. 0.11476 - 0.12175)
    ---------------------------------------------
    1 ROUGE-L Average_R: 0.14039 (95%-conf.int. 0.13719 - 0.14368)
    1 ROUGE-L Average_P: 0.24687 (95%-conf.int. 0.24291 - 0.25078)
    1 ROUGE-L Average_F: 0.16613 (95%-conf.int. 0.16295 - 0.16942)
    ```

    Run with the above setup, the results are similar to the reported values of the original paper.


## Training

```
python main.py -device 0 -batch_size 32 -model RNN_RNN -seed 1 -save_dir checkpoints/my_trained_model_RNNRNN_seed1.pt
```
### Data format
Training, validation, test data are json objects:
```
{
    doc: "the document text",
    labels: "1\n0\n1\n1\n01\n...",
    summaries: "the document summary"
}
```
The sentences of ``doc`` are separated by `\n`. The labels correspond to either keeping the corresponding sentence in (1) or out (0) for extractive summary training. The summaries also have sentences separated by `\n`.

The training process also requires word embeddings and a vocabulary built from the embeddings.

### Word embeddings
The data has 100-dimensional word2vec embeddings that are already trained on the CNN/Daily Mail corpus. If the embeddings change you might need to rebuild the vocabulary (``preprocess.py``).


## Labeler
The heuristic algorithm for labeling sentences for extractive training is in ``extractive_labeler``. Although it seems like a faithful implementation of the paper's greedy algorithm, it does not always give the same result as hpzhao's labeled dataset.

When training on a new dataset, the sentences must all be labelled first.

### Usage
```
usage: new_heuristic_labeler.py [-h] -i I -o O

optional arguments:
  -h, --help  show this help message and exit
  -i I        Path to json file of documents to label
  -o O        The path to write the output to
```

The script accepts an input that has one json object per line. Each json object should have a `"doc"` and `"summaries"` key. The sentences must be separated by new lines (`\n`). See the example input and output in ``extractive_labeler``.

### Setting up new datasets for testing or training
- Run some preprocessing script to get the correct format with "doc" and "summaries" (such as ``utils/process_reddit_dataset.py``)
- Run the labeler
- Name the output `test.json`, `train.json`, or `val.json`

## New datasets to test on

### Reddit
For ready-to-test datasets:
https://github.com/WiIIiamTang/summarunner-reddit-datasets

Or, process them manually:

#### TLDR 17 preprocessing

```
python utils/process_reddit_dataset.py -i example_datasets/example_redditTLDR.json -o data/example_redditTLDR_out.json

python extractive_labeler/new_heuristic_labeler.py -i data/example_redditTLDR_out.json -o data/reddit_labelled.json

python main.py -device 0 -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt -test_dir data/reddit_labelled.json
```
### Books

Run the files as explained in https://github.com/manestay/novel-chapter-dataset. Once the pks files are scraped, put those files in example_datasets folder. 

From here you can run the script extract_summaries.py in utils.
This file can be edited if the location of the pks is not in the example_datasets.

The output of this script should produce the correct test.json test dataset file needed for SummaRuNNer.

From here we can run SummaRuNNer on the test.json file.

The folder book_experiments contains the scripts used to run the experiments presented in our paper.
The folder outputs/book_data/scripts contains the scripts used to run the ROUGE scores once the data from book_experiments script is received.

Finally the scores are stored and kept in the folder: outputs/book_data/scores.
