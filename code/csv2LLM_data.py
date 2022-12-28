"""
Helper script for building together full contexts from modular vignette csvs used in experiments
for running neural model evaluations.
"""
import pandas as pd 
import argparse
import random

def convert_modular_to_llm_format(path, output):
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
        return [row[i] for i in row["shuffled_options_list"]]

    df = pd.read_csv(path)

    df_out = df.copy()
    # create options string in a set order
    options = df_out["competitor"] + ", " + df_out["sameCategory"] + ", and " + df_out["otherCategory"] + ". "
    # shuffle options
    options_list = [random.sample(["competitor", "sameCategory", "otherCategory"], 3) for i in range(len(df))]
    df["shuffled_options_list"] = options_list #df.apply(lambda x: random.shuffle(options_list))
    print("head ", df.head())
    df["shuffled_options"] = df.apply(lambda x: return_options(x), axis = 1)
    df["shuffled_options_string"] = df["shuffled_options"].apply(lambda s: ", ".join(s))
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
    df_out["sameCategory"] = df_out["taciturn"] + " We have " + df["competitor"] + " and " + df["sameCategory"] + "."
    df_out["otherCategory"] = df_out["taciturn"] + " We have " + df["otherCategory"] + "."
    df_out["fullList"] = df_out["taciturn"] + " We have " + df["shuffled_options_string"] + "."

    df_out = df_out[["itemName", "settingName", "context", "context_qa", "question", "taciturn", "competitor", "sameCategory", "otherCategory", "fullList"]]

    df_out.to_csv(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help = "path to file to convert")
    parser.add_argument("-o", "--output", help = "path to save processed output file to")

    args = parser.parse_args()

    convert_modular_to_llm_format(args.path, args.output)