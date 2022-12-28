"""
This script is for querying different pretrained QA models for comparing their surprisal and sampling patterns to human data.
Built based on code from https://medium.com/analytics-vidhya/question-answering-system-with-bert-ebe1130f8def .
"""

import torch
import transformers
import pandas as pd
from tqdm import tqdm
import random
import argparse

def predict_from_qa_model(model, stimuli, output_path):
    """
    Query the predicted spans from a pretrained QA model.
    Saves predicted decoded strings.
    """
    torch.manual_seed(1234)
    random.seed(1234)
    # read file with questions and answers
    df = pd.read_csv(stimuli)
    # assume there is a question and answer field and the file has long format
    assert ("question" in df.columns) and ("context_qa" in df.columns), "The stimuli file has to have a question and a context_qa column"
    
    # load requested model
    model_qa = transformers.AutoModelForQuestionAnswering.from_pretrained(model)
    tokenizer = transformers.AutoTokenizer.from_pretrained(model)
    print("(down)loaded model and tokenizer")

    # query the model
    model_name = []
    predicted_spans = []
    # TODO add possibilty to get top k predictions
    for _, r in df[["context_qa", "question"]].iterrows():
        # get token ids and position embeddings (contexts vs question) concatenated with CLS and SEP tokens
        encoding = tokenizer.encode_plus(
            text = r["question"],
            text_pair=r["context_qa"], 
            return_tensors="pt"
        )
        inputs = encoding['input_ids']  # Token embeddings
        segment_embedding = encoding['token_type_ids']  # Segment embeddings
        tokens = tokenizer.convert_ids_to_tokens(inputs.squeeze(0)) # input tokens for later decoding
        out = model_qa(inputs)
        # get predicted start and end of relevant span
        start_index = torch.argmax(out.start_logits, dim=-1)
        end_index = torch.argmax(out.end_logits, dim =-1)
        answer = " ".join(tokens[start_index:(end_index+1)])
        # fix subword tokenization and put back together words
        corrected_answer = ''
        for word in answer.split():
            # If it's a subword token append to sequence without space
            if word[0:2] == '##':
                corrected_answer += word[2:]
            else:
                corrected_answer += ' ' + word
        # save results   
        model_name.append(model)
        predicted_spans.append(corrected_answer)

    df["model_name"] = model_name
    df["predicted_spans"] = predicted_spans

    df.to_csv(output_path)    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help = "name of the Huggingface model to be used. If it cannot be accessed, an error will be thrown.")
    parser.add_argument(
        "-t", "--task", 
        help = "which task should be executed? (computing probability or sampling)", 
        choices = ["qa", "lm_prob", "lm_sampling"]
    )
    parser.add_argument("-p", "--path", help = "path to csv file containing stimuli")
    parser.add_argument("-o", "--output", help = "path to save processed output file to")
    # TODO add more decoding strategy args

    args = parser.parse_args()

    if args.task == "qa":
        predict_from_qa_model(args.model, args.path, args.output)

    else:
        pass
        # draw_samples_from_lm(args.model, args.stimuli)