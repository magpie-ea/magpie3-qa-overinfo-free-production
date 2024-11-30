"""
Script for re-classifying responses for the PhilTrans revisions.
"""

import pandas as pd
import os
import argparse

def assign_category(r, expt='e2', answer_column="option_category"):
    """
    Function for assigning answer category.
    """
    # get the column with the annotated mentioned options
    try:
       mentioned_options = r[answer_column].split(", ")
    # when no option mentioned, take whatever was already annotated
    except:
        response_category = r["category"]
        print('response cat ----- ', response_category)
        if response_category == "other":
            response_category = "other_response"
        return response_category

    # check which options occur in the response
    response_category = "other_response"
    # no mentioned alternative -- taciturn 
    if len(mentioned_options) == 0:
        response_category = "taciturn"
    # one mentioned alternative -- response category is the mentioned alternative
    elif len(mentioned_options) == 1:
        response_category = mentioned_options[0]
    # full list options for e3
    elif len(mentioned_options) == 3:
        if expt == 'e2':
            response_category = "fullList"
    elif len(mentioned_options) == 4:
        if expt == 'e3':
            response_category = "fullList"
    else:
        if expt == "e2":
            if ("competitor" in mentioned_options) and ("sameCategory" in mentioned_options):
                response_category = "sameCategory"
            ### this is the new categorization
            elif "otherCategory" in mentioned_options: 
                response_category = "otherCategory" 
            else:
                response_category = "other_response"
        else:
            ### this is the new categorization
            if "otherCategory" in mentioned_options:
                response_category = "otherCategory"
            elif (len(mentioned_options) == 2) and ("competitor_c1" in mentioned_options) and ("competitor_c2" in mentioned_options):
                response_category = "sameCategory"
            elif "mostSimilar" in mentioned_options:
                response_category = "mostSimilar"
            else:
                response_category = "other_response"
            
    return response_category
    


def main(results_dir="../results/", file_name="results.csv", separator=",", answer_column="option_category", experiment=None):
    """
    Script for categorizing free production responses 
    of E2 or E3. 
    """
    # read results file
    d = pd.read_csv(
        os.path.join(results_dir, file_name), 
        sep=separator
    )
    # identidy experiment
    if experiment is None:
        if "e2" in results_dir:
            experiment = "e2"
        elif "e3" in results_dir:
            experiment = "e3"
        else:
            raise ValueError("Results path must contain string if it is for e2 or e3")
    
    # construct path for classified df
    file_name_out = file_name.split(".")[0] + "_philtrans_categorized.csv"
    path_out = os.path.join(results_dir, file_name_out)

    # iterate over rows and classify responses
    for i, r in d.iterrows():
            response_category = assign_category(r, expt=experiment, answer_column=answer_column)
            # record 
            dict_r = r.to_dict()
            dict_r["new_category"] = response_category
            
            result = pd.DataFrame(dict_r, index=[0])
            result.to_csv(
                path_out,
                sep=",",
                index=False,
                mode="a",
                header=not os.path.exists(
                    path_out
                )
            )

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results_dir",
        type=str,
        default=".",
        help="Path to directory with results files to be processed.",
    )
    parser.add_argument(
        "--file_name",
        type=str,
        default="qa_evaluation.csv",
        help="Name of raw results file.",
    )
    parser.add_argument(
        "--separator",
        type=str,
        default="|",
        help="Separator for the results file.",
    )
    parser.add_argument(
        "--answer_column",
        type=str,
        default="pragmatic_answer",
        help="Name of column with answers to be classified.",
    )

    parser.add_argument(
        "--experiment",
        type=str,
        default=None,
        help="Experiment number.",
    )

    args = parser.parse_args()

    # print values of all arguments
    print("Arguments:")
    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")

    main(
        **vars(args)
    )    