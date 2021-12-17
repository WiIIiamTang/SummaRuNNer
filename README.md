# PyTorch SummaRuNNer
A modified version of hpzhao's work, which also includes [no-execution's extractive labeler](https://github.com/no-execution/Summa_label).

This repository is meant for experiments on new data. We provide tools to train and test on three new datasets.

To reproduce or verify results reported in our paper, [read this section](#new-datasets-to-test-on).



## Setup
After [downloading the labeled DailyMail data](https://drive.google.com/file/d/1JgsboIAs__r6XfCbkDWgmberXJw8FBWE/view?usp=sharing) and putting it in the ``data`` folder follow the steps:

### Requirements
1. Use Python 3.6 (it might work on other versions, but this was not tested)

2. 
```
pip3 install pipenv
python3 -m pipenv install
```
    
   - One of the requirements is PyTorch 0.3.1. This does not seem to work on Windows, but works on Linux distributions (and maybe Mac). See https://pytorch.org/get-started/previous-versions/

3. ``python3 -m pipenv shell``
    You should see something like
    ``((SummaRuNNer) ) user@PC:/mnt/c/Users/user$``
    at the prompt

### Run SummaRuNNer tests
4. Test without gpu: 
    ```
    python main.py -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt -topk 2
    ```

    Test with gpu: 

    ```
    python main.py -device 0 -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt -topk 2
    ```

    Results of predictions are stored in ``outputs/hyp`` while the "gold-standard" summaries are stored in ``outputs/ref``. The tests are done using the pretrained model provided by hpzhao.

### Install rouge
5. Point pyrouge to the rouge folder (in ``outputs``): 
    ```
    pyrouge_set_rouge_path absolute/path/to/ROUGE-1.5.5/
    ```

6.  **If you need Perl**,
    ```
    sudo apt-get install libxml-parser-perl
    ```


    You might also need to install pyrouge/rouge:
    ```
    pip install pyrouge rouge
    ```

7.  Install XML::DOM (Perl package):
    ```
    cpan install XML::DOM
    ``` 
    

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
python main.py -device 0 -batch_size 16 -model RNN_RNN -seed 1 -save_dir checkpoints/my_trained_model_RNNRNN_seed1.pt
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

When training on a new dataset, the sentences must all be labelled first. In the case of the DailyMail dataset provided here, it is already labeled so there is no need to run this.

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

**This section details the reproduction of results reported in our paper.**


### Reddit
- Reddit stories (raw): https://github.com/WiIIiamTang/summarunner-reddit-datasets

- RedditTLDR (already preprocessed): https://drive.google.com/drive/folders/1ytMH0dbmJb6HuTE9XmjPfY9CuaVOVl6a?usp=sharing

For preprocessing, note that we labeled these datasets but ended up not using these datasets for training.

 **Reddit Stories preprocessing**: Run ``utils/preprocess_reddit_stories.py``. You need to specify the correct directories for the **abstractive** summaries and labels. You must run the preprocess script **two times**. One time to obtain the test data, and another time to obtain the validation data.


**TLDR preprocessing**: **If you are using the original Webis TLDR 17 data**, then run ``utils/process_reddit_dataset.py`` on the json file. Then run the labeler on the output, as described in the [labeling](#labeler) section. You can test this on the example provided in ``example_datasets``. We recommend you just use the preprocessed test and validation sets in the link above.

---

### Books

Run the files as explained in https://github.com/manestay/novel-chapter-dataset. Once the pks files are scraped, put those files in example_datasets folder. 

From here you can run the script extract_summaries.py in utils.
This file can be edited if the location of the pks is not in the example_datasets.

The output of this script should produce the correct test.json test dataset file needed for SummaRuNNer.

From here we can run SummaRuNNer on the test.json file.

The folder book_experiments contains the scripts used to run the experiments presented in our paper.
The folder outputs/book_data/scripts contains the scripts used to run the ROUGE scores once the data from book_experiments script is received.

Finally the scores are stored and kept in the folder: outputs/book_data/scores. 

---

### Running our tests

Evalute ROUGE metrics by running ```outputs/eval.py [-b n]```

Where ``-b`` is the byte limit of the summaries. The true summaries must be in ``ref/``, and the model summaries must be in ``ref/``. Of course, before running the rouge script,  you have to generate the summaries for each dataset. Follow these steps to generate summaries:

#### RNN
For SummaRuNNer models, run ```main.py -test -batch_size 1 -model RNN_RNN -test_dir xxx -load_dir xxx -device 0 [-b n] [-topk n]```

Where ``-b`` is the byte limit of the summaries and ``-topk`` is the max number of sentences to take from the document for summarization. Set the test dir and load dir based on where your dataset and pretrained model is. For example, for 75 byte length limit, use ``-b 75``. For full length, **do not use the bytes setting** and use ``-topk`` instead. We used the best ``topk`` based on the validation set. Topk details:
- For all **Reddit** datasets, set ``topk`` to 3 when running  a full length test.

#### Baseline-LEAD-3
For **LEAD-3**, run ``lead3.py`` on each of the datasets.

#### Baseline-Random
For **Random**, run ``random_select.py`` on each of the datasets. You need to set the number of bytes or top sentences (``max_sent``) for this as well. 
- Set ``max_sent`` to 5 when testing on the Reddit Stories dataset, and 3 when testing on the RedditTLDR dataset.



---

### Running the training

SummaRuNNer trained with GloVe embeddings: https://drive.google.com/drive/folders/1ltTkUX01q713BcToCZl1K6y-JOEaKoBQ?usp=sharing

You must take the **100 dimensional embeddings** (``word2id100.json``, ``embedding100.npz``, ``RNN_RNN_seed_1_GloVe100.pt``).

To train yourself, download [these GloVe embeddings](https://nlp.stanford.edu/data/glove.6B.zip), and run ``preprocess.py -build_vocab`` on ``glove.6B.100d.txt`` to build the vocabulary. You need to have the embedding npz file and word2id json file before starting to train. Train with the command:

```
python main.py -train -device 0 -save_dir checkpoints/glovemodel.pt -embedding xxx -word2id xxx -batch_size 16 -seed 1
```
Set the embedding and word2id to the files you downloaded/created earlier. At the end of training, you will get a pretrained model in the ``checkpoints`` folder to use for testing (above).
