
echo "75"
echo
echo
python ../../eval_config.py -b 75 -ref ../data/ref_75/ -hyp ../data/hyp_75/ >> ../scores/75.txt


echo "275"
echo
echo
python ../../eval_config.py -b 275 -ref ../data/ref_275/ -hyp ../data/hyp_275/ >> ../scores/275.txt


echo "Top 15"
echo
echo
python ../../eval_config.py -ref ../data/ref_top_15/ -hyp ../data/hyp_top_15/ >> ../scores/top_15.txt



echo "Top 20"
echo
echo
python ../../eval_config.py -ref ../data/ref_top_20/ -hyp ../data/hyp_top_20/ >> ../scores/top_20.txt


echo "Top 25"
echo
echo
python ../../eval_config.py -ref ../data/ref_top_25/ -hyp ../data/hyp_top_25/ >> ../scores/top_25.txt


