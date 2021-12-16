cd ..
echo $PWD

echo "75"
echo 
echo 
mkdir outputs/ref_75
mkdir outputs/hyp_75
python main.py -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt -test_dir data/test.json -ref outputs/ref_75 -hyp outputs/hyp_75 -b 75


echo "275"
echo 
echo
mkdir outputs/ref_275
mkdir outputs/hyp_275
python main.py -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt -test_dir data/test.json -ref outputs/ref_275 -hyp outputs/hyp_275 -b 275



echo "Top 15"
echo
echo
mkdir outputs/ref_top_15
mkdir outputs/hyp_top_15
python main.py -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt -test_dir data/test.json -ref outputs/ref_top_15 -hyp outputs/hyp_top_15 -topk 15



echo "Top 20"
echo 
echo
mkdir outputs/ref_top_20
mkdir outputs/hyp_top_20
python main.py -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt -test_dir data/test.json -ref outputs/ref_top_20 -hyp outputs/hyp_top_20 -topk 20



echo "Top 25"
echo echo
mkdir outputs/ref_top_25
mkdir outputs/hyp_top_25
python main.py -batch_size 1 -test -load_dir checkpoints/RNN_RNN_seed_1.pt -test_dir data/test.json -ref outputs/ref_top_25 -hyp outputs/hyp_top_25 -topk 25

