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
        # segment_embedding = encoding['token_type_ids']  # Segment embeddings
        tokens = tokenizer.convert_ids_to_tokens(inputs.squeeze(0)) # input tokens for later decoding
        tokens = [t.encode("ascii", "ignore").decode() for t in tokens]
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

def sample_response_from_lm(model, path, output_path, topk, num_beams=1, max_length=0, temperature=0, top_p=1.0, top_k=0, seed=1234):
    """
    Helper for sampling responses from huggingface pretrained QA language models.

    Arguments:
    ---------
    model: str
        Huggingface name of the model to be used.
    path: str
        Path to stimuli file.
    output_path: str
        Path for saving file with samples.
    topk: int
        Number of predictions to return per input sample.
    num_beams: int
        Beam size rto use for returning >1 prediction per sample.
    max_length: int
        Maximal predicted sequence length.
    temperature: float
        Temperature for sampling next tokens.
    top_p: float
        P for nucleus sampling.
    top_k: int
        Number of tokens k to consider with top K sampling.
    seed: int
        Random seed to set.
    """
    torch.manual_seed(seed)
    random.seed(seed)
    # read file with questions and answers
    df = pd.read_csv(path)
    # assume there is a question and answer field and the file has long format
    assert ("question" in df.columns) and ("context_qa" in df.columns), "The stimuli file has to have a question and a context_qa column"
    
    assert topk <= num_beams, "Number of sequences to be returned has to be <= than the beam size when decoding"
    # move to gpu for faster inference
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    print("DEVICE ", device)
    # load requested model
    model_qa = transformers.AutoModelWithLMHead.from_pretrained(model)
    tokenizer = transformers.AutoTokenizer.from_pretrained(model)
    model_qa.to(device)

    model_name = []
    predictions = []
    for i, r in tqdm(df[["context_qa", "question"]].iterrows()):
        question = r["question"] # "What is 42?"
        context = r["context_qa"] # "42 is the answer to life, the universe and everything"
        input = f"question: {question} context: {context}"
        encoded_input = tokenizer(
            [input],
            return_tensors='pt',
            max_length=512,
            truncation=True
        )
        encoded_input.to(device)
        output = model_qa.generate(
            input_ids = encoded_input.input_ids,
            attention_mask = encoded_input.attention_mask,
            num_return_sequences = topk,
            num_beams = num_beams,
            max_length = max_length if max_length > 0 else 20,
            temperature = temperature if temperature != 1 else 1.0,
            top_p = top_p if top_p != 1 else top_p,
            top_k = top_k if top_k != 0 else 50,
        )
        output = tokenizer.batch_decode(output, skip_special_tokens=True)
        
        # append predictions
        model_name.append(model)
        predictions.append(output)

    df["model_name"] = model_name
    df["predictions"] = predictions

    df = df.explode(["predictions"])
    
    df.to_csv(output_path, index=False)  

def score_answers_with_lm(model, path, output_path, reduction="mean", seed=1234):
    """
    Helper for computing the probability of given responses under a pretrained LM.

    Arguments:
    ----------
    model: str
        Huggingface name of the model to be used.
    path: str
        Path to stimuli file.
    output_path: str
        Path for saving file with samples.
    seed: int
        Random seed to set.
    """
    torch.manual_seed(seed)
    random.seed(seed)

    # read file with questions and answers
    df = pd.read_csv(path)
    # assume there is a question and answer field and the file has long format
    assert all([c in df.columns for c in ["question", "context_qa", "taciturn", "competitor", "sameCategory", "otherCategory", "fullList"]]), "The stimuli file has to include the following columns: question, context_qa, taciturn, competitor, sameCategory, otherCategory, fullList"
    # move to gpu for faster inference
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    print("DEVICE ", device)

    criterion = torch.nn.CrossEntropyLoss(reduction=reduction)
    # load requested model
    model_qa = transformers.AutoModelWithLMHead.from_pretrained(model)
    tokenizer = transformers.AutoTokenizer.from_pretrained(model)
    model_qa.to(device)
    print("Model class ", model_qa.config_class)
    print("Vocab size ", len(tokenizer))

    model_name = []
    predictions = []
    answer_type = []
    for i, r in tqdm(df.iterrows()):
        probs = []
        # iterate over the different response options
        for a in ["taciturn", "competitor", "sameCategory", "otherCategory", "fullList"]:
            prompt = "question: " + r["question"] + " context: " + r["context_qa"]
            # tokenize
            encoded_input = tokenizer(
                [prompt],
                return_tensors='pt',
                max_length=512,
                truncation=True
            )
            encoded_input.to(device)
            encoded_answer = tokenizer(
                [r[a]],
                return_tensors='pt',
                max_length=512,
                truncation=True,
            )
            encoded_answer.to(device)
            # make forward step
            with torch.no_grad():
                output = model_qa(input_ids = encoded_input.input_ids, labels = encoded_answer.input_ids)
            # manually retrieve NLL from CE computation (to allow flexibility with respect to the reduction strategy)
            nll = criterion(output.logits.transpose(1,2), encoded_answer.input_ids)
            # store results (probs)
            probs.append(torch.exp(-nll).item())
            model_name.append(model)
            answer_type.append(a)
        # normalize over the different answer types
        vignette_probs = probs/np.sum(probs)
        predictions.append(vignette_probs)
    # append results to overall df
    df["answer_type_prob"] = predictions
    df = df.explode(["answer_type_prob"])
    df["model_name"] = model_name
    df["answer_type"] = answer_type
    
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
    parser.add_argument("-topk", "--topk", help = "top k candidate spans to decode", nargs="?", default=1, type=int)
    parser.add_argument("-ml", "--max_length", help = "max length of predicted response spans", nargs="?", default=0, type=int)
    parser.add_argument("-nb", "--num_beams", help = "size of beam to search when doing LM sampling", nargs="?", default=1, type=int)
    parser.add_argument("-tm", "--temperature", help = "sampling temperature when doing LM sampling", nargs="?", default=1, type=int)
    parser.add_argument("-tp", "--top_p", help = "top p for nucleus sampling when doing LM sampling", nargs="?", default=1, type=float)
    parser.add_argument("-tk", "--top_k", help = "top k number of tokens for sampling when doing LM sampling", nargs="?", default=0, type=int)
    parser.add_argument("-s", "--seed", help = "random seed for drawing several samples", nargs="?", default=1234, type=int)
    parser.add_argument("-r", "--reduction", help = "cross entropy calculation reduction strategy for scoring answer options with LMs", nargs="?", default="mean", type=str, choices=["mean", "sum"])

    args = parser.parse_args()

    if args.task == "qa":
        predict_from_qa_model(args.model, args.path, args.output, args.topk, args.max_length)

    elif args.task == "lm_sampling":
        sample_response_from_lm(args.model, args.path, args.output, args.topk, args.num_beams, args.max_length, args.temperature, args.top_p, args.top_k, args.seed)

    elif args.task == "lm_prob":
        score_answers_with_lm(args.model, args.path, args.output, args.reduction, args.seed)
    else:
        raise ValueError("Unrecognized task type")