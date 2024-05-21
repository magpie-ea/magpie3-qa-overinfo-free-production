"""
Helper script for assignening the mentioned options for E2 
(i.e., comptetitor 1, competitor 2, mostSimilar, otherCategory)
"""

import pandas as pd
import os

# read all e2 files
results_files = os.listdir("../data_paper_neural/results_post_cogsci/annotated/")
e2_results = [f for f in results_files if "e2" in f]
item_options = pd.read_csv("../data_paper_neural/e2_ItemCategorization.csv")
e2_vignettes = pd.read_csv("../data_paper_neural/e2_vignettes.csv")
print(item_options.head())

def assign_options(r):
    """
    Given row with raw response and manually assigned category,
    assign the single mentioned options.
    """
    mentioned_options = []
    mentioned_labels = []

    category = r["category"]
    item_name = r["itemName"]
    print("item name ", item_name)
    if not "chair" in item_name:
        context_num = e2_vignettes[e2_vignettes["itemName"] == item_name]["context_nr"].values[0]
        setting_name = e2_vignettes[e2_vignettes["itemName"] == item_name]["settingName"].values[0]
        print(context_num)
        options = item_options[item_options["settingName"] == setting_name]
    print(f"Category {category}, item name {item_name}")
    response = r["predictions"]

    if (item_name == "chair-repair") | (item_name == "chair-party"):
        mentioned_labels.append("prompt")
        mentioned_options.append("prompt")

    elif (category == "competitor") & (context_num == "context1"):
        option = options[options["global_category"] == "competitor_c1"]["response_option"].values[0]
        label = "competitor_c1"
        print("---- Competitor 1 ", option)
        mentioned_options.append(option)
        mentioned_labels.append(label)
    
    elif (category == "competitor") & (context_num == "context2"):
        option = options[options["global_category"] == "competitor_c2"]["response_option"].values[0]
        print("---- Competitor 2 ", option)
        label = "competitor_c2"
        mentioned_options.append(option)
        mentioned_labels.append(label)
    elif (category == "mostSimilar"):
        option = options[options["global_category"] == "mostSimilar"]["response_option"].values[0]
        print("---- Most similar ", option)
        label = "mostSimilar"
        mentioned_options.append(option)
        mentioned_labels.append(label)
    elif (category == "otherCategory"):
        option = options[options["global_category"] == "otherCategory"]["response_option"].values[0]
        print("---- Other category ", option)
        label = "otherCategory"
        mentioned_options.append(option)
        mentioned_labels.append(label)
    else:
        print("Response: ", response)
        # now process raw responses (for sameCategory and other responses)
        for j, o in enumerate(options["response_option_str"]):
            if o in response:
                mentioned_options.append(options.iloc[j]["response_option"])
                label = options.iloc[j]["global_category"]
                mentioned_labels.append(label)
                print("---- Raw ", o, label)

    options_str = ", ".join(mentioned_options)
    labels_str = ", ".join(mentioned_labels)

    return options_str, labels_str

if __name__ == "__main__":
    for f in e2_results:
        print(f"#### File {f}")
        d = pd.read_csv("../data_paper_neural/results_post_cogsci/annotated/" + f)
        path_out = "../data_paper_neural/results_post_cogsci/annotated/processed_exp2/" + f
        d_out = d.copy()
        response_option = []
        global_category = []

        for i, r in d_out.iterrows():
            mentioned_options, mentioned_labels = assign_options(r)
            response_option.append(mentioned_options)
            global_category.append (mentioned_labels)
        
        d_out["response_option"] = response_option
        d_out["global_category"] = global_category

        d_out.to_csv(path_out, index=False)
