"""
Helper script for building together full contexts from modular vignette csvs used in experiments
for running neural model evaluations.
"""
import pandas as pd 
import argparse
import random
import itertools

def convert_modular_to_llm_format(path, output, expt=1):
    """
    Creates full context strings from modular csvs with alternatives listed separately.
    Also creates all response options in a way taht is maximally advanageous
    to the performance of LLMs with respect to our hypothesis,
    i.e., by putting the competitor first in the list of options and scrambling the order
    of options in the full list response option compared to the context. This
    decreases the likelihood of the full list option in favor of other response options.

    Arguments:
    ---------
    path: str
        Path to input raw file.
    output: str
        Path where to save processed file.
    """
    def return_options(row):
        opts = []
        for r in row["shuffled_options_list"]:
            opts.append([row[i] for i in r])
        return opts

    def return_options_sameCat(row):
        opts = []
        for r in row["shuffled_sameCat_list"]:
            opts.append([row[i] for i in r])
        return opts

    df = pd.read_csv(path)

    df_out = df.copy()
    if expt == 1:
        # create options string in a set order
        options = df_out["competitor"] + ", " + df_out["sameCategory"] + ", and " + df_out["otherCategory"] + ". "
        # shuffle options and create all possible full list orders
        full_list_orders = list(itertools.permutations(["competitor", "sameCategory", "otherCategory"]))
        # options_list = [random.sample(["competitor", "sameCategory", "otherCategory"], 3) for i in range(len(df))]
        df["shuffled_options_list"] = [full_list_orders] * len(df) #df.apply(lambda x: random.shuffle(options_list))
        df["shuffled_options"] = df.apply(lambda x: return_options(x), axis = 1)
        print("head ", df.head())
        df["shuffled_options_string"] = df["shuffled_options"].apply(lambda s: [", ".join(i) for i in s])
        # put together context
        df_out["context"] = df_out["vignette_start"] + " " + options + df_out["vignette_continuation"] + " " + df_out["question"] + " You reply:"
        # replace newline chars (esp relevant for GPT-3)
        df_out["context"] = df_out["context"].apply(lambda s: s.replace("\\n", ""))
        # geneare context wihtout the question for the QA models
        df_out["context_qa"] = df_out["vignette_start"] + " " + options + df_out["vignette_continuation"]
        df_out["context_qa"] = df_out["context_qa"].apply(lambda s: s.replace("\\n", ""))
        # construct response options (may require some manual fine-tuning of the taciturn formulation)
        df_out["taciturn"] = "I'm sorry, we don't have " + df_out["itemQuestion"] + "."
        df_out["competitor"] = df_out["taciturn"] + " We have " + df["competitor"] + "."
        df_out["sameCategory1"] = df_out["taciturn"] + " We have " + df["competitor"] + " and " + df["sameCategory"] + "."
        df_out["sameCategory2"] = df_out["taciturn"] + " We have " + df["sameCategory"] + "."
        df_out["sameCategory3"] = df_out["taciturn"] + " We have " + df["sameCategory"] + " and " + df["competitor"] + "."
        df_out["otherCategory"] = df_out["taciturn"] + " We have " + df["otherCategory"] + "."
        for i in range(len(full_list_orders)):
            df[f"shuffled_options_string_{i}"] = df["shuffled_options_string"].apply(lambda s: s[i])
            df_out[f"fullList_{i}"] = df_out["taciturn"] + " We have " + df[f"shuffled_options_string_{i}"] + "."

        df_out = df_out[["itemName", "settingName", "context", "context_qa", "question", "taciturn", "competitor", "sameCategory1", "sameCategory2", "sameCategory3", "otherCategory", "fullList_0",  "fullList_1",  "fullList_2",  "fullList_3",  "fullList_4",  "fullList_5"]]
    
    else:
        # create options string in a set order
        options = df_out["competitor"] + ", " + df_out["mostSimilar"] + ", " + df_out["sameCategory"] + ", and " + df_out["otherCategory"] + ". "
        # shuffle options and create all possible full list orders
        full_list_orders = list(itertools.permutations(["competitor", "mostSimilar", "sameCategory", "otherCategory"]))
        df["shuffled_options_list"] = [full_list_orders] * len(df) 
        df["shuffled_options"] = df.apply(lambda x: return_options(x), axis = 1)
        print("head ", df.head())
        df["shuffled_options_string"] = df["shuffled_options"].apply(lambda s: [", ".join(i) for i in s])
        # same for sameCat 
        sameCat_list_orders = list(itertools.permutations(["competitor", "mostSimilar", "sameCategory"]))
        df["shuffled_sameCat_list"] = [sameCat_list_orders] * len(df) 
        df["shuffled_options_sameCat"] = df.apply(lambda x: return_options_sameCat(x), axis = 1)
        print("head ", df.head())
        df["shuffled_sameCat_string"] = df["shuffled_options_sameCat"].apply(lambda s: [", ".join(i) for i in s])
        
        # put together context
        df_out["context"] = df_out["vignette_start"] + " " + options + df_out["vignette_continuation"] + " " + df_out["question"] + " You reply:"
        # replace newline chars (esp relevant for GPT-3)
        df_out["context"] = df_out["context"].apply(lambda s: s.replace("\\n", ""))
        # geneare context wihtout the question for the QA models
        df_out["context_qa"] = df_out["vignette_start"] + " " + options + df_out["vignette_continuation"]
        df_out["context_qa"] = df_out["context_qa"].apply(lambda s: s.replace("\\n", ""))
        # construct response options (may require some manual fine-tuning of the taciturn formulation)
        df_out["taciturn"] = "I'm sorry, I don't have " + df_out["itemQuestion"] + "."
        df_out["competitor"] = "No, but I have " + df["competitor"] + "." #  df_out["taciturn"] + 
        df_out["mostSimilar"] = "No, but I have " + df["mostSimilar"] + "."
        # add same Cat options
        for i in range(len(sameCat_list_orders)):
            df[f"shuffled_sameCat_string_{i}"] = df["shuffled_sameCat_string"].apply(lambda s: s[i])
            df_out[f"sameCategory_{i}"] = "No, but I have " + df[f"shuffled_sameCat_string_{i}"] + "."
        # add options with one / two items
        df_out[f"sameCategory_{i+1}"] = "No, but I have " + df["competitor"] + " and " + df["sameCategory"]  + "."
        df_out[f"sameCategory_{i+2}"] = "No, but I have " + df["sameCategory"] + " and " + df["competitor"]  + "."
        df_out[f"sameCategory_{i+3}"] = "No, but I have " + df["sameCategory"] + "."
        df_out[f"sameCategory_{i+4}"] = "No, but I have " + df["competitor"] + " and " + df["mostSimilar"]  + "."
        df_out[f"sameCategory_{i+5}"] = "No, but I have " + df["mostSimilar"] + " and " + df["competitor"]  + "."
        df_out[f"sameCategory_{i+6}"] = "No, but I have " + df["mostSimilar"] + " and " + df["sameCategory"]  + "."
        df_out[f"sameCategory_{i+7}"] = "No, but I have " + df["sameCategory"] + " and " + df["mostSimilar"]  + "."

        df_out["otherCategory"] = "No, but I have " + df["otherCategory"] + "."
        for i in range(len(full_list_orders)):
            df[f"shuffled_options_string_{i}"] = df["shuffled_options_string"].apply(lambda s: s[i])
            df_out[f"fullList_{i}"] = "No, but I have " + df[f"shuffled_options_string_{i}"] + "."


        print("All columns in final df ", df_out.columns)
        df_out = df_out[df_out.columns[~df_out.columns.isin(['vignette_start','vignette_continuation', 'priorElicitation_context', 'priorElicitation_question', 'answer_template', 'itemQuestion', 'sameCategory', 'competitor_context1',
       'competitor_context2', 'correct_response'])]]
        # df_out = df_out[["itemName", "settingName", "context", "context_qa", "question", "taciturn", "competitor", "sameCategory1", "sameCategory2", "sameCategory3", "otherCategory", "fullList_0",  "fullList_1",  "fullList_2",  "fullList_3",  "fullList_4",  "fullList_5"]]
    

    df_out.to_csv(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help = "path to file to convert")
    parser.add_argument("-o", "--output", help = "path to save processed output file to")
    parser.add_argument("-e", "--experiment", help = "number of expt for which data is processed", type=int)

    args = parser.parse_args()

    convert_modular_to_llm_format(args.path, args.output, args.experiment)