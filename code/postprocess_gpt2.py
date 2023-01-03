import pandas as pd
import argparse 
from tqdm import tqdm

def postprocess_gpt2(path, output_path):
    """
    Utility helper for postprocessing GPT-2 samples (with and without few shot prompting).
    Removes the context from the generated response for easier categorization and inspection.
    """
    df = pd.read_csv(path)

    few_shot = False

    few_shot_context = """
    You are hosting a barbecue party. You are standing behind the barbecue. You have the following goods to offer: pork sausages, vegan burgers, grilled potatoes and beef burgers.
    You reason about what that person most likely wanted to have. That they asked for grilled zucchini suggests that they might want vegetarian food. From the items you have pork sausages and beef burgers are least likely to satisfy the persons desires. Vegan burgers and grilled potatoes come much closer. Grilled potatoes are most similar to grilled zucchini.
     Someone asks: Do you have grilled zucchini? You reply: I'm sorry, I don't have any grilled zucchini. But I do have some grilled potatoes. Now consider a different situation."""
    if "fewShot" in path:
        few_shot = True
    
    cleaned_predictions = []
    for i, r in tqdm(df[["context_qa", "question", "predictions"]].iterrows()):
        if few_shot:
            cleaned_pred = r["predictions"].replace(few_shot_context, "").replace(r["context_qa"], "").replace(r["question"] , "").replace("You reply: ", "").replace("Q: ", "").replace("A: ", "").strip()
            print("CLEANED PRED ", cleaned_pred)
            cleaned_predictions.append(cleaned_pred)
        else:
            cleaned_pred = r["predictions"].replace(r["context_qa"], "").replace(r["question"] , "").replace("You reply: ", "").replace("Q: ", "").replace("A: ", "").strip()
            print("CLEANED PRED ", cleaned_pred)
            cleaned_predictions.append(cleaned_pred)

    df["predictions_cleaned"] = cleaned_predictions

    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", help = "path to input file")
    parser.add_argument("-o", "--output", help = "path to save processed file to")
    
    args = parser.parse_args()

    postprocess_gpt2(args.path, args.output)