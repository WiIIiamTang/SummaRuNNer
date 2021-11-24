from rouge import Rouge
import json
import re
import jieba
import time
import os
from multiprocessing import Pool,Process,Queue
import gc
import threading
import nltk

def word_token(text):
	list_words = list(jieba.cut(text))
	return nltk.word_tokenize(text)

def get_label(inp_file_text,inp_file_label,json_file):
	print("getting label..")
	f1 = open(inp_file_text,'r')
	f2 = open(inp_file_label,'r')
	print(json_file)
	r = Rouge()
	with open(json_file,'w',encoding='utf-8') as writer:
		count = 0
		start = time.time()
		for doc,summarize in zip(f1,f2):
			
			if (count+1)%1000 == 0:
				print('finished',count+1,'instances')
				print('time usage:',time.time()-start)
				start = time.time()
			#sents = [' '.join(word_token(sent.strip())) for sent in re.split('[。！？～；...\u200b\xa0]',doc.strip()) if len(sent.strip())>=5]
			sents = [sent.strip() for sent in doc.strip().split('\\n')]
			print('sents: ', sents)
			sents = [x for x in sents if x != '']
			print(f'length of sentence: {len(sents)}')
			labels = [0] * len(sents)
			#summarize = ' '.join(word_token(summarize))
			rouge_group = []
			score_mid,max_idx = 0,0
			print(summarize.replace('\\n', '.'))
			for i,sent_i in enumerate(sents):
				try:
					score = r.get_scores(sent_i,summarize.replace('\\n', '.'))[0]['rouge-1']['f']
				except Exception as e:
					print('sent_i:',sent_i)
					print('sents:',sents)
					print('summarize:',summarize)
					print(e)
					continue
					#return sents
				if score > score_mid:
					score_mid = score
					max_idx = i
			rouge_group.append(sents[max_idx])
			labels[max_idx] = 1

			score_max = score_mid
			for j,sent_j in enumerate(sents):
				if j == max_idx:
					continue
				score = r.get_scores(' '.join(rouge_group+[sent_j]),summarize)[0]['rouge-1']['f']
				if score > score_max:
					labels[j] = 1
					rouge_group.append(sent_j)
					score_max = score

			dict_mid = {}
			dict_mid['doc'] = '\n'.join(sents)
			dict_mid['labels'] = '\n'.join([str(x) for x in labels])
			dict_mid['summaries'] = summarize

			writer.write(json.dumps(dict_mid,ensure_ascii=False)+'\n')
			count += 1

def main():
	path = 'data/'
	start = time.time()
	p = Pool(10)
	for i in range(16):
		gc.disable()
		text,summa = path+'sent'+str(i)+'.txt',path+'summ'+str(i)+'.txt'
		print(text, summa)
		p.apply_async(get_label,args=(text,summa,'out_'+str(i)+'.json',))
		print('Process ',i,'is running.......')
		gc.enable()
	p.close()
	p.join()
	end = time.time()
	print('time used :',end-start)

if __name__ == '__main__':
	main()

