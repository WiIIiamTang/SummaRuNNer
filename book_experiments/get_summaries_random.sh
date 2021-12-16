#cd ..
#echo $PWD

echo "75"
echo 
echo 
mkdir ../outputs/book_data/data/random/ref_rand_75
mkdir ../outputs/book_data/data/random/hyp_rand_75
python ../random_select.py -test_dir ../data/test.json -ref ../outputs/book_data/data/random/ref_rand_75 -hyp ../outputs/book_data/data/random/hyp_rand_75 -b 75


echo "275"
echo 
echo
mkdir ../outputs/book_data/data/random/ref_rand_275
mkdir ../outputs/book_data/data/random/hyp_rand_275
python ../random_select.py -test_dir ../data/test.json -ref ../outputs/book_data/data/random/ref_rand_275 -hyp ../outputs/book_data/data/random/hyp_rand_275 -b 275


echo "Top 15"
echo
echo
mkdir ../outputs/book_data/data/random/ref_rand_top_15
mkdir ../outputs/book_data/data/random/hyp_rand_top_15
python ../random_select.py -test_dir ../data/test.json -ref ../outputs/book_data/data/random/ref_rand_top_15 -hyp ../outputs/book_data/data/random/hyp_rand_top_15 -max_sent 15


echo "Top 20"
echo 
echo
mkdir ../outputs/book_data/data/random/ref_rand_top_20
mkdir ../outputs/book_data/data/random/hyp_rand_top_20
python ../random_select.py -test_dir ../data/test.json -ref ../outputs/book_data/data/random/ref_rand_top_20 -hyp ../outputs/book_data/data/random/hyp_rand_top_20 -max_sent 20


echo "Top 25"
echo echo
mkdir ../outputs/book_data/data/random/ref_rand_top_25
mkdir ../outputs/book_data/data/random/hyp_rand_top_25
python ../random_select.py -test_dir ../data/test.json -ref ../outputs/book_data/data/random/ref_rand_top_25 -hyp ../outputs/book_data/data/random/hyp_rand_top_25 -max_sent 25
