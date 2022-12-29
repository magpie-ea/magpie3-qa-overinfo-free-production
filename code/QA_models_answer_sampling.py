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
# from pipelines import pipeline
import numpy as np

def correct_answer(answer):
    """
    Helper for decoding subword tokens as single words.

    Arguments:
    ---------
    answer: str
        String of raw decoded tokens.
    Returns:
    --------
    corrected_answer: str
        Fixed decoded string.
    """
    corrected_answer = ''
    for word in answer.split():
        # If it's a subword token append to sequence without space
        if word[0:2] == '##':
            corrected_answer += word[2:]
        else:
            corrected_answer += ' ' + word

    return corrected_answer

def predict_from_qa_model(model, stimuli, output_path, topk, max_length):
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
    softmax = torch.nn.Softmax(dim=-1) 
    for _, r in tqdm(df[["context_qa", "question"]].iterrows()):
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
        starts = softmax(out.start_logits).detach().numpy()
        ends = softmax(out.end_logits).detach().numpy()
        if starts.ndim == 1:
            starts = starts[None]

        if ends.ndim == 1:
            ends = ends[None]
        
        ##### top k infrastructure (from QA pipeline huggingface src)
        outer = np.matmul(np.expand_dims(starts, -1), np.expand_dims(ends, 1))
        max_answer_len = max_length if max_length > 0 else len(r["context_qa"].split())
        # Remove candidate with end < start and end - start > max_answer_len
        candidates = np.tril(np.triu(outer), max_answer_len - 1)
        scores_flat = candidates.flatten()
        if topk == 1:
            idx_sort = [np.argmax(scores_flat)]
        elif len(scores_flat) < topk:
            idx_sort = np.argsort(-scores_flat)
        else:
            idx = np.argpartition(-scores_flat, topk)[0:topk]
            idx_sort = idx[np.argsort(-scores_flat[idx])]
            
        start, end = np.unravel_index(idx_sort, candidates.shape)[1:]
        indices = zip(start, end)
        answers = [" ".join(tokens[start_index:(end_index+1)]) for start_index, end_index in indices]
        corrected_answers = [correct_answer(a) for a in answers]
        model_name.append(model)
        predicted_spans.append(corrected_answers)
        

    df["model_name"] = model_name
    df["predicted_spans"] = predicted_spans

    df = df.explode(["predicted_spans"])
    
    df.to_csv(output_path, index=False)    

def sample_response_from_lm(model, path, output, **kwargs):
    """
    Helper for sampling responses from huggingface pretrained QA language models.

    Arguments:
    ---------
    model: str
        Huggingface name of the model to be used.
    path: str
        Path to stimuli file.
    output: str
        Path for saving file with samples.
    """
    torch.manual_seed(1234)
    random.seed(1234)
    # read file with questions and answers
    df = pd.read_csv(stimuli)
    # assume there is a question and answer field and the file has long format
    assert ("question" in df.columns) and ("context_qa" in df.columns), "The stimuli file has to have a question and a context_qa column"
    
    # load requested model
    if model == "valhalla/t5-base-qa-qg-hl":
        nlp = transformers.pipeline("multitask-qa-qg", model=model)
        # for qa pass a dict with "question" and "context"
        response = nlp({
            "question": "What is 42 ?",
            "context": "42 is the answer to life, the universe and everything."
        })
    else:
        model_qa = transformers.AutoModelWithLMHead.from_pretrained(model)
        tokenizer = transformers.AutoTokenizer.from_pretrained(model)
        question = "What is 42?"
        context = "42 is the answer to life, the universe and everything"
        input = f"question: {question} context: {context}"
        encoded_input = tokenizer([input],
                                    return_tensors='pt',
                                    max_length=512,
                                    truncation=True)
        output = model.generate(input_ids = encoded_input.input_ids,
                                    attention_mask = encoded_input.attention_mask)
        output = tokenizer.decode(output[0], skip_special_tokens=True)
        print(output)


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
    parser.add_argument("-topk", "--topk", help = "top k candidate spans to decode", nargs="?", default=1, type=int)
    parser.add_argument("-ml", "--max_length", help = "max length of predicted response spans", nargs="?", default=0, type=int)
    
    
    args = parser.parse_args()

    if args.task == "qa":
        predict_from_qa_model(args.model, args.path, args.output, args.topk, args.max_length)

    else:
        pass
        # draw_samples_from_lm(args.model, args.stimuli)