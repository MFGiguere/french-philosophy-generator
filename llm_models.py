import torch

from datasets import Dataset, load_dataset, DatasetDict

from parameters import model_type, features

from transformers import (
    pipeline,
    TrainingArguments, 
    Trainer,
    GPT2LMHeadModel, 
    GPT2Tokenizer,
    PhrasalConstraint,
    DataCollatorForLanguageModeling
)

path = "data_files//model"
###Initialize the model and do with the dataset. 
#First iteration needed to create the elements. 
def initialize_elems(model_type):
    model = GPT2LMHeadModel.from_pretrained(model_type)   

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding='max_length', truncation=True, max_length=100)

    dataset = load_dataset("csv", data_files="data_files//erudit.csv")
    dataset = dataset['train'].train_test_split(test_size=0.3)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    return model, tokenized_dataset

#Now that it exists we can just load the existing elements!
def load_elems():
    model = GPT2LMHeadModel.from_pretrained(path)
    features = features.update({'input_ids':str, 'attention_mask':str})
    dataset = load_dataset("json", data_files="data_files//dataset", features=features)
    return model, dataset




#Now I instantiate all that I need
tokenizer = GPT2Tokenizer.from_pretrained(model_type, max_length=100)
model, dataset = load_elems()


#Training
batch_size = 3
epochs = 10
weight_decay = 0.01
learning_rate = 1e-5

#2 data mlm
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, 
    mlm=False,
    mlm_probability= 0.15
)

training_args = TrainingArguments(
    output_dir=path, 
    overwrite_output_dir=True,
    num_train_epochs=epochs,
    per_gpu_train_batch_size= 16,
    weight_decay=weight_decay,
    save_total_limit=3,
    prediction_loss_only=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset["train"].shuffle(seed=45)
)

trainer.train()
trainer.save_model(path)

def generate(title, model):
    """Takes as str a fictive article title and generates an article."""
    paragraphs = 13.497328316801582
    sentences = 12
    sections = 4.497947782464942

    constraints = []
    for constraint_entitiy in " ".split(title):
        constraints.append(PhrasalConstraint(tokenizer(constraint_entitiy).input_ids))

    generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
    generator("", 
              num_beams = 5, 
              do_sample = False, 
              constraints = constraints,
              min_length = 45)
