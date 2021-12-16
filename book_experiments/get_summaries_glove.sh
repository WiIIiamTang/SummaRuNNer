cd ..
echo $PWD

path_to_glove="summarunner-glove"
path_to_data="outputs/book_data/data/sumaG"

echo "75"
echo 
echo 
mkdir ${path_to_data}/ref_75
mkdir ${path_to_data}/hyp_75
python main.py -batch_size 1 -test -load_dir ${path_to_glove}/RNN_RNN_seed_1_GloVe100.pt -word2id ${path_to_glove}/word2id100.json -embedding ${path_to_glove}/embedding100.npz -test_dir data/test.json -ref ${path_to_data}/ref_75 -hyp ${path_to_data}/hyp_75 -b 75


echo "275"
echo 
echo
mkdir ${path_to_data}/ref_275
mkdir ${path_to_data}/hyp_275
python main.py -batch_size 1 -test -load_dir ${path_to_glove}/RNN_RNN_seed_1_GloVe100.pt -word2id ${path_to_glove}/word2id100.json -embedding ${path_to_glove}/embedding100.npz -test_dir data/test.json -ref ${path_to_data}/ref_275 -hyp ${path_to_data}/hyp_275 -b 275

echo "Top 15"
echo
echo
mkdir ${path_to_data}/ref_top_15
mkdir ${path_to_data}/hyp_top_15
python main.py -batch_size 1 -test -load_dir ${path_to_glove}/RNN_RNN_seed_1_GloVe100.pt -word2id ${path_to_glove}/word2id100.json -embedding ${path_to_glove}/embedding100.npz -test_dir data/test.json -ref ${path_to_data}/ref_top_15 -hyp ${path_to_data}/hyp_top_15 -topk 15


echo "Top 20"
echo 
echo
mkdir ${path_to_data}/ref_top_20
mkdir ${path_to_data}/hyp_top_20
python main.py -batch_size 1 -test -load_dir ${path_to_glove}/RNN_RNN_seed_1_GloVe100.pt -word2id ${path_to_glove}/word2id100.json -embedding ${path_to_glove}/embedding100.npz -test_dir data/test.json -ref ${path_to_data}/ref_top_20 -hyp ${path_to_data}/hyp_top_20 -topk 20


echo "Top 25"
echo echo
mkdir ${path_to_data}/ref_top_25
mkdir ${path_to_data}/hyp_top_25
python main.py -batch_size 1 -test -load_dir ${path_to_glove}/RNN_RNN_seed_1_GloVe100.pt -word2id ${path_to_glove}/word2id100.json -embedding ${path_to_glove}/embedding100.npz -test_dir data/test.json -ref ${path_to_data}/ref_top_25 -hyp ${path_to_data}/hyp_top_25 -topk 25

