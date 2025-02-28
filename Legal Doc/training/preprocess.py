from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("ai4bharat/IndicBERTv2")

def preprocess_data(examples):
    tokenized = tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=512,
        return_offsets_mapping=True
    )
    
    # Add label alignment logic here
    return tokenized