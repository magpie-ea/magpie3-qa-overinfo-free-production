# Text production experiment on over-informative answers to preference-signaling questions

This is an online experiment using [magpie](https://magpie-experiments.org/).

You can inspect a live version of the free typing experiment [here](https://magpie-ea.github.io/magpie3-qa-overinfo-free-production/experiments/free_production/).

You can inspect a live version of the prior elicitation experiment [here](https://magpie3-qa-overinformative-priors.netlify.app/).

You can inspect the context-sensitivity free produciont experiment (E2) [here](https://magpie-ea.github.io/magpie3-qa-overinfo-free-production/experiments/contextSensitive_free_production/).

### Local execution 

First, clone the repository and set up the project with `npm install`.

To run the project locally, run `npm run serve`.

To build the project for deployment (e.g. to Netlify), run `npm run build`.

For more information, see the [manual](https://magpie-experiments.org/).


# Neural models

This repository also contains code for sampling responses to the same questions used in the human experiment from neural models. Additionally, pretrained neural language models are used in order to score different types of overinformative responses (of the same types used in the classification of the human data) under these models. 

The directory `code` contains scripts for sampling results from models made available on Huggingface hub. The summarized results in the directory `data_paper_neural`. For raw files, contact Polina. 


### `code`
Directory containing scripts for sampling neural model results. Both scripts allow to both sample responses and to score different types of overinformative responses (of the same types used in the classification of the human data) under pretrained neural language models. 

* `GPT-overinformative-answers.py`: script for querying GPT-3 through the OpenAI API. Requires a .env file with access credentials.
* `QA_models_answer_sampling.py`: script for querying extractive and generative models from Huggingface. 
* `csv2LLM_data.py`: helper script for converting experimental stimuli csv to csvs containing all answer options for scoring with LMs.
* `csv2txt.py`: helper for pretty-printing stimuli csv as text for easier reading.
* `postprocess_gpt2.py`: helper for removing prompt from completion output of GPT-2.
* `T0_inference.sh`: job script for running the script described below on slurm for the T0 model (too large to run inference locally).

In order to obtain results from trained neural models from the Huggingface Hub, navigate into `code` and run the following (*WARNING*: might trigger download of large weight files): 

* `python QA_models_answer_sampling.py -m="valhalla/t5-base-qa-qg-hl" -o="results/trials_LLMs_valhalla_t5_base_qa_qg_hl.csv"  -p="../experiments/free_production/trials/trials_LLMs_postprocessed.csv" -t="lm_sampling" -topk=5 -nb=5` to obtain top 5 generations from a Huggingface T5 language model finetuned for abstractive question answering. See `python QA_models_answer_sampling.py --help` for information on command line arguments.
* `python QA_models_answer_sampling.py -m="valhalla/t5-base-qa-qg-hl" -o="results/trials_LLMs_valhalla_t5_base_qa_qg_hl.csv"  -p="../experiments/free_production/trials/trials_LLMs_postprocessed.csv" -t="lm_prob"` to obtain scores of provided answers of different types under the finetuned T5 language model.
* `python QA_models_answer_sampling.py -m="bert-large-uncased-whole-word-masking-finetuned-squad" -o="results/trials_LLMs_bert-large-uncased-whole-word-masking-finetuned-squad.csv"  -p="../experiments/free_production/trials/trials_LLMs_postprocessed.csv" -t="qa" -topk=5` to obtain top 5 spans predicted by BERT Large finetuned for extractive QA on the SQuAD dataset. 

The list of model tags to retrieve respective models from Huggingface can be found in `data_paper_neural/e1_SA_model_proportions.csv`. The model cards of Huggingface describe the datasets on which the models were fine-tuned or trained.

### `data_paper_neural`

This directory contains results of querying the various neural models on both experiments as well as raw GPT-3 data and some helper summaries, reported in cogsci.

* `e1_gpt3_byPrompt_raw.csv`: raw sampling results, annotated with different response categories, produced by GPT-3 in different prompting conditions on experiment 1 vignettes. 
* `e1_gpt3_byPrompt_summary.csv`: summary of different response categories produced by GPT-3 in different prompting conditions, averaged over experiment 1 vignettes. 
* `e1_SA_gpt3_probs.csv`: probabilities of different response types computed under zero-shot and one-shot CoT GPT-3 for experiment 1 vignettes.
* `e1_SA_model_probs.csv`: probabilities of different response types computed under zero-shot prompted language models other than GPT-3 for experiment 1 vignettes.
* `e1_SA_model_proportions.csv`: proportions of response types in the responses sampled from different extractive and generative models for experiment 1 vignettes. These are described in terms of deviation from human proportions for the respective type. The "absolute_diff" column indicates the average absolute deviation from human proportions by-model. 
* `e2_gpt3_byPrompt_byCategory_raw.csv`: raw sampling results, annotated with different response categories and response options sampled from GPT-3 given different prompts for experiment 2 vignettes.
* `e2_gpt3_byPrompt_byCategory_summary.csv`: summary of different response categories of responses sampled from GPT-3 given different prompts for experiment 2 vignettes.
* `e2_gpt3_byPrompt_byContext_summary.csv`:  by-context summary of option type mentions in responses sampled from GPT-3 given different prompts for experiment 2 vignettes.
* `e2_human_summary_wide.csv`: wide summary of human E2 results, displaying response option proportions by-context.
* `e2_human_tidy.csv`: human E2 results, post exclusions, annotated with response categories, and split into rows containing single annotated suggested alternatives.
* `e2_ItemCategorization.csv`: file mapping different alternatives in each vignette to their option type for the respective vignette.
* `e2_SA_gpt3_onE1prompt.csv`: summary of different response categories of responses sampled from GPT-3 given different prompts used for experiment 1. 
* `e2_SA_gpt3_probs.csv`: probabilities of different response types computed under zero-shot and one-shot CoT GPT-3 for experiment 2 vignettes.
* `e2_SA_model_probs.csv`: probabilities of different response types computed under zero-shot prompted language models other than GPT-3 for experiment 2 vignettes.
* `e2_SA_model_proportions.csv`: proportions of response types in the responses sampled from different extractive and generative models for experiment 2 vignettes. These are described in terms of deviation from human proportions for the respective type. The "absolute_diff" column indicates the average absolute deviation from human proportions by-model. 
* `e2_vignettes.csv`: mapping of vinette contexts to their numbers.
* `QA_neural_models_categorized_samples_E1.csv`: raw categorized file containing samples from extractive and generative models for experiment 1. Note that all responses which identifiably mentioned alternative options for the question were annotated as acceptable answers, even if, e.g., they contained longer spans or repeated parts of the context. 'yes' responses were also excluded from model analyses described above, akin to human data analyses.
* `QA_neural_models_categorized_samples_E2.csv`: raw categorized file containing samples from extractive and generative models for experiment 2 *when prompted on the E2 one-shot context*. Note that all responses which identifiably mentioned alternative options for the question were annotated as acceptable answers, even if, e.g., they contained longer spans or repeated parts of the context. 'yes' responses were also excluded from model analyses described above, akin to human data analyses.
* `QA_neural_models_categorized_samples_promptE2.csv`: raw categorized file containing samples from extractive and generative models for experiment 2. Note that all responses which identifiably mentioned alternative options for the question were annotated as acceptable answers, even if, e.g., they contained longer spans or repeated parts of the context. 'yes' responses were also excluded from model analyses described above, akin to human data analyses.

### `data+analysis`

Files contained directly in this top level directory are pilot experimental results, including from pilot prior elicitation results. There are .md files and directories for all .Rmd files which were knitted.

* `01_main_free_typing_analysis.Rmd`: free production E1 pilot analysis
* `02_main_prior_elicitation_analysis.Rmd`: analysis of prior elicitation experiment ("conditional likability rating") pilot 1 for E1.
* `03_pilot2_prior_elicitation_analysis.Rmd`: analysis of prior elicitation experiment ("conditional likability rating") pilot 2 for E1.
* `04_pilot3_prior_elicitation_analysis.Rmd`: analysis of prior elicitation experiment ("conditional likability rating") pilot 3 for E1.
* `05_main_free_typing_cogsci_analysis.Rmd`: full analysis of full free production E1.
* `06_expt_vs_LLMs_analysis.Rmd`: script for comparing neural model results to human data. Focuses on plotting along different dimensions. Includes anayses of different neural models.
* `06_expt_vs_gpt3_exporation.Rmd`: script focusing on comparing GPT-3 to human results. 
* `07_main_contextSensitive_pilot_analysis.Rmd`: full E2 analysis script.
* `08_cogsci_write_up.Rmd`: intermediate summary of pre-cosci results on full E1, pilot E2 and pilot neural model results.
* `data_exploration.r`: legacy E1 analysis script.

#### `cogsci`

Minimal analysis files uplaoded as supplementary materials.

* `01_e1_main_free_typing_cogsci_analysis.Rmd`: the script for the analysis of the human data from experiment 1. The corresponding anonymized data can be found in the `data` directory described below.
* `02_e2_main_contextSensitivity_analysis.Rmd`: the script for the analysis of the human data from experiment 2. The corresponding anonymized data can be found in the `data` directory described below.
* `03_LLMs_analysis_cogsci.Rmd`: the script contains utilities for inspecting data drawn from neural models, specifically GPT-3, and plotting / analysing it against the human data. The `data_paper_neural` contains the sampled model results.

#### `data`

Anonymized, categorized, possibly post-exclusion files from human experiments. The main files are listed below.

* `results_105_QA_overinfo-contextDependent-freeTyping-pilot4-130-categorized.csv`: full E2 dataset (annotated and anonymized)
* `results_QA-overinfo-freeTyping-cogsci_full_categorized_cleaned.csv`: full E1 dataset (anonymized, annotated, post exclusions)
* `results_QA-overinfo-freeTyping-cogsci_full_categorized.csv`: full E1 dataset (anonymized, annotated, pre exclusions)
* `results_100_QA-overinformative-priorElicitation-magpie-pilot03_anonymized.csv`: prior elicitation results from pilot 3 (for E1).

#### `viz`

Directory containing exported plots from various analyses. The plots used for cogsci are `e1_4prompts.pdf`, `e2_byPrompt_cogsci_final.pdf`.

### `experiments`

This directory contains experiments implemented in magpie (see above for live hosted versions and local hosting instructions).

* `contextSensitive_free_production`: directory with experiment 2 (free production given vignettes which were paired and presented same alternatives in two different contexts, manipulating their functional relevance)
* `free_production`: directory with experiment 1 (free production given different options in contexts)
* `prior_elicitation`: prior / conditional likability / similarity rating of items used in E1. (slider rating experiment)