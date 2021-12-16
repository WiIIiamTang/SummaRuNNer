cd ../..
echo "75"
echo
echo
path_to_data_hyp="./book_data/data/sumaG/hyp"
path_to_data_ref="./book_data/data/sumaG/ref"
score_name="./book_data/scores/sumaG"

python eval_config.py -b 75 -ref ${path_to_data_ref}_75/ -hyp ${path_to_data_hyp}_75/ >> ${score_name}_75.txt


echo "275"
echo
echo
python eval_config.py -b 275 -ref ${path_to_data_ref}_275/ -hyp ${path_to_data_hyp}_275/ >> ${score_name}_275.txt


echo "Top 15"
echo
echo
python eval_config.py -ref ${path_to_data_ref}_top_15/ -hyp ${path_to_data_hyp}_top_15/ >> ${score_name}_top_15.txt



echo "Top 20"
echo
echo
python eval_config.py -ref ${path_to_data_ref}_top_20/ -hyp ${path_to_data_hyp}_top_20/ >> ${score_name}_top_20.txt


echo "Top 25"
echo
echo
python eval_config.py -ref ${path_to_data_ref}_top_25/ -hyp ${path_to_data_hyp}_top_25/ >> ${score_name}_top_25.txt


