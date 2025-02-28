from transformers import TFAutoModelForTokenClassification, DataCollatorForTokenClassification
from datasets import load_from_disk
import tensorflow as tf

# Load processed data
dataset = load_from_disk("training/data/processed")

# Model config
label_list = ["O", "B-PARTY", "I-PARTY", "B-CLAUSE", "I-CLAUSE", "B-AMOUNT", "I-AMOUNT"]

model = TFAutoModelForTokenClassification.from_pretrained(
    "ai4bharat/IndicBERTv2-mlm-only",
    num_labels=len(label_list),
    id2label={i: l for i, l in enumerate(label_list)}
)

# Training setup
model.compile(optimizer=tf.keras.optimizers.Adam(3e-5))
model.fit(
    dataset["train"].to_tf_dataset(batch_size=16),
    validation_data=dataset["test"].to_tf_dataset(batch_size=16),
    epochs=5
)