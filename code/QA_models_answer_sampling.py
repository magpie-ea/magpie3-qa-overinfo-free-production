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
import numpy as np

def format_inst_context(text, model, tokenizer):
    """
    Helper for inserting appropriate special tokens
    for Llama-chat / instruct and Mixtral-Instruct.
    """
    # NOTE: no system messages are used
    # NOTE: the few shot example is formatted as part of the instruction; not the model's own previous output
    if "70b-chat" in model:
        formatted_text = f"[INST] {text} [/INST]"
    elif "Mixtral-8x7B-Instruct" in model:
        formatted_text = f"[INST] {text} [/INST]"
    elif "Llama-3" in model:
        message = [
            {"role": "user", "content": text},
        ]

        formatted_text = tokenizer.apply_chat_template(
                message, 
                tokenize=False, 
                add_generation_prompt=True
        )
    else:
        formatted_text = text

    return formatted_text


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
    span_probs = []
    softmax = torch.nn.Softmax(dim=-1) 
    for _, r in tqdm(df[["context_qa", "question"]].iterrows()):
        # get token ids and position embeddings (contexts vs question) concatenated with CLS and SEP tokens
        encoding = tokenizer.encode_plus(
            text = r["question"],
            text_pair=r["context_qa"], 
            return_tensors="pt"
        )
        inputs = encoding['input_ids']  # Token embeddings
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
        ##### with additional renormalization of probabilities of possible candidate spans to allow to retrieve chosen span probabilities
        outer = np.matmul(np.expand_dims(starts, -1), np.expand_dims(ends, 1))
        max_answer_len = max_length if max_length > 0 else len(r["context_qa"].split())
        # Remove candidate with end < start and end - start > max_answer_len
        candidates = np.tril(np.triu(outer), max_answer_len - 1)
        scores_flat = candidates.flatten()
        # renormalize the possible candidate probabilities 
        candidates_renorm = softmax(torch.tensor(scores_flat)).detach().numpy()
        
        if topk == 1:
            idx_sort = [np.argmax(candidates_renorm)]
        elif len(scores_flat) < topk:
            idx_sort = np.argsort(-candidates_renorm)
        else:
            idx = np.argpartition(-candidates_renorm, topk)[0:topk]
            idx_sort = idx[np.argsort(-candidates_renorm[idx])]
            
        start, end = np.unravel_index(idx_sort, candidates.shape)[1:]
        indices = zip(start, end)
        answers = [" ".join(tokens[start_index:(end_index+1)]) for start_index, end_index in indices]
        corrected_answers = [correct_answer(a) for a in answers]
        # retrieving topk probs
        spans_prob = candidates_renorm[idx_sort]
        
        span_probs.append(spans_prob)
        model_name.append(model)
        predicted_spans.append(corrected_answers)

        

    df["model_name"] = model_name
    df["predicted_spans"] = predicted_spans
    df["prediction_probs"] = span_probs

    df = df.explode(["predicted_spans", "prediction_probs"])
    
    df.to_csv(output_path, index=False)    

def sample_response_from_lm(model, path, output_path, topk, num_beams=1, max_length=0, temperature=0, top_p=1.0, top_k=0, seed=1234, few_shot=False, prompt="zero-shot", experiment="e1"):
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
    few_shot: bool
        Flag indicating whether to use the one-shot example context additionally to the story context.
    prompt: str
        Type of prompt to use for sampling.
    experiment: str
        Experiment number.
    """
    model_out = model.split("/")[-1]
    constructed_output_path = output_path + f"results_{experiment}_{model_out}_{prompt}.csv"
    torch.manual_seed(seed)
    random.seed(seed)
    # read file with questions and answers
    df = pd.read_csv(path)
    # assume there is a question and answer field and the file has long format
    assert ("question" in df.columns) and ("context_qa" in df.columns), "The stimuli file has to have a question and a context_qa column"
    
#    assert topk <= num_beams, "Number of sequences to be returned has to be <= than the beam size when decoding"
    # move to gpu for faster inference
    if torch.backends.mps.is_available():
        device = "cpu"#"mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    print("DEVICE ", device)
    # load requested model
    model_qa = transformers.AutoModelForCausalLM.from_pretrained(
        model,
        device_map="auto",
        torch_dtype=torch.float16,

    )
    model_qa.eval()
    if model == "danyaljj/gpt2_question_answering_squad2":
        tokenizer = transformers.AutoTokenizer.from_pretrained("gpt2")
    else:
        tokenizer = transformers.AutoTokenizer.from_pretrained(model)

    # model_qa.to(device)
    if experiment == "e1":
        few_shot_context = """
        You are hosting a barbecue party. You are standing behind the barbecue. You have the following goods to offer: pork sausages, vegan burgers, grilled potatoes and beef burgers. 
        """
        few_shot_question = "Someone asks: Do you have grilled zucchini? "
        few_shot_answer = "You reply: I'm sorry, I don't have any grilled zucchini. But I do have some grilled potatoes."
        few_shot_cot = "Let's think step by step. You reason about what that person most likely wanted to have. That they asked for grilled zucchini suggests that they might want vegetarian food. From the items you have pork sausages and beef burgers are least likely to satisfy the persons desires. Vegan burgers and grilled potatoes come much closer. Grilled potatoes are most similar to grilled zucchini."
    elif experiment == "e2":
        few_shot_context = "You give a dinner party at your apartment. More people showed up than you expected. Your neighbor, who just arrived, approaches you and asks: Do you have a spare chair I could borrow? You do not, in fact, have a spare chair, but you do have the following items: a broom, a TV armchair, a stool, a ladder and a kitchen table. "
        few_shot_question = ""
        few_shot_answer = "So you say: No, I don't have a spare chair, but you can have the stool."
        few_shot_cot = "You deliberate your response as follows. The practical goal of the questioner is to sit down at the dinner table. For this purpose, the most useful object from the list of available items is the stool."
    elif experiment == "e3_highprior":
        few_shot_context = "There are three types of laptops commonly used in your town: Acer laptops, MacBooks and Dell laptops. It is common knowledge that Acer laptops are used by most people, MacBooks are used by fewer people, and Dell laptops are very rare."
        few_shot_question = "A hypermarket carries laptop chargers for all types of laptops except the least common Dell laptops. A customer walks in and asks a salesperson: Do you have laptop chargers?"
        few_shot_answer = "The salesperson replies: Yes, we do."
        few_shot_cot = "Let's think step by step. The salesperson reasons about the kind of laptop the customer most likely needs a charger for. Given their common knowledge, it is most likely that the customer has an Acer laptop. Therefore, it is likely that the customer is interested in an Acer charger. The hypermarket has Acer chargers and can therefore satisfy the customer's potential needs."
    elif experiment == "e3_lowprior":
        few_shot_context = "There are three types of laptops commonly used in your town: Acer laptops, MacBooks and Dell laptops. It is common knowledge that Acer laptops are used by most people, MacBooks are used by fewer people, and Dell laptops are very rare."
        few_shot_question = "A hypermarket carries laptop accessories for all types of laptops except the most common Acer laptops. A customer walks in and asks a salesperson: Do you have laptop chargers?"
        few_shot_answer = "The salesperson replies: Yes, but we don't have Acer chargers."
        few_shot_cot = "Let's think step by step. The salesperson reasons about the kind of laptop the customer most likely needs a charger for. Given their common knowledge, it is most likely that the customer has an Acer laptop. Therefore, it is likely that the customer is interested in an Acer charger. However, the hypermarket doesn't have Acer chargers and therefore might not be able to satisfy the customer's potential needs."
    else:
        raise ValueError("Experiment type incorrect!")
    
    model_name = []
    predictions = []
    probs = []
    prompting = []
    inputs = []
    for i, r in tqdm(df[["context_qa", "question"]].iterrows()):
        question = r["question"] 
        context = r["context_qa"] 
        if few_shot:
            if prompt == "cot":
                context = few_shot_context + few_shot_question + few_shot_cot + " " + few_shot_answer + "\n\nYour turn.\n" + context
            elif prompt == "explanation":
                context = few_shot_context + few_shot_question + few_shot_cot + "\n\nYour turn.\n" + context
            elif prompt == "example":
                context = few_shot_context + few_shot_question + few_shot_answer + "\n\nYour turn.\n" + context
            else:
                context = context

        if model == "danyaljj/gpt2_question_answering_squad2":
            input = f"{context} Q: {question} A:"
        elif model == "gpt2":
            input = context + " " + question + " You reply:" 
        else:
            input = f"{context} {question}" #f"question: {question} context: {context}"
        inputs.append(input)
        formatted_input = format_inst_context(
            input,
            model,
            tokenizer,
        )
        print("### Formatted input#### ", formatted_input)
        encoded_input = tokenizer(
            formatted_input,
            return_tensors='pt',
            # max_length=512,
            # truncation=True
        )
        # print("Encoded formatted input: ", encoded_input)
        # print("Encoding decoded back w special tokens:", tokenizer.decode(encoded_input.input_ids[0], skip_special_tokens=False) )
        print("Input ids ", len(encoded_input.input_ids))
        encoded_input.to(model_qa.device)
        
        output = model_qa.generate(
                input_ids = encoded_input.input_ids,
                attention_mask = encoded_input.attention_mask,
                do_sample=True,
                num_return_sequences = topk,
             #   num_beams = num_beams,
                max_new_tokens = max_length if max_length > 0 else 20,
                temperature = temperature if temperature != 1 else 1.0,
                top_p = top_p if top_p != 1 else top_p,
                top_k = top_k if top_k != 0 else None,
                output_scores = True,
                return_dict_in_generate = True,
        )
        if "gpt2" in model:
                # only take the scores of the answer sequence
            start_ind = encoded_input.input_ids[0].shape[-1] + 1
            output_seq = tokenizer.batch_decode(output.sequences[:, start_ind:], skip_special_tokens=True)
        elif ("mistral" in model) or ("llama" in model):
            start_ind = encoded_input.input_ids[0].shape[-1]
            print("Mistral start ind ", start_ind)
            output_seq = tokenizer.batch_decode(output.sequences[:, start_ind:], skip_special_tokens=True)
            print(output_seq)
            print(output.keys())
        else:
            output_seq = tokenizer.batch_decode(output.sequences, skip_special_tokens=True)
        # catch some weird (probably version difference related) bugs arising with finetuned BART
       # except ValueError:
        #    output_seq = "ERROR"
        continuation = output.sequences[:, start_ind:]
        seq_mean_log_prob = [np.nan for i in range(len(output_seq))]
        # for k in range(len(output_seq)):
        #     print('len scores ', len(output.scores), output.scores[0].shape)
        #     seq_log_prob = [output.scores[i][k, j].item() for i, j in enumerate(continuation)]
        #     seq_mean_log_p = np.mean([np.log(np.exp(i)/(1 + np.exp(i))) for i in seq_log_prob])
        # seq_mean_log_prob.append(seq_mean_log_p)
        # append predictions
        model_name.append(model)
        predictions.append(output_seq)
        prompting.append(prompt)
        probs.append(seq_mean_log_prob)

    df["model_name"] = model_name
    df["inputs"] = inputs
    df["predictions"] = predictions
    df["probs"] = probs
    df["prompting_strategy"] = prompting

    df = df.explode(["predictions", "probs"])
    
    df.to_csv(constructed_output_path, index=False)  

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
    # colnames = ["taciturn", "competitor", "sameCategory1", "sameCategory2", "sameCategory3", "otherCategory", "fullList_0", "fullList_1", "fullList_2", "fullList_3", "fullList_4", "fullList_5"]
    colnames = ["taciturn", "competitor", 'mostSimilar', "otherCategory", 'sameCategory_0', 'sameCategory_1', 'sameCategory_2', 'sameCategory_3',
       'sameCategory_4', 'sameCategory_5', 'sameCategory_6', 'sameCategory_7',
       'sameCategory_8', 'sameCategory_9', 'sameCategory_10',
       'sameCategory_11', 'sameCategory_12', 'fullList_0', 'fullList_1',
       'fullList_2', 'fullList_3', 'fullList_4', 'fullList_5', 'fullList_6',
       'fullList_7', 'fullList_8', 'fullList_9', 'fullList_10', 'fullList_11',
       'fullList_12', 'fullList_13', 'fullList_14', 'fullList_15',
       'fullList_16', 'fullList_17', 'fullList_18', 'fullList_19',
       'fullList_20', 'fullList_21', 'fullList_22', 'fullList_23']
    
    # assume there is a question and answer field and the file has long format
    assert all([c in df.columns for c in colnames + ["question", "context_qa"]]), "The stimuli file has to include the following columns: question, context_qa, taciturn, competitor, sameCategory, otherCategory (_1, _2, _3), fullList (_0 until _5)"
    # move to gpu for faster inference
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    print("DEVICE ", device)

    criterion = torch.nn.CrossEntropyLoss(reduction=reduction)
    criterion_sum = torch.nn.CrossEntropyLoss(reduction="sum")
    # load requested model
    model_qa = transformers.AutoModelWithLMHead.from_pretrained(model)
    tokenizer = transformers.AutoTokenizer.from_pretrained(model)
    model_qa.to(device)
    print("Model class ", model_qa.config_class)
    print("Vocab size ", len(tokenizer))

    model_name = []
    predictions = []
    perplexities = []
    # length_normalized_probs = []
    answer_type = []
        
    for i, r in tqdm(df.iterrows()):
        # init named tuples
        probs = {k: 0 for k in colnames}
        ppls = {k: 0 for k in colnames}
        normalized_probs = {k: 0 for k in colnames}
        # iterate over the different response options
        for a in colnames:
            if model == "danyaljj/gpt2_question_answering_squad2":
                prompt = f"{r['context_qa']} Q: {r['question']} A: {r[a]}"
            elif model == "gpt2":
                prompt = r['context_qa'] + " " +r['question'] + " You reply: " + r[a]
            else:
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
            with torch.no_grad():
                # for decoder only models, the entire sequence including the context is passed as the label
                if "gpt2" in model: 
                    output = model_qa(**encoded_input, labels = encoded_input.input_ids)
                # for encoder-decoder models, only the answer is passed as the labels since the input context is  only passed through the encoder
                else:
                    output = model_qa(input_ids = encoded_input.input_ids, labels = encoded_answer.input_ids)
            # manually retrieve NLL from CE computation (to allow flexibility with respect to the reduction strategy)
            if "gpt2" in model:
                # only take the scores of the answer sequence
                encoded_input_rev = encoded_input.input_ids[0].tolist()
                encoded_input_rev.reverse() # for finding last occurence of : as the token for retrieving the answer probs only
                start_ind = len(encoded_input_rev) - encoded_input_rev.index(tokenizer([":"], return_tensors='pt').input_ids[0, 0].item()) 
                nll = criterion(output.logits[:, start_ind:, :].transpose(1,2), encoded_answer.input_ids[:, :])
                # compute perplexity
                sentence_nll = criterion_sum(output.logits[:, start_ind:, :].transpose(1,2), encoded_answer.input_ids[:, :])
                ppl = torch.exp(sentence_nll / encoded_answer.input_ids[:, :].shape[-1])
                
            else:
                nll = criterion(output.logits.transpose(1,2), encoded_answer.input_ids)
                # compute perplexity
                sentence_nll = criterion_sum(output.logits.transpose(1,2), encoded_answer.input_ids)
                ppl = torch.exp(sentence_nll / encoded_answer.input_ids.shape[-1])
                
            # store results (probs)
            probs[a] = torch.exp(-nll).item()
            ppls[a] = ppl.item()
            # normalized_probs[a] = normalized_sentence_prob.item()
            # probs.append(torch.exp(-nll).item())
            # ppls.append(ppl.item())
            # normalized_probs.append(normalized_sentence_prob.item())
        model_name.append([model]*6)
        answer_type.append(["taciturn", "competitor", "mostSimilar", "sameCategory", "otherCategory", "fullList"])
        # average over the different sameCategory / fullList options
        avg_probs = [probs["taciturn"],
            probs["competitor"],
            probs["mostSimilar"],
            np.mean([probs[k] for k in [c for c in colnames if c.startswith("sameCategory")]]),
            probs["otherCategory"],
            np.mean([probs[k] for k in [c for c in colnames if c.startswith("fullList")]])
        ]
        avg_ppls = [ppls["taciturn"],
            ppls["competitor"],
            ppls["mostSimilar"],
            np.mean([ppls[k] for k in [c for c in colnames if c.startswith("sameCategory")]]),
            ppls["otherCategory"],
            np.mean([ppls[k] for k in [c for c in colnames if c.startswith("fullList")]])
        ]
    
        # normalize over the different answer types
        vignette_probs = avg_probs/np.sum(avg_probs)
        predictions.append(vignette_probs)
        perplexities.append(avg_ppls)
    
    # append results to overall df
    df["answer_type_prob_avg"] = predictions
    df["answer_type_ppl"] = perplexities
    df["model_name"] = model_name
    df["answer_type"] = answer_type
    df = df.explode(["answer_type_prob_avg", "answer_type_ppl", "model_name", "answer_type"]) 
    
    
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
    parser.add_argument("-fs", "--few_shot", help = "should the few-shot example context be used for LMs?", action="store_true")
    parser.add_argument("-pr", "--prompt", help="Type of prompt", default="zero-shot", type=str, choices=["zero-shot", "explanation", "example", "cot"])
    parser.add_argument("-ex", "--experiment", help="Type of experiment", default="e1", type=str, choices=["e1", "e2", "e3_highprior", "e3_lowprior"])

    args = parser.parse_args()

    if args.task == "qa":
        predict_from_qa_model(args.model, args.path, args.output, args.topk, args.max_length)

    elif args.task == "lm_sampling":
        sample_response_from_lm(args.model, args.path, args.output, args.topk, args.num_beams, args.max_length, args.temperature, args.top_p, args.top_k, args.seed, args.few_shot, args.prompt, args.experiment)

    elif args.task == "lm_prob":
        score_answers_with_lm(args.model, args.path, args.output, args.reduction, args.seed)
    else:
        raise ValueError("Unrecognized task type")
