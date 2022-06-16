import os
import torch
import datasets
import argparse
import pandas as pd
import pyarrow as pa
import numpy as np
import pickle as pkl
from scipy.special import softmax
from transformers import AutoTokenizer
from transformers import DataCollatorWithPadding
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizer, LineByLineTextDataset
from transformers import BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling
from transformers import TrainingArguments, Trainer





parser = argparse.ArgumentParser(description="""PhaTYP is a python library for bacteriophages' lifestyles prediction. 
                                 PhaTYP is a BERT-based model and rely on protein-based vocabulary to convert DNA sequences into sentences for prediction.""")
parser.add_argument('--out', help='name of the output file',  type=str, default = 'out/example_prediction.csv')
parser.add_argument('--reject', help='threshold to reject prophage',  type=float, default = 0.2)
parser.add_argument('--midfolder', help='folder to store the intermediate files', type=str, default='phatyp/')
inputs = parser.parse_args()

transformer_fn = inputs.midfolder

out_dir = os.path.dirname(inputs.out)
if out_dir != '':
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)



sentence_id2contig = pkl.load(open(f'{transformer_fn}/sentence_id2contig.dict', 'rb'))
bert_feat          = pd.read_csv(f'{transformer_fn}/bert_feat.csv')

SENTENCE_LEN = 300  # len
NUM_TOKEN = 45583   # PC

CONFIG_DIR = "config"
OUTPUT_DIR = "finetune"

# load the token configuration
tokenizer = BertTokenizer.from_pretrained(CONFIG_DIR, do_basic_tokenize=False)


def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)



train = pa.Table.from_pandas(bert_feat)
test  = pa.Table.from_pandas(bert_feat)
train = datasets.Dataset(train)
test  = datasets.Dataset(test)

data = datasets.DatasetDict({"train": train, "test": test})


tokenized_data= data.map(preprocess_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
model = AutoModelForSequenceClassification.from_pretrained("model", num_labels=2)


training_args = TrainingArguments(
    output_dir='results',
    overwrite_output_dir=False,
    do_train=True,
    do_eval=True,
    learning_rate=2e-5,
    num_train_epochs=10,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)




with torch.no_grad():
    pred, label, metric = trainer.predict(tokenized_data["test"])



prediction_value = []
for item in prediction:
    prediction_value.append(softmax(item))
prediction_value = np.array(prediction_value)


all_pred = []
all_score = []
for score in prediction_value:
    pred = np.argmax(score)
    if pred == 1:
        all_pred.append('temperate')
        all_score.append(score[1])
    else:
        all_pred.append('virulent')
        all_score.append(score[0])



pred_csv = pd.DataFrame({"Contig":id2contig.values(), "Pred":all_pred, "Score":all_score})
pred_csv.to_csv(inputs.out, index = False)
