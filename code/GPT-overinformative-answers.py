import openai
import time
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
import argparse 
from openai import OpenAI
from pprint import pprint
from datetime import datetime

# set openAI key in separate .env file w/ content
# OPENAIKEY = yourkey
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# items = pd.read_csv('trials_LLMs_e1.csv')
# items = pd.read_csv('../experiments/free_production/trials/trials_LLMs_all_options_postprocessed.csv')
# items = pd.read_csv('../experiments/contextSensitive_free_production/trials/trials_e2_fctPrompt_fixedOrder.csv')[24:].reset_index()
# items = pd.read_csv('speaker_priors_examples2.csv') #[24:].reset_index()

# items = pd.read_csv('trials_LLMs_e2.csv')

examples = {
    "e1": {
        "zero-shot": "",
        "cot": "You are hosting a barbecue party. You are standing behind the barbecue. You have the following goods to offer: pork sausages, vegan burgers, grilled potatoes and beef burgers. Someone asks: Do you have grilled zucchini? Let's think step by step. You reason about what that person most likely wanted to have. That they asked for grilled zucchini suggests that they might want vegetarian food. From the items you have pork sausages and beef burgers are least likely to satisfy the persons desires. Vegan burgers and grilled potatoes come much closer. Grilled potatoes are most similar to grilled zucchini. You reply: I'm sorry, I don't have any grilled zucchini. But I do have some grilled potatoes.",
        "explanation": "You are hosting a barbecue party. You are standing behind the barbecue. You have the following goods to offer: pork sausages, vegan burgers, grilled potatoes and beef burgers. Someone asks: Do you have grilled zucchini? Let's think step by step. You reason about what that person most likely wanted to have. That they asked for grilled zucchini suggests that they might want vegetarian food. From the items you have pork sausages and beef burgers are least likely to satisfy the persons desires. Vegan burgers and grilled potatoes come much closer. Grilled potatoes are most similar to grilled zucchini.",
        "example": "You are hosting a barbecue party. You are standing behind the barbecue. You have the following goods to offer: pork sausages, vegan burgers, grilled potatoes and beef burgers. Someone asks: Do you have grilled zucchini? You reply: I'm sorry, I don't have any grilled zucchini. But I do have some grilled potatoes."
    },
    "e2": {
        "zero-shot": "",
        "cot": "You give a dinner party at your apartment. More people showed up than you expected.\nYour neighbor, who just arrived, approaches you and asks: Do you have a spare chair I could borrow? You do not, in fact, have a spare chair, but you do have the following items: a broom, a TV armchair, a stool, a ladder and a kitchen table. You deliberate your response as follows. The practical goal of the questioner is to sit down at the dinner table. For this purpose, the most useful object from the list of available items is the stool. So you say: No, I don't have a spare chair, but you can have the stool.",
        "explanation": "You give a dinner party at your apartment. More people showed up than you expected.\nYour neighbor, who just arrived, approaches you and asks: Do you have a spare chair I could borrow? You do not, in fact, have a spare chair, but you do have the following items: a broom, a TV armchair, a stool, a ladder and a kitchen table. You deliberate your response as follows. The practical goal of the questioner is to sit down at the dinner table. For this purpose, the most useful object from the list of available items is the stool.",
        "example": "You give a dinner party at your apartment. More people showed up than you expected.\nYour neighbor, who just arrived, approaches you and asks: Do you have a spare chair I could borrow? You do not, in fact, have a spare chair, but you do have the following items: a broom, a TV armchair, a stool, a ladder and a kitchen table. So you say: No, I don't have a spare chair, but you can have the stool."
    },
    "e3_lowprior": {
        "zero-shot": "",
        "cot": "There are three types of laptops commonly used in your town: Acer laptops, MacBooks and Dell laptops. It is common knowledge that Acer laptops are used by most people, MacBooks are used by fewer people, and Dell laptops are very rare. A hypermarket carries laptop accessories for all types of laptops except the most common Acer laptops. A customer walks in and asks a salesperson: Do you have laptop chargers?\nLet's think step by step. The salesperson reasons about the kind of laptop the customer most likely needs a charger for. Given their common knowledge, it is most likely that the customer has an Acer laptop. Therefore, it is likely that the customer is interested in an Acer charger. However, the hypermarket doesn't have Acer chargers and therefore might not be able to satisfy the customer's potential needs. The salesperson replies: Yes, but we don't have Acer chargers.",
        "explanation": "There are three types of laptops commonly used in your town: Acer laptops, MacBooks and Dell laptops. It is common knowledge that Acer laptops are used by most people, MacBooks are used by fewer people, and Dell laptops are very rare. A hypermarket carries laptop accessories for all types of laptops except the most common Acer laptops. A customer walks in and asks a salesperson: Do you have laptop chargers?\nLet's think step by step. The salesperson reasons about the kind of laptop the customer most likely needs a charger for. Given their common knowledge, it is most likely that the customer has an Acer laptop. Therefore, it is likely that the customer is interested in an Acer charger. However, the hypermarket doesn't have Acer chargers and therefore might not be able to satisfy the customer's potential needs.",
        "example": "There are three types of laptops commonly used in your town: Acer laptops, MacBooks and Dell laptops. It is common knowledge that Acer laptops are used by most people, MacBooks are used by fewer people, and Dell laptops are very rare. A hypermarket carries laptop accessories for all types of laptops except the most common Acer laptops. A customer walks in and asks a salesperson: Do you have laptop chargers?\nThe salesperson replies: Yes, but we don't have Acer chargers."
    },
    "e3_highprior": {
        "zero-shot": "",
        "cot": "There are three types of laptops commonly used in your town: Acer laptops, MacBooks and Dell laptops. It is common knowledge that Acer laptops are used by most people, MacBooks are used by fewer people, and Dell laptops are very rare. A hypermarket carries laptop chargers for all types of laptops except the least common Dell laptops. A customer walks in and asks a salesperson: Do you have laptop chargers?\nLet's think step by step. The salesperson reasons about the kind of laptop the customer most likely needs a charger for. Given their common knowledge, it is most likely that the customer has an Acer laptop. Therefore, it is likely that the customer is interested in an Acer charger. The hypermarket has Acer chargers and can therefore satisfy the customer's potential needs. The salesperson replies: Yes, we do.",
        "explanation": "There are three types of laptops commonly used in your town: Acer laptops, MacBooks and Dell laptops. It is common knowledge that Acer laptops are used by most people, MacBooks are used by fewer people, and Dell laptops are very rare. A hypermarket carries laptop chargers for all types of laptops except the least common Dell laptops. A customer walks in and asks a salesperson: Do you have laptop chargers?\nLet's think step by step. The salesperson reasons about the kind of laptop the customer most likely needs a charger for. Given their common knowledge, it is most likely that the customer has an Acer laptop. Therefore, it is likely that the customer is interested in an Acer charger. The hypermarket has Acer chargers and can therefore satisfy the customer's potential needs.",
        "example": "There are three types of laptops commonly used in your town: Acer laptops, MacBooks and Dell laptops. It is common knowledge that Acer laptops are used by most people, MacBooks are used by fewer people, and Dell laptops are very rare. A hypermarket carries laptop chargers for all types of laptops except the least common Dell laptops. A customer walks in and asks a salesperson: Do you have laptop chargers?\nThe salesperson replies: Yes, we do."
    }    
}
# preface for GPT3 as a one-shot learner in E1
oneShotExample = '''EXAMPLE: 

You are hosting a barbecue party. You are standing behind the barbecue. You have the following goods to offer: pork sausages, vegan burgers, grilled potatoes and beef burgers. 
Someone asks: Do you have grilled zucchini?

Let's think step by step. You reason about what that person most likely wanted to have. That they asked for grilled zucchini suggests that they might want vegetarian food. From the items you have pork sausages and beef burgers are least likely to satisfy the person's desires. Vegan burgers and grilled potatoes come much closer. Grilled potatoes are most similar to grilled zucchini.
You reply: I'm sorry, I don't have any grilled zucchini. But I do have some grilled potatoes.

YOUR TURN:
'''
# preface for GPT3 as a one-shot learner in E2
oneShotExampleE2 = '''EXAMPLE:

You give a dinner party at your apartment. More people showed up than you expected. 
Your neighbor, who just arrived, approaches you and asks: Do you have a spare chair I could borrow?

You do not, in fact, have a spare chair, but you do have the following items: a broom, a TV armchair, a stool, a ladder and a kitchen table. You deliberate your response as follows. The practical goal of the questioner is to sit down at the dinner table. For this purpose, the most useful object from the list of available items is the stool.
So you say: No, I don't have a spare chair, but you can have the stool.

YOUR TURN:
'''
oneShotExampleE2_mismatch = '''EXAMPLE:

You give a dinner party at your apartment. More people showed up than you expected. 
Your neighbor, who just arrived, approaches you and asks: Do you have a spare chair I could borrow?

You do not, in fact, have a spare chair, but you do have the following items: a stool, a TV armchair, a ladder and a broom. 
So you say: No, I don't have a spare chair, but you can have the broom.

YOUR TURN:
''' # You deliberate your response as follows. The practical goal of the questioner is to sit down at the dinner table. For this purpose, the most useful object from the list of available items is the broom.
oneShotExampleE2_polina = '''EXAMPLE:

You are out in the forest for a camping trip with your friends. You are about to camp for the first night in a new location.
Your friend starts to stake the tent and asks: Do you have a hammer?

You do not, in fact, have a hammer, but you do have the following available options: a handsaw, a rock, an oil lamp and a pocket knife.
You deliberate your response as follows. The practical goal of the questioner is to hammer the tent stake into the ground. You reason about the most useful alternative from the list of available options.

YOUR TURN:
'''


def getLogProbContinuation(initialSequence, continuation, preface = ''):
    """
    Helper for retrieving log probability of different response types from GPT-3.
    """
    initialSequence = preface + initialSequence
    response = openai.Completion.create(
            engine      = "text-davinci-003", 
            prompt      = initialSequence + " " + continuation,
            max_tokens  = 0,
            temperature = 1, 
            logprobs    = 0,
            echo        = True,
        ) 
    text_offsets = response.choices[0]['logprobs']['text_offset']
    cutIndex = text_offsets.index(max(i for i in text_offsets if i < len(initialSequence))) + 1
    endIndex = response.usage.total_tokens
    answerTokens = response.choices[0]["logprobs"]["tokens"][cutIndex:endIndex]
    answerTokenLogProbs = response.choices[0]["logprobs"]["token_logprobs"][cutIndex:endIndex] 
    meanAnswerLogProb = np.mean(answerTokenLogProbs)
    sentenceLogProb = np.sum(answerTokenLogProbs)


    return meanAnswerLogProb, sentenceLogProb, (endIndex - cutIndex)

def sampleContinuation(initialSequence, topk = 1, max_tokens = 32, preface = '', model='text-davinci-003'):
    """
    Helper for sampling predicted responses given prompts.
    """
    initialSequence = preface + "\n\nYour turn.\n" + initialSequence
    answers = []
    probs = []
    inputs = []

    print("Initial sequence of gpt 4 ", initialSequence)

    if (model == "text-davinci-003"):
        response = openai.Completion.create(
                engine      = "text-davinci-003", 
                prompt      = initialSequence,
                max_tokens  = max_tokens,
                temperature = 1, 
                logprobs    = 0,
                echo        = True,
                n           = topk,
            ) 
        print("response ", response)

        for i in range(topk):
            text_offsets = response.choices[i]['logprobs']['text_offset']
            cutIndex = text_offsets.index(max(i for i in text_offsets if i < len(initialSequence))) + 1
            try:
                endIndex = response.choices[i]["logprobs"]["tokens"].index("<|endoftext|>")
            # cases when eos token was not predicted
            except ValueError:
                print("No eos token ")
                endIndex = text_offsets.index(text_offsets[-1]) + 1
            answerTokens = response.choices[i]["logprobs"]["tokens"][cutIndex:endIndex]
            answerTokenLogProbs = response.choices[i]["logprobs"]["token_logprobs"][cutIndex:endIndex] 
            meanAnswerLogProb = np.mean(answerTokenLogProbs)
            probs.append(meanAnswerLogProb)
            answerSentence = "".join(answerTokens).replace("\n", "").strip()
            answers.append(answerSentence)
            print("AnswerSentence ", answerSentence)
        
    elif (model == 'gpt-4') or (model == 'gpt-3.5-turbo'):

        client = OpenAI()
        for i in range(topk):
            completion = client.chat.completions.create(
                model=model,
                logprobs=True,
                temperature=1,
                max_tokens=64,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": initialSequence}
                ]
            )
            response = completion.choices[0].message.content
            log_probs_obj = completion.choices[0].logprobs.content
            print("Length of log probs object ", len(log_probs_obj))
            log_probs_list = [l.logprob for l in log_probs_obj]
            tokens_list = [l.token for l in log_probs_obj]
            print("Number of generated words ", len(response.split(" ")))
            print("Log probs list ", log_probs_list, len(log_probs_list))
            print("Tokens list ", len(tokens_list), tokens_list)
            # print("Completion ")
            # pprint(completion)
            print("Model version ", completion.model)
            print("GPT -4 resp ", response)
            inputs.append(initialSequence)
            answers.append(response)
            probs.append(np.mean(log_probs_list))
    else:
        raise ValueError("Unknown model type")
    
    
    return answers, probs, completion.model, inputs


def processItem(item, wait = 0, preface = ''):
    # colnames_e1 = ["taciturn", "competitor", "sameCategory1", "sameCategory2", "sameCategory3", "otherCategory", "fullList_0", "fullList_1", "fullList_2", "fullList_3", "fullList_4", "fullList_5"]
    colnames = ["taciturn", "competitor", 'mostSimilar', "otherCategory", 'sameCategory_0', 'sameCategory_1', 'sameCategory_2', 'sameCategory_3',
       'sameCategory_4', 'sameCategory_5', 'sameCategory_6', 'sameCategory_7',
       'sameCategory_8', 'sameCategory_9', 'sameCategory_10',
       'sameCategory_11', 'sameCategory_12', 'fullList_0', 'fullList_1',
       'fullList_2', 'fullList_3', 'fullList_4', 'fullList_5', 'fullList_6',
       'fullList_7', 'fullList_8', 'fullList_9', 'fullList_10', 'fullList_11',
       'fullList_12', 'fullList_13', 'fullList_14', 'fullList_15',
       'fullList_16', 'fullList_17', 'fullList_18', 'fullList_19',
       'fullList_20', 'fullList_21', 'fullList_22', 'fullList_23']
    probs = {k: 0 for k in colnames}
    ppls = {k: 0 for k in colnames}
    exception_counter = {k: 0 for k in colnames}
    
    for a in colnames:
        # caqtch potential request timeouts
        for _ in range(2):
            try:
                prob, sent_ll, seq_length = getLogProbContinuation(item.context, item[a], preface)
                probs[a] = np.exp(prob)
                ppls[a] = np.exp(-sent_ll/seq_length)
                time.sleep(5)
                break
            except openai.error.ServiceUnavailableError:
                print("OpenAI connection error")
                exception_counter[a] += 1
                time.sleep(20)
                continue

        

    if any([v > 1 for v in list(exception_counter.values())]):
        raise ValueError("some probs were not computed!")

    # include averaging over different permutations
    avg_probs = [probs["taciturn"],
        probs["competitor"],
        probs["mostSimilar"],
        np.mean([probs[k] for k in [c for c in colnames if c.startswith("sameCategory")]]),
        probs["otherCategory"],
        np.mean([probs[k] for k in [c for c in colnames if c.startswith("fullList")]])
    ]
    # also compute perplexities
    avg_ppls = [ppls["taciturn"],
        ppls["competitor"],
        ppls["mostSimilar"],
        np.mean([ppls[k] for k in [c for c in colnames if c.startswith("sameCategory")]]),
        ppls["otherCategory"],
        np.mean([ppls[k] for k in [c for c in colnames if c.startswith("fullList")]])
    ]
    probs = avg_probs/np.sum(avg_probs)
    
    results = pd.DataFrame({
        "itemName": [item.itemName] * 6,
        "answer_type": ["taciturn", "competitor", "mostSimilar", "sameCategory", "otherCategory", "fullList"],
        "answer_type_prob_avg": probs,
        "answer_type_ppl": avg_ppls,
    }, index = [item.itemName]*6)
    
    # write out by item results, in case API stops responding
    results.to_csv(f"../data_paper_neural/results_post_cogsci/GPT3-davinci-003-predictions-e2-{item.itemName}.csv")
    time.sleep(wait) # to prevent overburdening free tier of OpenAI
    return(results)
    
def sampleAnswersForItem(item, wait = 0, preface = '', topk = 1, max_tokens = 32):
    """
    Helper for sampling formatting the responses.
    """
    answers = []
    probs = []
    inputs_list = []

    if preface == "diverseQA":
        preface = "EXAMPLE: " + item.CoT
    answer, prob, model_version, inputs = sampleContinuation(item.context_qa + " " + item.question, preface=preface, topk=topk, max_tokens=max_tokens, model="gpt-4") # item.context_fct_prompt
    answers.append(answer)
    probs.append(prob)
    inputs_list.append(inputs)
    results = pd.DataFrame(
        {
        "itemName"     : [item.itemName] * len(answers),
        "inputs": inputs_list,
        "predictions"  : answers,
        "probs"        : probs,  
        "model_version": [model_version] * len(answers),
        }
    )
    # flatten df in case more than one answer was sampled
    results = results.explode(["predictions", "probs"])
    # also save each item for the case of time outs
    results.to_csv(f"../data_paper_neural/results_post_cogsci/GPT4-samples-e3-{item.itemName}.csv", index=False)
    time.sleep(wait) # to prevent overburdening free tier of OpenAI
    return results    

if __name__ == "__main__":
    # parse cmd args
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--task", help = "which response should be retrieved from GPT3?", choices = ["probs", "samples"])
    parser.add_argument("-os", "--one_shot", help = "one shot or zero shot context for GPT3?", action="store_true")
    parser.add_argument("-n", "--num_samples", help = "number of samples to draw (WARNING: high credit cost)", nargs="?", default=1, type = int)
    parser.add_argument("-m", "--max_tokens", help = "maximal number of tokens to sample for each response (WARNING: high credit cost)", nargs="?", default=32, type = int)
    parser.add_argument("-e", "--experiment", help = "which experiment to process?", choices = ["e1", "e2", "e3_lowprior", "e3_highprior"], default = "e1")
    parser.add_argument("-pr", "--prompt", help="Type of prompt", default="zero-shot", type=str, choices=["zero-shot", "explanation", "example", "cot"])

    args = parser.parse_args()
    if args.experiment == "e1":
        few_shot_items = oneShotExample
        items = pd.read_csv('../experiments/free_production/trials/trials_LLMs_all_options_postprocessed.csv')
    elif args.experiment == "e2":
        few_shot_items = oneShotExampleE2
        items = pd.read_csv('../experiments/contextSensitive_free_production/trials/trials_e2_fctPrompt_fixedOrder.csv')
        # remove items that were used as one-shot example
        items = items[(items.itemName != "chair-repair") & (items.itemName != "chair-party")].reset_index()
        print("Number of items for E2: ", len(items))
    elif args.experiment == "e3_lowprior":
        few_shot_items = ""
        items = pd.read_csv('../experiments/04-priorSensitivity_free_production/trials/trials_pilot2_models.csv')
    elif args.experiment == "e3_highprior":
        few_shot_items = ""
        items = pd.read_csv('../experiments/04-priorSensitivity_free_production/trials/trials_pilot2_models.csv')
    else:
        raise ValueError("Unknown experiment number")
    
    # run scoring
    if args.task == "probs": 
        # one-shot vs zero shot
        if args.one_shot:
            # don't forget to use the appropriate prompt
            results_oneShotLearner = pd.concat([processItem(items.loc[i], wait = 40, preface = examples[args.experiment][args.prompt]) for i in range(len(items))])
            results_oneShotLearner.to_csv('../data_paper_neural/results_post_cogsci/GPT3-davinci-003-predictions-oneShotLearner-e2.csv', index = False)
        else:
            results_zeroShotLearner = pd.concat([processItem(items.loc[i], wait = 40, preface = "") for i in range(len(items))])
            results_zeroShotLearner.to_csv('../data_paper_neural/results_post_cogsci/GPT3-davinci-003-predictions-overinfo-zeroShotLearner-e2.csv', index = False)
    # run sampling
    elif args.task == "samples":
        # one shot
        if args.one_shot:
            # don't forget to use the appropriate prompt
            # samples_oneShotLearner = pd.concat([sampleAnswersForItem(items.loc[i], wait = 45, preface = oneShotExampleE2_mismatch, topk=args.num_samples, max_tokens=args.max_tokens) for i in range(len(items))])
            samples_oneShotLearner = pd.concat([sampleAnswersForItem(items.loc[i], wait = 45, preface = examples[args.experiment][args.prompt], topk=args.num_samples, max_tokens=args.max_tokens) for i in range(len(items))])
            samples_oneShotLearner.to_csv(f'../data_paper_neural/results_post_cogsci/GPT4-samples-{args.prompt}_{args.experiment}_{timestamp}.csv', index = False)
        # vs zero shot
        else:
            
            samples_zeroShotLearner = pd.concat([sampleAnswersForItem(items.loc[i], wait = 45, preface = "", topk=args.num_samples, max_tokens=args.max_tokens) for i in range(len(items))])
            samples_zeroShotLearner.to_csv(f'../data_paper_neural/results_post_cogsci/GPT4-samples-{args.prompt}-{args.experiment}_{timestamp}.csv', index = False)

    else:
        raise ValueError("Unknown task type")
