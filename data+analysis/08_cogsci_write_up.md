QA CogSci write up
================
PT
2023-01-15

# Paper Outline: Comparing Overinformative Answers to Yes/No Questions by Humans and Neural Language Models

## general framing

### goal:

- understand patterns in human over-informative answers to polar
  question
  - as a partial window into question understanding / interpretation
  - with an eye towards building human-like conversational agents

### main contributions:

- human data suggesting over-informative answer patterns are
  context-dependent and utility-based (not fixed similarity heuristic)
- investigate whether / why state-of-the-art LMs don’t necessarily
  mirror human-like patterns

## human experiments

1.  [**E1**](https://magpie-ea.github.io/magpie3-qa-overinfo-free-production/experiments/free_production/):
    question signals desirable object; context is (relatively)
    uninformative; alternative objects are classified intuitively by
    likability / similarity relative to the target. Free production
    answer generation (as before).

- design: three alternatives in context (competitor, same category,
  other category).
- goal: collect human natural data, provide dataset.
- hypothesis: given questions signaling the goal, humans are
  overinformative and offer the competitor most, while having a low
  propensity towards full list responses.
- answers classified into different categories by their information
  content (taciturn, competitor, sameCategory, otherCategory, fullList).

2.  [**E2**](https://magpie-ea.github.io/magpie3-qa-overinfo-free-production/experiments/contextSensitive_free_production/):
    context signals broader action relevance; pairs of items: same
    question / target and same alternatives, but different “problems” of
    the questioner. Free production answer generation.

- design: pairs of contexts. Alternatives of following types are the
  same for both (x4): most similar to target (conceptually, not
  anticipated to be the competitor in either context), competitor for
  one context, competitor for other context, other category (distractor,
  not considered relevant in either context).
- example vignette pair:
  1.  You have a new neighbor who will be moving into the apartment on
      the ground floor of your house. You see your new neighbor cleaning
      his windows before moving in. When walking out of the building you
      see him trying to reach the top of the window that he is cleaning.
      In your apartment you have a ladder, a stool, a leather recliner
      and a broom. When your neighbor sees you in front of the house,
      they greet you and ask: Do you have a chair?
  2.  Your neighbor is hosting a dinner party with a lot of guests at
      their apartment on the ground floor. The house does not have an
      elevator. You are also invited. As more guests arrive, your
      neighbor runs out of seating options. In your apartment on the
      third floor of the house you have a ladder, a stool, a leather
      recliner and a broom. Your neighbor asks: Do you have a chair?
  3.  most similar = recliner, competitor context 1 = ladder, competitor
      context 2 = stool, other category = broom. Full list of items can
      be found
      [here](https://github.com/magpie-ea/magpie3-qa-overinfo-free-production/blob/main/experiments/contextSensitive_free_production/trials/trials_split_cogsci_pilot4.csv).
- goal: collect human natural data, provide dataset.
- hypothesis: given the same question and alternatives, humans provide
  different responses depending on the action / functional relevance in
  context, i.e., show action relevance sensitivity. They will offer the
  respective competitor most, while having a lower propensity towards
  offering the other options or full lists.
- answers classified into 1) different categories depending on their
  information content (as in E1) and 2) as mentioning the alternatives
  classified into mostSimilar, competitor_context1, competitor_context2,
  otherCategory.

### results

- [Experiment
  1](https://github.com/magpie-ea/magpie3-qa-overinfo-free-production/blob/main/data%2Banalysis/05_main_free_typing_cogsci_analysis.md):
  157 subjects / 594 responses analysed, 15 pairs of vignettes

![global response type proportions in
E1](05_main_free_typing_cogsci_analysis_files/figure-gfm/unnamed-chunk-8-1.png)

- multinomial Bayesian regression of response type against an intercept
  (no REs) shows credible effects for the following intuitive
  hypotheses:
  1.  the competitor is the prevalent category
  2.  competitor is more prevalent than otherCategory
  3.  competitor is more prevalent than fullList
  4.  sameCategory is more prevalent than otherCategory
  5.  sameCategory is more prevalent than fullList
- [Experiment 2](): 36 subjects / 143 responses analysed, 13 pairs of
  vignettes.
  - distribution of response types across contexts ![response type
    proportions across contexts in
    E2](07_main_contextSensitive_pilot_analysis_files/figure-gfm/unnamed-chunk-7-1.png)

  - distribution of alternative types mentioned in context 2 (left side)
    vs context 1 (right side) ![difference in category mentioning
    proportions between contexts in
    E2](07_main_contextSensitive_pilot_analysis_files/figure-gfm/unnamed-chunk-12-1.png)

  - stats TBD (probably bootstrapping the absolute difference of
    category mentioning proportions between the contexts)

## neural model experiments and comparison to human data

### goal

- compare performance of pretrained neural extractive and generative
  [models on QA to human
  performance](https://github.com/magpie-ea/magpie3-qa-overinfo-free-production/blob/main/data%2Banalysis/06_expt_vs_LLMs_analysis.md)
  (from Huggingface / OpenAI)
- investigate ability of generative LMs to pick up on pragmatic
  reasoning by comparing performance in a zero-shot setting to one-shot
  setting (example context + question + response with explanation
  prepended to context)
  - extractive: RoBERTa base (SQuADv2), BERT large uncased whole word
    masking (SQuADv1), BERT base cased (SQuADv2), DistilBERT base cased
    (SQuADv1), DistilBERT base uncased (SQuADv1), DeBERTA base
    (SQuADv2), tinyRoBERTa (SQuADv2), Electra base (SQuADv2), BART
    (SQuADv2)
  - generative: T5 base QA finetuned (SQuADv2), T5 base QA finetuned
    (DuoRC), T0_3B (many datasets), BART (Eli5), GPT-2, GPT-2 finetuned
    (SQuADv2), ChatGPT, GPT-3

### approach

- comparison on two metrics:
  - sampling performance, i.e. direct task inference, top 5 samples
    classified manually like human responses
  - mean log probs over tokens of different types of answers (averaged
    over all permutations of alternatives in the sentence, and answer
    types both with and without taciturn prefix “I’m sorry, we don’t
    have…”)

### results

- Experiment 1:
  - human responses, averages over response types (over both extractive
    and generative model), and probabilities computed under LMs across
    models from E1 ![global neural response type proportions,
    probabilities and human data in
    E1](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-29-1.png)

  - by-model plot of sampled response types (extractive + generative)
    ![neural response type proportionsby model in
    E1](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-10-1.png)

  - by-model retrieved probabilities (generative models) ![neural
    responseprobabilitie in
    E1](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-23-1.png)

  - generative model sample type proportions under one-shot
    vs. zero-shot prompting ![neural response type proportions on zero
    shot vs one shot prompts in
    E1](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-12-1.png)

  - the models’ sample proportions and mean log probabilities assigned
    to different response types were compared to human response type
    proportions with $X^2$-tests (by-model) and the $p$-values were
    retrieved. All $p$-values are well below 0.05.
- Experiment 2:
  - alternatives mentioned in samples from LMs across models by context
    (only GPT-3 zero shot so far) ![gpt3 slternative mentioning
    proportions in E2](viz/e2_gpt3_samples.png)
  - response type proportions in GPT3 zero shot samples ![gpt3 response
    type proportions in E2](viz/e2_gpt3_categories.png)
  - human responses and probabilities computed under LMs across models
    (only GPT-3 zero shot so far) ![gpt3 response type probabilities vs
    human proportions in E2](viz/e2_scores.png)

  TBD
  - by-model plot of sampled response types (extractive + generative)
  - by-model retrieved probabilities (generative models)
  - generative model sample type proportions under one-shot
    vs. zero-shot prompting

## conclusions

- as anticipated, humans mostly produce competitor responses, and are
  less likely to produce full list responses.
- human suggestions are action-relevance dependent
- neural models have a much higher propensity of full list responses
- probabilities of different response types assigned by neural models do
  not mirror human preferences, suggesting that they lack the necessary
  representational and reasoning capacities
