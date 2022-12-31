# Text production experiment on over-informative answers to preference-signaling questions

This is an online experiment using [magpie](https://magpie-experiments.org/).

You can inspect a live version of the free typing experiment [here](https://magpie-ea.github.io/magpie3-qa-overinfo-free-production/experiments/free_production/).

You can inspect a live version of the prior elicitation experiment [here](https://magpie3-qa-overinformative-priors.netlify.app/).

### Local execution 

First, clone the repository and set up the project with `npm install`.

To run the project locally, run `npm run serve`.

To build the project for deployment (e.g. to Netlify), run `npm run build`.

For more information, see the [manual](https://magpie-experiments.org/).


# LLMs

This repository also contains code for sampling responses to the same questions used in the human experiment from neural models made available on Huggingface hub. Additionally, pretrained neural language models are used in order to score different types of overinformative responses (of the same types used in the classification of the human data) under these models. 

The directory `code` contains respective scripts and results in the directory `code/results`. In order to obtain results from trained neural models, navigate into `code` and run the following (*WARNING*: might trigger download of large weight files): 

* `python QA_models_answer_sampling.py -m="valhalla/t5-base-qa-qg-hl" -o="results/trials_LLMs_valhalla_t5_base_qa_qg_hl.csv"  -p="../experiments/free_production/trials/trials_LLMs_postprocessed.csv" -t="lm_sampling" -topk=5 -nb=5` to obtain top 5 generations from a Huggingface T5 language model finetuned for abstractive question answering. See `python QA_models_answer_sampling.py --help` for information on command line arguments.
* `python QA_models_answer_sampling.py -m="valhalla/t5-base-qa-qg-hl" -o="results/trials_LLMs_valhalla_t5_base_qa_qg_hl.csv"  -p="../experiments/free_production/trials/trials_LLMs_postprocessed.csv" -t="lm_prob"` to obtain scores of provided answers of different types under the finetuned T5 language model.
* `python QA_models_answer_sampling.py -m="bert-large-uncased-whole-word-masking-finetuned-squad" -o="results/trials_LLMs_bert-large-uncased-whole-word-masking-finetuned-squad.csv"  -p="../experiments/free_production/trials/trials_LLMs_postprocessed.csv" -t="lm_prob" -topk=5` to obtain top 5 spans predicted by BERT Large finetuned for extractive QA on the SQuAD dataset. 