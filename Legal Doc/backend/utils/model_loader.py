from transformers import TFAutoModelForTokenClassification, AutoTokenizer

def load_models():
    """Load IndicBERT NER and T5 simplification models"""
    return {
        "ner_model": TFAutoModelForTokenClassification.from_pretrained("backend/models/ner_model"),
        "simplifier": TFAutoModelForSequenceClassification.from_pretrained("t5-small"),
        "tokenizer": AutoTokenizer.from_pretrained("ai4bharat/IndicBERTv2")
    }