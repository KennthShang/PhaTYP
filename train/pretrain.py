import argparse
from transformers import BertTokenizer, LineByLineTextDataset
from transformers import BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments


SENTENCE_LEN = 300  # PC
NUM_TOKEN = 45583   # PC

parser = argparse.ArgumentParser(description="""PhaTYP is a python library for bacteriophages' lifestyles prediction. 
                                 PhaTYP is a BERT-based model and rely on protein-based vocabulary to convert DNA sequences into sentences for prediction.""")
parser.add_argument('--train', help='pth of the train file',  type=str, default = 'train.txt')
parser.add_argument('--val', help='pth of the test file',  type=str, default = 'val.txt')
inputs = parser.parse_args()


TRAIN_DATA_PATH = inputs.train
VAL_DATA_PATH = inputs.val
CONFIG_DIR = "../config"
OUTPUT_DIR = "log"

# load the token configuration
tokenizer = BertTokenizer.from_pretrained(CONFIG_DIR, do_basic_tokenize=False)

# # try example
# sentence = "PC_002835 PC_000001 UNKNOWN"
# encoded_input = tokenizer.tokenize(sentence)
# print(encoded_input)
# print(tokenizer.encode(sentence))

# load the training and evaluation datasets
data_train = LineByLineTextDataset(
    tokenizer = tokenizer,
    file_path = TRAIN_DATA_PATH,
    block_size = SENTENCE_LEN  # maximum sequence length
)

data_val = LineByLineTextDataset(
    tokenizer = tokenizer,
    file_path = VAL_DATA_PATH,
    block_size = SENTENCE_LEN  # maximum sequence length
)

print('No. of train: ', len(data_train)) # No of lines in your datset
print('No. of val: ', len(data_val)) # No of lines in your datset

# load the BERT configuration
config = BertConfig(
    vocab_size=NUM_TOKEN,
    hidden_size=512, 
    num_hidden_layers=8, 
    num_attention_heads=8,
    max_position_embeddings=SENTENCE_LEN
)

# loda the BERT mdoel
model = BertForMaskedLM(config)
print('No of parameters: ', model.num_parameters())

# set training configuration
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.025
)

# load the training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=False,
    do_train=True,
    do_eval=True,
    max_steps=200000,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=16,
    save_steps=500,
    save_total_limit=10,
    # prediction_loss_only=True,
    # gradient_accumulation_steps=25,
    gradient_accumulation_steps=2,
    evaluation_strategy='epoch',
    learning_rate=4e-4,
    adam_epsilon=1e-6,
    weight_decay=0.01,
    adam_beta1=0.9,
    adam_beta2=0.98,
    warmup_steps=10000,
    fp16=True
)

# set the training setting
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=data_train,
    eval_dataset=data_val
)

# Train !
trainer.train()
trainer.save_model(OUTPUT_DIR)
