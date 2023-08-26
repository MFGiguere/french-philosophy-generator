# French philosophy article generator
The goal of this project was to train a language model to generate french philosophy articles. This project was started during the contexte of the Deepmay 2023 bootcamp. You can find below what we did on this project and what needs to be done for the future: feel free to collaborate, comment and/or send ideas! Please note that this is a really ambitious project that will probably not allow us to generate coherent philosophy articles. 

## Step 1: Find a database
The goal of this step was to identify a corpus of french philosophical text we could use for later steps. 
There were three ways this step could go
```
    1. We find a database of philosophy texts already formatted for AI.
    2. We find a website of philosophy texts that needs formatting.
    3. We find different websites for different styles of philosophy texts. 
```

After taking everything into account, we decided to go with step 2 and parse erudit.org for philosophy texts. The dataset can be found on Huggingface: https://huggingface.co/datasets/mfgiguere/erudit-french-philosophy

## Step 2: Parse and format the texts
To parse the texts, we used the functions that we defined in "scrape_models.py" and ran "parse_erudit_site(revues)". The strategy for each journal was list all editions, list all texts on to each editions and then parse the texts. Theses functions allowed us to parse 263 129 sentences and put them in a 86 917 ko file, which constitutes . Do note that since wifi , but an if-else was programmed in the functions to allow parsing the missing texts. 

While we will probably end up dropping most parameters, it's still useful to gather some of them since "all philosophy published on erudit.org" is a small dataset. 

## Step 3: Find and train a LLM
An issue that arose during the process was the lack of LLM in french: since english is the "standard" language in sciences and technology, Start with OpenAI that has french texts. We however found a promising model on https://huggingface.co/ named "dbddv01/gpt2-french-small". 

Right now, this step isn't finished: there are still errors when trying to load dataset or how to train the model. The most common error is "return torch.embedding(weight, input, padding_idx, scale_grad_by_freq, sparse)
IndexError: index out of range in self" that we get when trying to trainer.train. 

## Step 4: Generate text!
Since we didn't make it out of step 3, this stays really primitive. We want to generate texts using "title" as inputs. 

At this step, we also got errors. We get the warning "Please set `padding_side='left'` when initializing the tokenizer.". Also, the only sentences we get are "frey de l’autre côté, il est vrai que l’on ne peut pas" with a variable number of space at the end. 

## BONUS STEP: Click on the mustache
I have also included in this directory files for an ngram model trained with the french version of "Thus Spoke Zarathustra" by Nietzche. You can find this model in action here: https://mfgiguere.pythonanywhere.com/