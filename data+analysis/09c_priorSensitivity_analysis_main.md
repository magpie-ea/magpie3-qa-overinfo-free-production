PragmaticQA E4: Prior Sensitivity Free Production: Main
================
PT
2024-04-30

# Intro

This is another experiment in the PragmaticQA project, wherein we
investigate whether speakers’ overinformativeness in response to polar
questions depends on the (commonly known) prior probability of the
available options. The live experiment can be found
[here](https://magpie-ea.github.io/magpie3-qa-overinfo-free-production/experiments/04-priorSensitivity_free_production/).
We manipulate the prior probability of the available options in context,
resulting in two critical conditions, highPrior (high prior options
available) and lowPrior (high prior option not available). The
experiment is a free production experiment. Each participant sees four
main trials (two per condition, assigned at random to four randomly
chosen vignettes), and one filler trial. Fillers are re-used from CogSci
E1.

- Main experiment: N=99 were recruited. Ten items were used (as in pilot
  2). Therefore, the combined data of pilot 2 (N=30) and the main data
  collection are analysed here.

We exclude the following invalid response categories:

- “no”: participants answered no to the question (although all questions
  were yes-questions)
- “other”: uncategorizable responses
- “yes”: all three options were stated as available

Furthermore, some responses had two categories, namely the full list
(i.e., the two available options were named) and the exceptive phrase
(i.e, it was stated that one option was not available). Such responses
were split into two data points with single labels.

``` r
d_main_clean <- d_main %>%
  filter(category != "no") %>%
  filter(category != "other") %>%
  filter(category != "yes") %>%
  mutate(
    category = str_split(category, ", ", simplify = FALSE) 
  ) %>%
  unnest(category) %>%
  mutate(
    category = ifelse(category == "taciturn_more", "taciturn", category)
  )
  
d_main_clean
```

    ## # A tibble: 456 × 14
    ##    submiss…¹   age answer categ…² comme…³ condi…⁴ corre…⁵ educa…⁶ gender itemN…⁷
    ##        <dbl> <dbl> <chr>  <chr>   <chr>   <chr>   <chr>   <chr>   <chr>  <chr>  
    ##  1      3363    30 Yes w… tacitu… This w… low_pr… <NA>    Gradua… female videoG…
    ##  2      3363    30 Yes, … fullLi… This w… high_p… <NA>    Gradua… female coffee…
    ##  3      3363    30 Hi! W… except… This w… high_p… <NA>    Gradua… female cardBl…
    ##  4      3363    30 There… except… This w… low_pr… <NA>    Gradua… female phoneR…
    ##  5      3364    29 Yes, … fullLi… <NA>    low_pr… <NA>    Gradua… female parking
    ##  6      3364    29 Yes, … except… <NA>    low_pr… <NA>    Gradua… female parking
    ##  7      3364    29 Yes, … fullLi… <NA>    high_p… <NA>    Gradua… female carshr…
    ##  8      3364    29 You c… fullLi… <NA>    high_p… <NA>    Gradua… female foodCo…
    ##  9      3364    29 Yes w… fullLi… <NA>    low_pr… <NA>    Gradua… female airpla…
    ## 10      3365    24 You c… fullLi… <NA>    high_p… <NA>    Gradua… other  social…
    ## # … with 446 more rows, 4 more variables: languages <chr>, responseTime <dbl>,
    ## #   trialNr <dbl>, trial_type <chr>, and abbreviated variable names
    ## #   ¹​submission_id, ²​category, ³​comments, ⁴​condition, ⁵​correct_response,
    ## #   ⁶​education, ⁷​itemName

The freely typed responses were manually categorized into the following
categories:

- “taciturn”: responses just saying “yes” or “yes, we do” or similar.
- “taciturn_more”: responses saying “yes” but providing some additional
  information without mentioning specific options, for instance “Yes
  there are some coffee shops around the corner”
- “mostLikely”: response mentioning the most likely option among the
  available ones, e.g., “Yes we do accept American Express”
- “leastLikely”: only one option was named, namely the least likely one
  among the available ones, e.g., “Yes we do accept Visa” in the high
  prior condition
- “fullList”: responses mentioning the two specific available options
- “exceptive: responses mentioning which option is NOT available,
  e.g.,”Yes, all except Card Blanche”

Below the single category proportions are displayed by condition. For
the purposes of the main analysis, taciturn and taciturn_more responses
are collapsed.

``` r
df_answerOptions_global_summary <- d_main_clean %>% 
  group_by(category) %>% 
  summarise(answerType_count = n(), 
            answerType_proportion = answerType_count / nrow(d)
            )

df_answerOptions_byCondition_summary <- d_main_clean %>% 
  filter(category != "no") %>%
  group_by(condition) %>%
  mutate(condition_counts = n()) %>%
  group_by(category, condition) %>% 
  summarise(answerType_count = n(), 
            answerType_proportion = answerType_count / condition_counts
            ) %>% unique()
```

    ## `summarise()` has grouped output by 'category', 'condition'. You can override
    ## using the `.groups` argument.

``` r
df_answerOptions_byCondition_summary %>%
  ggplot(aes(x = condition, y = answerType_proportion, fill = category)) +
  geom_col(color = "#575463") +
  theme_csp() +
  theme(plot.title = element_text(hjust = 0.5)) +
  ylab("Proportion of answer type") +
  xlab("") 
```

![](09c_priorSensitivity_analysis_main_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

Below, the response categories are plotted by-item, so as to check if
respondents might have chosen different strategies, e.g., full-list
responses, in e.g. commercial contexts so as to not loose customers:

``` r
df_answerOptions_byCondition_byItem_summary <- d_main_clean %>% 
  filter(category != "no") %>%
  group_by(itemName, condition) %>%
  mutate(condition_counts = n()) %>%
  group_by(itemName, category, condition) %>% 
  summarise(answerType_count = n(), 
            answerType_proportion = answerType_count / condition_counts
            ) %>% unique()
```

    ## `summarise()` has grouped output by 'itemName', 'category', 'condition'. You
    ## can override using the `.groups` argument.

``` r
df_answerOptions_byCondition_byItem_summary %>%
  ggplot(aes(x = condition, y = answerType_count, fill = category)) +
  geom_col(color = "#575463") +
  theme_csp() +
  theme(plot.title = element_text(hjust = 0.5)) +
  ylab("Proportion of answer type") +
  facet_wrap(~itemName, ncol=3) +
  xlab("") 
```

![](09c_priorSensitivity_analysis_main_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

We can also check whether there is a credible difference between the
rate of fullList responses (i.e., both fullList and exceptive responses)
in the two conditions, by fitting a Bayesian logistic regression with a
main effect of condition and maximal random effects. Uninformative
priors are used. The hypothesis is that there are more fullList
responses in the lowPrior condition than in the highPrior condition.

``` r
d_main_fullList_binary <- d_main_clean %>% 
  mutate(is_fullList = ifelse(category == "exceptive", 1, ifelse(category == "fullList", 1, 0))) 

priors <- set_prior("student_t(1, 0, 2)", class = "b")

lm_full <- brm(
  is_fullList ~ condition + (1 + condition | submission_id) + (1 + condition | itemName),
  data = d_main_fullList_binary,
  family = "bernoulli",
  prior = priors,
  control = list(adapt_delta = 0.95),
  iter = 3000,
  chains = 4
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
summary(lm_full)
```

    ##  Family: bernoulli 
    ##   Links: mu = logit 
    ## Formula: is_fullList ~ condition + (1 + condition | submission_id) + (1 + condition | itemName) 
    ##    Data: d_main_fullList_binary (Number of observations: 456) 
    ##   Draws: 4 chains, each with iter = 3000; warmup = 1500; thin = 1;
    ##          total post-warmup draws = 6000
    ## 
    ## Group-Level Effects: 
    ## ~itemName (Number of levels: 10) 
    ##                                   Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(Intercept)                         1.19      0.46     0.50     2.31 1.00
    ## sd(conditionlow_prior)                0.69      0.49     0.03     1.85 1.00
    ## cor(Intercept,conditionlow_prior)    -0.16      0.52    -0.95     0.89 1.00
    ##                                   Bulk_ESS Tail_ESS
    ## sd(Intercept)                         2029     2856
    ## sd(conditionlow_prior)                1459     2350
    ## cor(Intercept,conditionlow_prior)     3401     2607
    ## 
    ## ~submission_id (Number of levels: 121) 
    ##                                   Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(Intercept)                         2.76      0.65     1.71     4.22 1.00
    ## sd(conditionlow_prior)                1.45      0.76     0.10     2.97 1.00
    ## cor(Intercept,conditionlow_prior)    -0.59      0.37    -0.98     0.48 1.00
    ##                                   Bulk_ESS Tail_ESS
    ## sd(Intercept)                         1225     2819
    ## sd(conditionlow_prior)                 789     1344
    ## cor(Intercept,conditionlow_prior)     2182     2307
    ## 
    ## Population-Level Effects: 
    ##                    Estimate Est.Error l-95% CI u-95% CI Rhat Bulk_ESS Tail_ESS
    ## Intercept              0.86      0.54    -0.14     1.99 1.00     1921     2515
    ## conditionlow_prior     0.18      0.44    -0.73     1.02 1.00     3376     3191
    ## 
    ## Draws were sampled using sampling(NUTS). For each parameter, Bulk_ESS
    ## and Tail_ESS are effective sample size measures, and Rhat is the potential
    ## scale reduction factor on split chains (at convergence, Rhat = 1).

The same analysis is done with the rate of “exceptive” answers only. The
same hypothesis is tested (i.e., more exceptive answers are expected in
the lowPrior than in the highPrior condition).

``` r
d_main_exceptive_binary <- d_main_clean %>% 
  mutate(is_exceptive = ifelse(category == "exceptive", 1, 0)) 

priors <- set_prior("student_t(1, 0, 0.25)", class = "b")

lm_exceptive <- brm(
  is_exceptive ~ condition + (1 + condition | submission_id) + (1 + condition | itemName),
  data = d_main_exceptive_binary,
  family = "bernoulli",
  prior = priors,
  control = list(adapt_delta = 0.95),
  iter = 3000,
  chains = 4
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
summary(lm_exceptive)
```

    ##  Family: bernoulli 
    ##   Links: mu = logit 
    ## Formula: is_exceptive ~ condition + (1 + condition | submission_id) + (1 + condition | itemName) 
    ##    Data: d_main_exceptive_binary (Number of observations: 456) 
    ##   Draws: 4 chains, each with iter = 3000; warmup = 1500; thin = 1;
    ##          total post-warmup draws = 6000
    ## 
    ## Group-Level Effects: 
    ## ~itemName (Number of levels: 10) 
    ##                                   Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(Intercept)                         1.49      0.57     0.67     2.80 1.00
    ## sd(conditionlow_prior)                1.22      0.72     0.10     2.90 1.00
    ## cor(Intercept,conditionlow_prior)     0.09      0.48    -0.77     0.93 1.00
    ##                                   Bulk_ESS Tail_ESS
    ## sd(Intercept)                         3256     4254
    ## sd(conditionlow_prior)                1888     1855
    ## cor(Intercept,conditionlow_prior)     3357     3560
    ## 
    ## ~submission_id (Number of levels: 121) 
    ##                                   Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(Intercept)                         1.39      0.48     0.54     2.49 1.00
    ## sd(conditionlow_prior)                0.80      0.57     0.04     2.12 1.00
    ## cor(Intercept,conditionlow_prior)    -0.24      0.54    -0.97     0.89 1.00
    ##                                   Bulk_ESS Tail_ESS
    ## sd(Intercept)                         1587     2311
    ## sd(conditionlow_prior)                1385     2921
    ## cor(Intercept,conditionlow_prior)     3536     3442
    ## 
    ## Population-Level Effects: 
    ##                    Estimate Est.Error l-95% CI u-95% CI Rhat Bulk_ESS Tail_ESS
    ## Intercept             -2.88      0.67    -4.31    -1.70 1.00     3309     3610
    ## conditionlow_prior     0.41      0.53    -0.36     1.68 1.00     4073     2941
    ## 
    ## Draws were sampled using sampling(NUTS). For each parameter, Bulk_ESS
    ## and Tail_ESS are effective sample size measures, and Rhat is the potential
    ## scale reduction factor on split chains (at convergence, Rhat = 1).

We also check whether there is a credible difference between the rate of
taciturn responses in the two conditions, by fitting a Bayesian logistic
regression with a main effect of condition and maximal random effects.
We expect more taciturn responses in the highPrior condition compared to
the lowPrior condition.

``` r
d_main_taciturn_binary <- d_main_clean %>% 
  mutate(is_taciturn = ifelse(category == "taciturn", 1, 0)) 

lm_taciturn <- brm(
  is_taciturn ~ condition + (1 + condition | submission_id) + (1 + condition | itemName),
  data = d_main_taciturn_binary,
  family = "bernoulli",
  prior = priors,
  control = list(adapt_delta = 0.95),
  iter = 3000,
  chains = 4
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
summary(lm_taciturn)
```

    ##  Family: bernoulli 
    ##   Links: mu = logit 
    ## Formula: is_taciturn ~ condition + (1 + condition | submission_id) + (1 + condition | itemName) 
    ##    Data: d_main_taciturn_binary (Number of observations: 456) 
    ##   Draws: 4 chains, each with iter = 3000; warmup = 1500; thin = 1;
    ##          total post-warmup draws = 6000
    ## 
    ## Group-Level Effects: 
    ## ~itemName (Number of levels: 10) 
    ##                                   Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(Intercept)                         1.72      0.57     0.87     3.06 1.00
    ## sd(conditionlow_prior)                0.68      0.54     0.02     2.02 1.00
    ## cor(Intercept,conditionlow_prior)    -0.09      0.54    -0.94     0.90 1.00
    ##                                   Bulk_ESS Tail_ESS
    ## sd(Intercept)                         2479     4118
    ## sd(conditionlow_prior)                2595     3384
    ## cor(Intercept,conditionlow_prior)     6219     4220
    ## 
    ## ~submission_id (Number of levels: 121) 
    ##                                   Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(Intercept)                         3.56      0.83     2.19     5.45 1.01
    ## sd(conditionlow_prior)                1.76      0.91     0.15     3.67 1.01
    ## cor(Intercept,conditionlow_prior)    -0.52      0.37    -0.97     0.49 1.00
    ##                                   Bulk_ESS Tail_ESS
    ## sd(Intercept)                         1394     2641
    ## sd(conditionlow_prior)                 873     1202
    ## cor(Intercept,conditionlow_prior)     3018     2726
    ## 
    ## Population-Level Effects: 
    ##                    Estimate Est.Error l-95% CI u-95% CI Rhat Bulk_ESS Tail_ESS
    ## Intercept             -2.02      0.73    -3.52    -0.63 1.00     3060     3820
    ## conditionlow_prior    -0.24      0.39    -1.18     0.36 1.00     4879     3154
    ## 
    ## Draws were sampled using sampling(NUTS). For each parameter, Bulk_ESS
    ## and Tail_ESS are effective sample size measures, and Rhat is the potential
    ## scale reduction factor on split chains (at convergence, Rhat = 1).
