import pickle as pkl
from transformers import AutoTokenizer
from transformers import DataCollatorWithPadding
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizer, LineByLineTextDataset
from transformers import BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling
from transformers import TrainingArguments, Trainer
import datasets
import pandas as pd
import pyarrow as pa
import numpy as np
import argparse
from datasets import load_metric

parser = argparse.ArgumentParser(description="""PhaTYP is a python library for bacteriophages' lifestyles prediction. 
                                 PhaTYP is a BERT-based model and rely on protein-based vocabulary to convert DNA sequences into sentences for prediction.""")
parser.add_argument('--train', help='pth of the train file',  type=str, default = 'train.csv')
parser.add_argument('--val', help='pth of the test file',  type=str, default = 'val.csv')
inputs = parser.parse_args()



SENTENCE_LEN = 300  # PC
NUM_TOKEN = 45583   # PC

CONFIG_DIR = "../config"
OUTPUT_DIR = "finetune"

# load the token configuration
tokenizer = BertTokenizer.from_pretrained(CONFIG_DIR, do_basic_tokenize=False)


def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


train = pd.read_csv(inputs.train)
test  = pd.read_csv(inputs.val)
train = pa.Table.from_pandas(train)
test  = pa.Table.from_pandas(test)
train = datasets.Dataset(train)
test  = datasets.Dataset(test)

data = datasets.DatasetDict({"train": train, "test": test})


tokenized_data= data.map(preprocess_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
model = AutoModelForSequenceClassification.from_pretrained("log", num_labels=2)


training_args = TrainingArguments(
    output_dir='results',
    overwrite_output_dir=False,
    do_train=True,
    do_eval=True,
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    num_train_epochs=10,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)


trainer.train()
pred, label, metric = trainer.predict(tokenized_data["test"])

def return_metrics(pred, labels):
    predictions = np.argmax(pred, axis=-1)
    TP, FP, FN, TN = 0, 0, 0, 0
    for pred, label in zip(predictions, labels):
        if pred == label and label == 1:
            TP += 1
        elif pred == label and label == 0:
            TN += 1
        elif pred != label and label == 1:
            FN += 1
        elif pred != label and label == 0:
            FP += 1
    return TP/(TP+FN), TN/(TN+FP)


viru, temp = return_metrics(pred, label)
print(f'viru acc: {viru:.2f} || temp acc: {temp:.2f}')
trainer.save_model("model")
