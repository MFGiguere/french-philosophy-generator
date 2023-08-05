features = {
        "Journal": str,              #The name of the journal where the text was published
        "Author": str,               #Required to be able to generate texts by author. 
        "Year": str,                 #Will help form a sense of direction on a large scale.  
        "Title": str,                #Can be useful for smaller dataset, but can be inferred with enough files. 
        "section_rank": int,         #Abstract will be 0 and sections will start as 1. 
        "par_rank": int,             #Abstract will be 0 and paragraphs will start as 1. 
        "sent_rank": int,            #no of sentence in the paragraph
        "text": str                  #Will be single sentence at a time. 
        }

revues = ["philoso", "ltp", "sp"]    #This represents all journals in french under the "philosophy" label on erudit.org. 

model_type = "dbddv01/gpt2-french-small"
