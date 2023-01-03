QA free typing analysis
================
Polina Tsvilodub
2023-01-02

## Intro

The following script compares the results from the [free production
human
experiment](https://github.com/magpie-ea/magpie3-qa-overinfo-free-production/blob/main/data%2Banalysis/05_main_free_typing_cogsci_analysis.md)
run on the final 30 items for CogSci to samples and scores retrieved
from Language Models (LMs) and neural models fine-tuned for question
answering on various datasets. For each model, the top 5 predictions
were retrieved. For LMs, the results are compared when using the
one-shot example also used for GPT-3, vs results without any additional
context prompting. Example model queries looked like this:

- extractive QA models: \[CLS\] Do you have raspberry cake? \[SEP\] You
  are a server in a café. Today the café has raspberry pie, chocolate
  cookies, and cheese pizza. A customer asks:\[SEP\]
- LM: You are a server in a café. Today the café has raspberry pie,
  chocolate cookies, and cheese pizza. A customer asks: Q: Do you have
  raspberry cake? A:
- LM with one shot example: You are hosting a barbecue party. You are
  standing behind the barbecue. You have the following goods to offer:
  pork sausages, vegan burgers, grilled potatoes and beef burgers. You
  reason about what that person most likely wanted to have. That they
  asked for grilled zucchini suggests that they might want vegetarian
  food. From the items you have pork sausages and beef burgers are least
  likely to satisfy the persons desires. Vegan burgers and grilled
  potatoes come much closer. Grilled potatoes are most similar to
  grilled zucchini. You reply: I’m sorry, I don’t have any grilled
  zucchini. But I do have some grilled potatoes. Now consider a
  different situation. Someone asks: Do you have grilled zucchini? You
  are a server in a café. Today the café has raspberry pie, chocolate
  cookies, and cheese pizza. A customer asks: Q: Do you have raspberry
  cake? A:

The samples from the neural models were hand-categorized into the same
categories as the human data. That is, they were categorized according
to the following criteria. Note that responses consisting of incomplete
/ ungrammatical / repetitive sentences (especially in case of GPT-2
based or one-shot models, the predictions sometimes repeated parts of
the context) were also classified as long as they contained mentions of
critical alternatives. When the alternative was mentioned incompletely
(e.g., ‘kickboxing’ instead of ‘kickboxing class’), it was only taken
into account in the classification of it was judged to be a phrase hat
could be naturally produced by human participants (mostly, kickboxing
item).

- ‘competitor’: responses mentioning the anticipated competitor only.
  Responses which started with yes but then only mentioned the
  competitor were also considered competitor category responses.
- ‘sameCategory’: responses offering both same category alternatives or
  offering the option which we did not consider the direct competitor.
  Responses which started with yes but then mentioned relevant
  alternatives were also considered same category responses.
- ‘otherCategory’: responses offering the alternative from the different
  category. Responses which started with yes but then mentioned relevant
  alternatives were also considered other category responses.
- ‘fullList’: responses where all alternatives were listed (also across
  several sentences). Responses which started with yes or repeated parts
  of the context / question but then mentioned all alternatives were
  also considered fullList responses.
- ‘taciturn’: responses not offering any alternative options or further
  alternative solutions. Responses repeating the question and saying
  ‘no’ or saying ‘no’ followed by some (generated) explanation or
  repetition were also considered taciturn responses.
- ‘other’: where a same category + other category response are mixed,
  uncertain answers, unclassifiable responses, responses offering
  further steps towards solcing the problem, responses using basic level
  categories (e.g., “dogs” instead of offering specific alternatives).
  Also nonsense responses, contradictory responses, responses mentioning
  parts of the one-shot context, completely ungrammatical responses,
  responses including insufficient formulations of some alternative were
  classified as ‘other’.
- ‘yes’: plain ‘yes’ responses, responses mentioning that the target
  item was present, responses mentioning the presense of the target otem
  even if it was followed by correctly mentioning alternative items
  (e.g., as additional options).
- The additional ‘none’ category was introduced due to extractive QA
  models which sometime predict an empty span consisting of a special
  token only. These were marked as being silent, i.e., ‘none’ (since
  such an option did not exist for human participants).

First, the script provides some descriptive information about the neural
model samples and probs, before presenting visual comparisons to human
data followed by some exploratory stats.

## Load processed experimental results and neural model data, display descriptions

Read in by-vignette response category proportions.

Read in categorized sample data from (generative) LMs and extractive QA
models.

    ## # A tibble: 6 × 15
    ##   `Unnamed: 0` itemName  setti…¹ context conte…² quest…³ tacit…⁴ compe…⁵ sameC…⁶
    ##          <dbl> <chr>     <chr>   <chr>   <chr>   <chr>   <chr>   <chr>   <chr>  
    ## 1            0 cafe-pie  cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 2            0 cafe-pie  cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 3            0 cafe-pie  cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 4            0 cafe-pie  cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 5            0 cafe-pie  cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 6            1 cafe-piz… cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## # … with 6 more variables: otherCategory <chr>, fullList <chr>,
    ## #   model_name <chr>, predictions <chr>, category <chr>, is_few_shot <lgl>, and
    ## #   abbreviated variable names ¹​settingName, ²​context_qa, ³​question, ⁴​taciturn,
    ## #   ⁵​competitor, ⁶​sameCategory

Load all files with probabilities of different kinds of (human)
responses under pretrained LMs. All probabilities were computed
*without* one-shot exmples in the context.

    ## # A tibble: 6 × 15
    ##    ...1 Unname…¹ itemN…² setti…³ context conte…⁴ quest…⁵ tacit…⁶ compe…⁷ sameC…⁸
    ##   <dbl>    <dbl> <chr>   <chr>   <chr>   <chr>   <chr>   <chr>   <chr>   <chr>  
    ## 1     0        0 cafe-p… cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 2     0        0 cafe-p… cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 3     0        0 cafe-p… cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 4     0        0 cafe-p… cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 5     0        0 cafe-p… cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## 6     1        1 cafe-p… cafe    You ar… You ar… Do you… I'm so… I'm so… I'm so…
    ## # … with 5 more variables: otherCategory <chr>, fullList <chr>,
    ## #   answer_type_prob <dbl>, model_name <chr>, answer_type <chr>, and
    ## #   abbreviated variable names ¹​`Unnamed: 0`, ²​itemName, ³​settingName,
    ## #   ⁴​context_qa, ⁵​question, ⁶​taciturn, ⁷​competitor, ⁸​sameCategory

Look at the distributions of response types in the sampled responses,
globally and by-model. ‘None’ and ‘yes’ responses are excluded from
global, by-model, by-item and by-model-by-item proportion summaries for
further analyses.

    ## Models that were used:  aware-ai/bart-squadv2 bert-large-uncased-whole-word-masking-finetuned-squad bigscience/T0_3B danyaljj/gpt2_question_answering_squad2 deepset/bert-base-cased-squad2 deepset/deberta-v3-base-squad2 deepset/electra-base-squad2 deepset/roberta-base-squad2 deepset/tinyroberta-squad2 distilbert-base-cased-distilled-squad distilbert-base-uncased-distilled-squad gpt2 MaRiOrOsSi/t5-base-finetuned-question-answering valhalla/t5-base-qa-qg-hl yjernite/bart_eli5

    ## Number of models that were used:  15

    ## Overall response category counts:

    ## # A tibble: 9 × 2
    ##   category          n
    ##   <chr>         <int>
    ## 1 competitor      466
    ## 2 fullList        618
    ## 3 none            236
    ## 4 other           825
    ## 5 otherCategory    41
    ## 6 sameCategory    127
    ## 7 taciturn        161
    ## 8 yes             524
    ## 9 <NA>              2

    ## By model response category counts:

    ## # A tibble: 87 × 3
    ##    model_name                                            category          n
    ##    <chr>                                                 <chr>         <int>
    ##  1 aware-ai/bart-squadv2                                 competitor       25
    ##  2 aware-ai/bart-squadv2                                 fullList          3
    ##  3 aware-ai/bart-squadv2                                 none             29
    ##  4 aware-ai/bart-squadv2                                 other            91
    ##  5 aware-ai/bart-squadv2                                 sameCategory      2
    ##  6 bert-large-uncased-whole-word-masking-finetuned-squad competitor       69
    ##  7 bert-large-uncased-whole-word-masking-finetuned-squad fullList         49
    ##  8 bert-large-uncased-whole-word-masking-finetuned-squad other            21
    ##  9 bert-large-uncased-whole-word-masking-finetuned-squad otherCategory     2
    ## 10 bert-large-uncased-whole-word-masking-finetuned-squad sameCategory      9
    ## # … with 77 more rows

    ## By dataset response category proportions:

    ## `summarise()` has grouped output by 'dataset'. You can override using the
    ## `.groups` argument.

    ## # A tibble: 39 × 4
    ## # Groups:   dataset [6]
    ##    dataset                                                   categ…¹     n  prop
    ##    <chr>                                                     <chr>   <int> <dbl>
    ##  1 eli5                                                      yes       233 0.777
    ##  2 DuoRC                                                     yes       131 0.437
    ##  3 SQuADv1                                                   fullLi…   312 0.416
    ##  4 WebText                                                   yes       124 0.413
    ##  5 MC QA, EQA, CBQA, D2T, sentiment, summary, topic, paraph… tacitu…    57 0.38 
    ##  6 SQuADv2                                                   other     447 0.372
    ##  7 SQuADv1                                                   other     202 0.269
    ##  8 WebText                                                   tacitu…    75 0.25 
    ##  9 SQuADv1                                                   compet…   184 0.245
    ## 10 DuoRC                                                     fullLi…    64 0.213
    ## # … with 29 more rows, and abbreviated variable name ¹​category

    ## Compare response category proportions of models trained on SQuADv1 vs SQuADv2:

    ## `summarise()` has grouped output by 'dataset'. You can override using the
    ## `.groups` argument.

    ## # A tibble: 9 × 3
    ##   category       SQuADv1   SQuADv2
    ##   <chr>            <dbl>     <dbl>
    ## 1 competitor     0.245    0.208   
    ## 2 fullList       0.416    0.146   
    ## 3 other          0.269    0.372   
    ## 4 otherCategory  0.0107   0.0242  
    ## 5 sameCategory   0.056    0.0442  
    ## 6 <NA>           0.00267 NA       
    ## 7 none          NA        0.197   
    ## 8 taciturn      NA        0.000833
    ## 9 yes           NA        0.0075

    ## Compare response category proportions of cased vs uncased DistilBERT models:

    ## `summarise()` has grouped output by 'model_name'. You can override using the
    ## `.groups` argument.

    ## # A tibble: 6 × 3
    ##   category      `distilbert-base-cased-distilled-squad` distilbert-base-uncase…¹
    ##   <chr>                                           <dbl>                    <dbl>
    ## 1 competitor                                    0.3                      0.16   
    ## 2 fullList                                      0.26                     0.373  
    ## 3 other                                         0.38                     0.407  
    ## 4 otherCategory                                 0.00667                 NA      
    ## 5 sameCategory                                  0.0467                   0.0533 
    ## 6 <NA>                                          0.00667                  0.00667
    ## # … with abbreviated variable name ¹​`distilbert-base-uncased-distilled-squad`

    ## `summarise()` has grouped output by 'model_name', 'is_few_shot'. You can
    ## override using the `.groups` argument.

    ## Proportion of response categories by model:

    ## # A tibble: 112 × 5
    ## # Groups:   model_name, is_few_shot [20]
    ##    model_name                                       is_fe…¹ categ…²     n   prop
    ##    <chr>                                            <lgl>   <chr>   <int>  <dbl>
    ##  1 aware-ai/bart-squadv2                            FALSE   compet…    25 0.167 
    ##  2 aware-ai/bart-squadv2                            FALSE   fullLi…     3 0.02  
    ##  3 aware-ai/bart-squadv2                            FALSE   none       29 0.193 
    ##  4 aware-ai/bart-squadv2                            FALSE   other      91 0.607 
    ##  5 aware-ai/bart-squadv2                            FALSE   sameCa…     2 0.0133
    ##  6 bert-large-uncased-whole-word-masking-finetuned… FALSE   compet…    69 0.46  
    ##  7 bert-large-uncased-whole-word-masking-finetuned… FALSE   fullLi…    49 0.327 
    ##  8 bert-large-uncased-whole-word-masking-finetuned… FALSE   other      21 0.14  
    ##  9 bert-large-uncased-whole-word-masking-finetuned… FALSE   otherC…     2 0.0133
    ## 10 bert-large-uncased-whole-word-masking-finetuned… FALSE   sameCa…     9 0.06  
    ## # … with 102 more rows, and abbreviated variable names ¹​is_few_shot, ²​category

    ## Proportion of 'yes' response categories by model (sorted from worst model to best):

    ## # A tibble: 10 × 5
    ## # Groups:   model_name, is_few_shot [10]
    ##    model_name                                      is_fe…¹ categ…²     n    prop
    ##    <chr>                                           <lgl>   <chr>   <int>   <dbl>
    ##  1 yjernite/bart_eli5                              TRUE    yes       118 0.787  
    ##  2 yjernite/bart_eli5                              FALSE   yes       115 0.767  
    ##  3 gpt2                                            TRUE    yes       100 0.667  
    ##  4 MaRiOrOsSi/t5-base-finetuned-question-answering TRUE    yes        69 0.46   
    ##  5 MaRiOrOsSi/t5-base-finetuned-question-answering FALSE   yes        62 0.413  
    ##  6 bigscience/T0_3B                                FALSE   yes        27 0.18   
    ##  7 gpt2                                            FALSE   yes        24 0.16   
    ##  8 danyaljj/gpt2_question_answering_squad2         FALSE   yes         6 0.04   
    ##  9 danyaljj/gpt2_question_answering_squad2         TRUE    yes         2 0.0133 
    ## 10 deepset/roberta-base-squad2                     FALSE   yes         1 0.00667
    ## # … with abbreviated variable names ¹​is_few_shot, ²​category

    ## Proportion of 'none' response categories by QA model (sorted from worst model to best):

    ## # A tibble: 6 × 5
    ## # Groups:   model_name, is_few_shot [6]
    ##   model_name                     is_few_shot category     n  prop
    ##   <chr>                          <lgl>       <chr>    <int> <dbl>
    ## 1 deepset/electra-base-squad2    FALSE       none        77 0.513
    ## 2 deepset/deberta-v3-base-squad2 FALSE       none        50 0.333
    ## 3 aware-ai/bart-squadv2          FALSE       none        29 0.193
    ## 4 deepset/tinyroberta-squad2     FALSE       none        28 0.187
    ## 5 deepset/bert-base-cased-squad2 FALSE       none        27 0.18 
    ## 6 deepset/roberta-base-squad2    FALSE       none        25 0.167

    ## `summarise()` has grouped output by 'model_name', 'is_few_shot'. You can
    ## override using the `.groups` argument.
    ## `summarise()` has grouped output by 'model_name'. You can override using the
    ## `.groups` argument.
    ## `summarise()` has grouped output by 'model_name', 'is_few_shot', 'itemName'.
    ## You can override using the `.groups` argument.
    ## `summarise()` has grouped output by 'itemName'. You can override using the
    ## `.groups` argument.

    ## Proportion of response categories by vignette:

    ## # A tibble: 158 × 5
    ## # Groups:   itemName [30]
    ##    itemName      category          n   prop answerType   
    ##    <chr>         <chr>         <int>  <dbl> <fct>        
    ##  1 bar-tea       competitor       10 0.132  competitor   
    ##  2 bar-tea       fullList         35 0.461  fullList     
    ##  3 bar-tea       other            30 0.395  other        
    ##  4 bar-tea       taciturn          1 0.0132 taciturn     
    ##  5 bar-whiteWine competitor       21 0.259  competitor   
    ##  6 bar-whiteWine fullList         26 0.321  fullList     
    ##  7 bar-whiteWine other            24 0.296  other        
    ##  8 bar-whiteWine otherCategory     1 0.0123 otherCategory
    ##  9 bar-whiteWine sameCategory      2 0.0247 sameCategory 
    ## 10 bar-whiteWine taciturn          7 0.0864 taciturn     
    ## # … with 148 more rows

    ## Global response category proportions:

    ## # A tibble: 6 × 4
    ##   category          n   prop answerType   
    ##   <chr>         <int>  <dbl> <fct>        
    ## 1 competitor      466 0.208  competitor   
    ## 2 fullList        618 0.276  fullList     
    ## 3 other           825 0.369  other        
    ## 4 otherCategory    41 0.0183 otherCategory
    ## 5 sameCategory    127 0.0567 sameCategory 
    ## 6 taciturn        161 0.0719 taciturn

## Plots

The first plot shows global response proportions, averaged across models
and vignettes.

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

The next plot displays proportions of different responses from different
models, averaging across one-shot and zero-shot LMs.

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-9-1.png)<!-- -->

The next plot displays proportions of different responses from different
models, differentiating between one-shot and zero-shot LMs.

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->

The next plot displays proportions of different responses from models
by-vignette.

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-11-1.png)<!-- -->

### Comparing neural and human responses

Below, the response type categories sampled from models and collected in
the free production human experiment are plotted against each other.

First, the global proportions are compared.

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-12-1.png)<!-- -->

Next, by-vignette results can be found below.

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-13-1.png)<!-- -->

### Model probabilities

Below, the scores assigned to provided answer types are compared to the
proportions of those answer types generated by the language models
during sampling. Whenever the responses sampled from the model were
difficult to classify due to half-generated phrases (like “kick” instead
of kickboxing), they were categorized as “other” responses. The
comparison is by model type.

    ## `summarise()` has grouped output by 'answerType'. You can override using the
    ## `.groups` argument.

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-14-1.png)<!-- -->

Compare the samples and the probabilities assigned by the models to
human data (across models and vignettes).

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-15-1.png)<!-- -->

Below, scores by-vignette are compared (across models).

    ## `summarise()` has grouped output by 'answerType'. You can override using the
    ## `.groups` argument.

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-16-1.png)<!-- -->

Compare the scores of different models to their proportion predictions:

![](06_expt_vs_LLMs_analysis_files/figure-gfm/unnamed-chunk-17-1.png)<!-- -->

## Stats

Below, the KL-divergence of between global human response type
proportions (renormalized after excluding ‘other’ responses) and
probabilities assigned by the models are compared. Note the implicit
assumption that the proportions of different response types produced by
humans are the probabilities of producing that particular type given the
context.

``` r
df_human_global_renorm <- df_human_global %>% filter(answerType != "other") %>%
  mutate(answer_type_prob = prop / (df_human_global %>% filter(answerType != "other") %>% pull(prop) %>% sum()))

model_human_dists <- rbind(lm_scores_global %>% pull(answer_type_prob), df_human_global_renorm %>% pull(answer_type_prob)) 
kl <- philentropy::KL(model_human_dists)
```

    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.

``` r
cat("KL divergence : ", kl)
```

    ## KL divergence :  1.034189

Compute a multinomial regression with a main effect of human vs model
data, regressing the response category against an intercept and a main
effect of data source, and random by-item intercepts. Competitor
responses are coded as the reference level.

``` r
df_human_raw <- read_csv("data/results_QA-overinfo-freeTyping-cogsci_full_anonymized_categorized.csv") %>% 
  filter(category != 'yes', !(submission_id %in% c(4608, 4690, 4687, 4733, 4763))) %>% 
  mutate(answerType = factor(category, levels = answerOrder),
         model_name = "human"
         ) %>% 
  select(itemName, answerType, model_name)

df_samples_human_raw <- nm_samples_categorized %>% 
  filter((category != "yes") & (category != "none")) %>%
  mutate(
    answerType = factor(category, levels = answerOrder),
    model_name = "neural"
  ) %>%
  select(itemName, answerType, model_name) %>%
  rbind(., df_human_raw) %>%
  mutate(
    model_name = factor(model_name, levels = c("human", "neural"))
  )

contrasts(df_samples_human_raw$answerType)
```

    ##               sameCategory otherCategory fullList taciturn other
    ## competitor               0             0        0        0     0
    ## sameCategory             1             0        0        0     0
    ## otherCategory            0             1        0        0     0
    ## fullList                 0             0        1        0     0
    ## taciturn                 0             0        0        1     0
    ## other                    0             0        0        0     1

``` r
contrasts(df_samples_human_raw$model_name)
```

    ##        neural
    ## human       0
    ## neural      1

``` r
model <- brm(answerType ~ 1 + model_name + (1 | itemName), 
             data = df_samples_human_raw,
             family = "categorical",
             iter = 4000
             )
```

    ## Running /Library/Frameworks/R.framework/Resources/bin/R CMD SHLIB foo.c
    ## clang -arch arm64 -I"/Library/Frameworks/R.framework/Resources/include" -DNDEBUG   -I"/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/Rcpp/include/"  -I"/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppEigen/include/"  -I"/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppEigen/include/unsupported"  -I"/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/BH/include" -I"/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/StanHeaders/include/src/"  -I"/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/StanHeaders/include/"  -I"/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppParallel/include/"  -I"/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/rstan/include" -DEIGEN_NO_DEBUG  -DBOOST_DISABLE_ASSERTS  -DBOOST_PENDING_INTEGER_LOG2_HPP  -DSTAN_THREADS  -DBOOST_NO_AUTO_PTR  -include '/Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/StanHeaders/include/stan/math/prim/mat/fun/Eigen.hpp'  -D_REENTRANT -DRCPP_PARALLEL_USE_TBB=1   -I/opt/R/arm64/include   -fPIC  -falign-functions=64 -Wall -g -O2  -c foo.c -o foo.o
    ## In file included from <built-in>:1:
    ## In file included from /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/StanHeaders/include/stan/math/prim/mat/fun/Eigen.hpp:13:
    ## In file included from /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppEigen/include/Eigen/Dense:1:
    ## In file included from /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppEigen/include/Eigen/Core:88:
    ## /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppEigen/include/Eigen/src/Core/util/Macros.h:628:1: error: unknown type name 'namespace'
    ## namespace Eigen {
    ## ^
    ## /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppEigen/include/Eigen/src/Core/util/Macros.h:628:16: error: expected ';' after top level declarator
    ## namespace Eigen {
    ##                ^
    ##                ;
    ## In file included from <built-in>:1:
    ## In file included from /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/StanHeaders/include/stan/math/prim/mat/fun/Eigen.hpp:13:
    ## In file included from /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppEigen/include/Eigen/Dense:1:
    ## /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/library/RcppEigen/include/Eigen/Core:96:10: fatal error: 'complex' file not found
    ## #include <complex>
    ##          ^~~~~~~~~
    ## 3 errors generated.
    ## make: *** [foo.o] Error 1

``` r
summary(model)
```

    ##  Family: categorical 
    ##   Links: musameCategory = logit; muotherCategory = logit; mufullList = logit; mutaciturn = logit; muother = logit 
    ## Formula: answerType ~ 1 + model_name + (1 | itemName) 
    ##    Data: df_samples_human_raw (Number of observations: 2833) 
    ##   Draws: 4 chains, each with iter = 4000; warmup = 2000; thin = 1;
    ##          total post-warmup draws = 8000
    ## 
    ## Group-Level Effects: 
    ## ~itemName (Number of levels: 31) 
    ##                               Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(musameCategory_Intercept)      0.85      0.17     0.57     1.24 1.00
    ## sd(muotherCategory_Intercept)     1.51      0.40     0.88     2.43 1.00
    ## sd(mufullList_Intercept)          0.29      0.09     0.12     0.48 1.00
    ## sd(mutaciturn_Intercept)          0.71      0.13     0.48     1.00 1.00
    ## sd(muother_Intercept)             0.48      0.09     0.32     0.67 1.00
    ##                               Bulk_ESS Tail_ESS
    ## sd(musameCategory_Intercept)      2304     3943
    ## sd(muotherCategory_Intercept)     2180     3751
    ## sd(mufullList_Intercept)          1693     1930
    ## sd(mutaciturn_Intercept)          2446     4689
    ## sd(muother_Intercept)             2451     3974
    ## 
    ## Population-Level Effects: 
    ##                                  Estimate Est.Error l-95% CI u-95% CI Rhat
    ## musameCategory_Intercept            -1.24      0.20    -1.65    -0.85 1.00
    ## muotherCategory_Intercept           -5.99      0.88    -7.94    -4.46 1.00
    ## mufullList_Intercept                -1.68      0.16    -2.02    -1.37 1.00
    ## mutaciturn_Intercept                -1.01      0.17    -1.36    -0.67 1.00
    ## muother_Intercept                   -1.41      0.17    -1.74    -1.09 1.00
    ## musameCategory_model_nameneural     -0.29      0.17    -0.62     0.03 1.00
    ## muotherCategory_model_nameneural     2.86      0.81     1.54     4.69 1.00
    ## mufullList_model_nameneural          1.97      0.17     1.65     2.30 1.00
    ## mutaciturn_model_nameneural         -0.15      0.15    -0.45     0.15 1.00
    ## muother_model_nameneural             2.00      0.15     1.70     2.31 1.00
    ##                                  Bulk_ESS Tail_ESS
    ## musameCategory_Intercept             2989     4815
    ## muotherCategory_Intercept            4798     4252
    ## mufullList_Intercept                 7012     5450
    ## mutaciturn_Intercept                 3482     4740
    ## muother_Intercept                    4335     4720
    ## musameCategory_model_nameneural      7784     6131
    ## muotherCategory_model_nameneural     8172     4497
    ## mufullList_model_nameneural          8434     6168
    ## mutaciturn_model_nameneural          7455     5952
    ## muother_model_nameneural             7253     5628
    ## 
    ## Draws were sampled using sampling(NUTS). For each parameter, Bulk_ESS
    ## and Tail_ESS are effective sample size measures, and Rhat is the potential
    ## scale reduction factor on split chains (at convergence, Rhat = 1).

Extract contrasts by response type between human data and neural model
data (i.e., probability that proportion of given response type is larger
in human than in neural model data):

``` r
model_posteriors <- model %>% spread_draws(b_musameCategory_Intercept, b_muotherCategory_Intercept, b_mufullList_Intercept, b_mutaciturn_Intercept, b_muother_Intercept, b_musameCategory_model_nameneural, b_muotherCategory_model_nameneural, b_mufullList_model_nameneural, b_mutaciturn_model_nameneural, b_muother_model_nameneural) %>%
  mutate(
    sameCategory = b_musameCategory_Intercept - b_musameCategory_model_nameneural,
    otherCategory = b_musameCategory_Intercept - b_muotherCategory_model_nameneural,
    fullList = b_mufullList_Intercept - b_mufullList_model_nameneural,
    taciturn = b_mutaciturn_Intercept - b_mutaciturn_model_nameneural,
    other = b_muother_Intercept - b_muother_model_nameneural
  )

model_posteriors %>% select(sameCategory, otherCategory, fullList, taciturn, other) %>%
  gather(key, val) %>%
  group_by(key) %>%
  summarize(
    '|95%' = quantile(val, probs = c(0.025, 0.975))[[1]],
    'mean'  = mean(val),
    '95%|' = quantile(val, probs = c(0.025, 0.975))[[2]],
    prob_gt_0 = mean(val > 0)*100,
    prob_lt_0 = mean(val < 0)*100
  ) -> model_posteriors_summary

model_posteriors_summary
```

    ## # A tibble: 5 × 6
    ##   key           `|95%`   mean `95%|` prob_gt_0 prob_lt_0
    ##   <chr>          <dbl>  <dbl>  <dbl>     <dbl>     <dbl>
    ## 1 fullList       -4.30 -3.66  -3.04      0         100  
    ## 2 other          -4.01 -3.41  -2.84      0         100  
    ## 3 otherCategory  -5.95 -4.10  -2.70      0         100  
    ## 4 sameCategory   -1.58 -0.945 -0.326     0.137      99.9
    ## 5 taciturn       -1.41 -0.857 -0.294     0.112      99.9

``` r
# TODO: determine the prob that competitor proportion in human data larger than in neural data
```
