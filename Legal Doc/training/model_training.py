from transformers import AutoTokenizer, TFAutoModel, TFAutoModelForTokenClassification
import tensorflow as tf

# Load IndicBERT with NER head
model_name = "ai4bharat/IndicBERTv2-mlm-only"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForTokenClassification.from_pretrained(model_name, num_labels=7)  # 7 legal entity types

# Sample legal entity labels (customize with your dataset)
label_map = {
    0: "O",
    1: "B-LAW",
    2: "I-LAW",
    3: "B-CLAUSE",
    4: "I-CLAUSE",
    5: "B-PARTY",
    6: "I-PARTY"
}

# Sample training data preparation
def preprocess_legal_documents(texts, annotations):
    encodings = tokenizer(texts, truncation=True, padding=True, return_tensors="tf")
    labels = []
    for ann in annotations:
        labels.append([label_map[label] for label in ann])
    return encodings, tf.convert_to_tensor(labels)

# Training loop
def train_model():
    # Load your legal documents dataset here
    sample_texts = ["This Agreement is made between [Party A] and [Party B]..."]
    sample_annotations = [[0, 0, 0, 1, 2, 0, 0, 5, 6, 0, 5, 6]]
    
    train_encodings, train_labels = preprocess_legal_documents(sample_texts, sample_annotations)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(3e-5),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    
    model.fit(
        dict(train_encodings),
        train_labels,
        batch_size=8,
        epochs=3
    )
    
    model.save_pretrained("legal_ner_model")

if __name__ == "__main__":
    train_model()