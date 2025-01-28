# import pandas as pd
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
# from datasets import Dataset
# import evaluate
# import torch
# import numpy as np
# from transformers import DataCollatorForSeq2Seq
# from transformers import Trainer, TrainingArguments, BitsAndBytesConfig
# from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
# import argparse
# import os
# import re
# from transformers import StoppingCriteria, StoppingCriteriaList

# class StoppingCriteriaSub(StoppingCriteria):
#     def __init__(self, stops = [], encounters=1):
#         super().__init__()
#         self.stops = [stop.to("cuda") for stop in stops]

#     def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
#         last_token = input_ids[0][-1]
#         for stop in self.stops:
#             if tokenizer.decode(stop) == tokenizer.decode(last_token):
#                 return True
#         return False


# stop_words = [".", "]", "']", "']\n", "\n", "]\n", "\n\n", "']\n\n", "</s>"]
# stop_words_ids = [tokenizer(stop_word, return_tensors='pt', add_special_tokens=False)['input_ids'].squeeze() for stop_word in stop_words]
# stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(stops=stop_words_ids)])

# def evaluate_generation(testing_datasets, top_sampling=False, beam_search=True, temperature=False, is_causallm = True):

#     # sbert_avg = 0.0

#     # sbert = SentenceTransformer('all-MiniLM-L6-v2')

#     generation_strategy = args.generation_strategy + "-" + str(args.fewshot_examples) if args.generation_strategy == "fewshot" else args.generation_strategy
#     foldername = f"{dataset}_{args.model_name}_{language}_{generation_strategy}_{args.use_extra_info}_{args.cn_strategy}_{top_sampling}_{beam_search}_{temperature}".replace("/", "-")
#     if not os.path.exists(f"test_results/{foldername}"):
#         os.makedirs(f"test_results/{foldername}")
#     for example in testing_datasets:
#         inputt = example["example"]
#         tweet = example["tweet"]
#         number = example["number"]
#         w = open(f"test_results/{foldername}/hate_tweet_{language}_{number}", 'w')
#         inputt.to(device)
#         if beam_search:
#             result = model.generate(**inputt, do_sample=True, max_new_tokens=280, num_beams=4, no_repeat_ngram_size=4, num_return_sequences=1, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id)
#         elif top_sampling:
#             result = model.generate(inputs=inputt, do_sample=True, max_new_tokens=280, top_k=0, top_p=0.92, no_repeat_ngram_size=2, num_return_sequences=1, stopping_criteria=stopping_criteria, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id)
#         elif temperature:
#             result = model.generate(inputs=inputt, do_sample=True, max_new_tokens=280, temperature=0.7, no_repeat_ngram_size=2, num_return_sequences=1, stopping_criteria=stopping_criteria, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id)
#         else:
#             result = model.generate(inputs=inputt, max_new_tokens=280, no_repeat_ngram_size=2, num_return_sequences=1, stopping_criteria=stopping_criteria, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id)
#         if is_causallm:
#             preds = str(tokenizer.decode(result[0][len(inputt["input_ids"][0]):]))
#         else:
#             preds = str(tokenizer.decode(result[0]))
#             preds = re.sub(r'<extra_id_\d*>', '', preds)
#         response = preds.replace("\n", "").replace("\t", "").split("[/INST]")[-1].replace("<s>", "").replace("</s>", "").replace("<pad>", "").replace("<|eot_id|>", "").replace("<|start_header_id|>", "").replace("<|im_end|>", "")
#         print("----------------------------------tweet-----------------------------")
#         print(tweet)
#         print("----------------------------------preds-----------------------------")
#         print(response)
#         print("\n")
#         # for labels in example[0]["counterSpeech"]:

#             # cosine_scores_preds = sbert.encode([preds], convert_to_tensor=True)
#             # cosine_scores_labels = sbert.encode([labels], convert_to_tensor=True)

#             # sbert_score = util.cos_sim(cosine_scores_preds, cosine_scores_labels)

#             # sbert_avg += sbert_score[0][0].item()
#         w.write(tweet.replace("\n", "").replace("\t", ""))
#         w.write('\n')
#         w.write(response)
#         w.write("\n")
#         w.close()
