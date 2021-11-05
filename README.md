# PyTorch SummaRuNNer
A fork of hpzhao's work, which includes [no-execution's extractive labeler](https://github.com/no-execution/Summa_label).

## Test to see if installation is correct
Tested on Ubuntu 18.04 (WSL2) without CUDA.  After [downloading the sample data](https://drive.google.com/file/d/1JgsboIAs__r6XfCbkDWgmberXJw8FBWE/view?usp=sharing) and putting it in the ``data`` folder,

### Setup
1. Use Python 3.6

2. ``pipenv install``
    - One of the requirements is PyTorch 0.3.1. This does not seem to work on Windows, but seems to work on Linux distributions (and maybe Mac). See https://pytorch.org/get-started/previous-versions/

3. ``pipenv shell``
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
5. Point pyrouge to the rouge folder: 
    ```
    pyrouge_set_rouge_path absolute/path/to/ROUGE-1.5.5/
    ```

6. 
    ```
    sudo apt-get install libxml-parser-perl
    ```
    Or the equivalent on Mac (to install Perl).


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
    1 ROUGE-1 Average_R: 0.24484 (95%-conf.int. 0.24127 - 0.24854)
    1 ROUGE-1 Average_P: 0.24440 (95%-conf.int. 0.24075 - 0.24827)
    1 ROUGE-1 Average_F: 0.24361 (95%-conf.int. 0.24004 - 0.24732)
    ---------------------------------------------
    1 ROUGE-2 Average_R: 0.10173 (95%-conf.int. 0.09852 - 0.10494)
    1 ROUGE-2 Average_P: 0.10192 (95%-conf.int. 0.09872 - 0.10513)
    1 ROUGE-2 Average_F: 0.10144 (95%-conf.int. 0.09822 - 0.10464)
    ---------------------------------------------
    1 ROUGE-L Average_R: 0.12879 (95%-conf.int. 0.12597 - 0.13180)
    1 ROUGE-L Average_P: 0.22632 (95%-conf.int. 0.22294 - 0.22988)
    1 ROUGE-L Average_F: 0.15230 (95%-conf.int. 0.14940 - 0.15517)
    ```

    Run with the above setup, the results are 1-2 points lower than the reported values in the original paper.


## Training

```
python main.py -device 0 -batch_size 32 -model RNN_RNN -seed 1 -save_dir checkpoints/my_trained_model_RNNRNN_seed1.pt
```
### Data format
Training, validation, test data are json objects:
```json
{
    doc: "the document text",
    labels: "1\n0\n1\n1\n01\n...",
    summaries: "the document summary"
}
```
The sentences of ``doc`` are separated by `\n`. The labels correspond to either keeping the corresponding sentence in (1) or out (0) for extractive summary training. The summaries also have sentences separated by `\n`.

The training process also requires word embeddings and a vocabulary built from the embeddings.

### Labeler
The heuristic algorithm for labeling sentences for extractive training is in ``extractive_labeler``. Although it seems like a faithful implementation of the paper's greedy algorithm, it does not always give the same result as hpzhao's labeled dataset.

When training on a new dataset, the sentences must all be labelled first.

### Word embeddings
The data has 100-dimensional word2vec embeddings that are already trained on the CNN/Daily Mail corpus. If the embeddings change you might need to rebuild the vocabulary (``preprocess.py``).
