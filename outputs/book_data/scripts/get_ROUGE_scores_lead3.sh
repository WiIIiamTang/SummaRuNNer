cd ../..
echo "75"
echo
echo
path_to_data_hyp="./book_data/data/lead3/hyp_lead3/"
path_to_data_ref="./book_data/data/lead3/ref_lead3/"
score_name="./book_data/scores/lead3"

python eval_config.py -b 75 -ref ${path_to_data_ref} -hyp ${path_to_data_hyp} >> ${score_name}_75.txt


echo "275"
echo
echo
python eval_config.py -b 275 -ref ${path_to_data_ref} -hyp ${path_to_data_hyp} >> ${score_name}_275.txt


echo "Top 15"
echo
echo
python eval_config.py -ref ${path_to_data_ref} -hyp ${path_to_data_hyp} >> ${score_name}_top_15.txt
