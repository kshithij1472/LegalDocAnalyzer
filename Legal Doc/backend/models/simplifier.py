from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer

model = TFAutoModelForSeq2SeqLM.from_pretrained("t5-small")
tokenizer = AutoTokenizer.from_pretrained("t5-small")