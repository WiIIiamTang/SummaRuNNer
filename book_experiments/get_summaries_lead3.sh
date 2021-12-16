
echo "Lead 3"
echo 
echo 
mkdir ../outputs/book_data/data/lead3/ref_lead3
mkdir ../outputs/book_data/data/lead3/hyp_lead3
python ../lead3.py -test_dir ../data/test.json -ref ../outputs/book_data/data/lead3/ref_lead3 -hyp ../outputs/book_data/data/lead3/hyp_lead3

