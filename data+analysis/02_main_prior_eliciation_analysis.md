QA prior elicitation & free typing analysis
================
Polina Tsvilodub
2022-11-06

## Intro

Below, exploratory analysis of the prior elicitation QA experiment data
can be found. In the end, the results are compared against the free
production results. Details of the free production analysis can be found
[here](https://github.com/magpie-ea/magpie3-qa-overinfo-free-production/blob/main/data%2Banalysis/01_main_free_typing_analysis.md).

Participants failing all attention checks (3 out of 11 trials) are
excluded from analysis. The attention checks consisted of trials where
participants read instructions to move all sliders all the way to the
left or to the right.

    ## # A tibble: 10 × 3
    ##    itemName               passed_subj     n
    ##    <chr>                  <lgl>       <int>
    ##  1 airport-europe-UPDATED FALSE          20
    ##  2 airport-usa            FALSE          45
    ##  3 art-drawing            FALSE          40
    ##  4 art-painting           FALSE          20
    ##  5 carRental-fun          FALSE          40
    ##  6 carRental-moving       FALSE          25
    ##  7 jobCenter-engineer     FALSE          15
    ##  8 jobCenter-office       FALSE          30
    ##  9 music-hardrock         FALSE          30
    ## 10 music-softrock         FALSE          20

    ## Numbrer of subjects who failed attention checks:  19

    ## 
    ## Subject exclusion rate:  0.2375

To understand what is going on in the attention checks, plot the ratings
in the attention checking trials only, selecting participants who
failed. It seems that many participants simply ignored the instructions
and followed “anticipated” ratings.

``` r
df_attention %>%
  filter(submission_id %in% subj_id_attention_fails) %>%
  mutate(answerType = factor(answerType, levels=answerOrder)) %>%
  group_by(itemName, answerType) %>%
  summarize(mean_response = mean(response)) %>%
  ggplot(aes(x = answerType, fill = answerType, y = mean_response)) +
  geom_col() +
  facet_wrap(itemName~., ncol=4) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  theme(strip.text.x = element_text(size = 10)) +
  theme(panel.spacing = unit(2, "lines")) +
  ylab("Mean ratings") +
  xlab("Alternative type")
```

    ## `summarise()` has grouped output by 'itemName'. You can override using the
    ## `.groups` argument.

![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

We further exclude participants who provide the same responses on all
trials (i.e. responses within the range of 5 points, basically just
click trough the experiment).

    ## # A tibble: 40 × 6
    ## # Groups:   submission_id [1]
    ##    itemName                 submission_id answerType     respo…¹ cente…² bad_s…³
    ##    <chr>                            <dbl> <chr>            <dbl>   <dbl> <lgl>  
    ##  1 petAdoption-dogs                  4476 competitor           0     -50 TRUE   
    ##  2 petAdoption-dogs                  4476 sameCategory1        0     -50 TRUE   
    ##  3 petAdoption-dogs                  4476 sameCategory2        0     -50 TRUE   
    ##  4 petAdoption-dogs                  4476 otherCategory1       0     -50 TRUE   
    ##  5 petAdoption-dogs                  4476 otherCategory2       0     -50 TRUE   
    ##  6 touristInfo-childTheatre          4476 competitor           3     -47 TRUE   
    ##  7 touristInfo-childTheatre          4476 sameCategory1        3     -47 TRUE   
    ##  8 touristInfo-childTheatre          4476 sameCategory2        3     -47 TRUE   
    ##  9 touristInfo-childTheatre          4476 otherCategory1       3     -47 TRUE   
    ## 10 touristInfo-childTheatre          4476 otherCategory2       3     -47 TRUE   
    ## # … with 30 more rows, and abbreviated variable names ¹​response,
    ## #   ²​centered_response, ³​bad_subj

    ## 
    ## number of subjects who provided the same responses within 5 points on all main trials: 1

Characteristics of the analysed clean dataset:

    ## 
    ## Number of analysed vignette responses:  480

    ## # A tibble: 36 × 2
    ##    itemName                                 n
    ##    <chr>                                <int>
    ##  1 bar-tea                                  7
    ##  2 bar-whiteWine                           16
    ##  3 bookingAgency-highClassAccommodation     9
    ##  4 bookingAgency-lowClassAccommodation     18
    ##  5 books-fantasy                           13
    ##  6 books-romance                           11
    ##  7 cafe-pie                                10
    ##  8 cafe-pizza                              14
    ##  9 clothing-beach                          16
    ## 10 clothing-winter                         10
    ## # … with 26 more rows

    ## 
    ## average number of responses per vignette: 13.33333

    ## 
    ## vignette with most responses:  bookingAgency-lowClassAccommodation 18

    ## 
    ## vignette with least responses:  bar-tea 7

The first plot below shows the raw prior ratings (y-axis) against the
alternative category (i.e., competitor, sameCategory1, otherCategory1
etc; x-axis). The second plot shows only by-vignette by-alternative
average ratings across participants. The horizontal dashed line
represents no change in beliefs of the participants about the
alternative, given the context. The error bars represent 95%
bootstrapped credible intervals.

    ## Warning: `as_data_frame()` was deprecated in tibble 2.0.0.
    ## ℹ Please use `as_tibble()` instead.
    ## ℹ The signature and semantics have changed, see `?as_tibble`.
    ## ℹ The deprecated feature was likely used in the purrr package.
    ##   Please report the issue at <]8;;https://github.com/tidyverse/purrr/issueshttps://github.com/tidyverse/purrr/issues]8;;>.

    ## Warning: `cols` is now required when using unnest().
    ## Please use `cols = c(strap)`

    ## `summarise()` has grouped output by 'itemName'. You can override using the
    ## `.groups` argument.

![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-10-2.png)<!-- -->

The global plot below shows by-category ratings averaging over
vignettes. The error bars represent 95% bootstrapped credible intervals.

    ## Warning: `cols` is now required when using unnest().
    ## Please use `cols = c(strap)`

![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-11-1.png)<!-- -->

The plot below shows the raw by-vignette by-alternative ratings (small
points) with labels representing the actual alternative options. The
large points indicate the by-vignette by-alternative means. **Please
note the varying order of the answer alternative categories on the
x-axis (color).**

    ## `summarise()` has grouped output by 'answerOption_string', 'answerType'. You
    ## can override using the `.groups` argument.

![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-12-1.png)<!-- -->

## Comparing prior ratings to free production

The plot below combines free production response rates with prior
ratings. More specifically, the x axis shows the categorized free
production response proportions (over participants) as bars. The prior
elicitation raw responses were collapsed into the categories
‘competitor’, ‘sameCategory’ (comprising ratings for ‘sameCategory1’ and
‘sameCategory2’ alternatives, respectively) and ‘otherCategory’
(collapsing ‘otherCategory1’ and ‘otherCategory2’ ratings). The raw
responses (samller points) as well as by-item by-alternative means
(larger points) are added in the respective answer categories for easier
comparison. The horizontal dashed line represents no change in
participants’ beliefs in the prior rating experiment.

![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-15-1.png)<!-- -->

Fit a linear model as a baseline, predicting the response type
proportion from the respective prior rating:

``` r
df_long_scaled4lm <- df_clean_main_wItems_long2_scaled %>% 
  #filter(answerType_string == answerType) %>%
  select(itemName, answerType, mean_response) %>%
  unique() %>% 
  pivot_wider(names_from = "answerType", values_from = "mean_response", values_fn = mean) %>%
  pivot_longer(cols = -itemName, names_to = "answerType", values_to = "mean_rating")

df_prior_freeProd <- d_clean_main_collapsedCompetitor_summary_100 %>% 
  left_join(., df_long_scaled4lm, by=c('itemName', 'answerType')) %>%
  filter(answerType %in% c("competitor", "sameCategory", "otherCategory"))

lm_freeProd_prior <- lme4::lmer(responseCategory_proportion ~ mean_rating + (1 | itemName), data = df_prior_freeProd)
summary(lm_freeProd_prior)
```

    ## Linear mixed model fit by REML ['lmerMod']
    ## Formula: responseCategory_proportion ~ mean_rating + (1 | itemName)
    ##    Data: df_prior_freeProd
    ## 
    ## REML criterion at convergence: -38.9
    ## 
    ## Scaled residuals: 
    ##      Min       1Q   Median       3Q      Max 
    ## -2.29214 -0.62103  0.03121  0.33244  2.04832 
    ## 
    ## Random effects:
    ##  Groups   Name        Variance Std.Dev.
    ##  itemName (Intercept) 0.003313 0.05756 
    ##  Residual             0.027900 0.16703 
    ## Number of obs: 70, groups:  itemName, 36
    ## 
    ## Fixed effects:
    ##             Estimate Std. Error t value
    ## (Intercept) -0.24585    0.09901  -2.483
    ## mean_rating  0.87237    0.16320   5.345
    ## 
    ## Correlation of Fixed Effects:
    ##             (Intr)
    ## mean_rating -0.974

``` r
# regressing the proportion of the response category (competitor / same / other category) against the mean rating of the competitor / sameCategory / otherCategory option for the item linearly
lm_freeProd_prior_brm <- brms::brm(responseCategory_proportion ~ mean_rating + (1 | itemName), 
                                   data = df_prior_freeProd,
                                   control = list(adapt_delta = 0.99),
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
summary(lm_freeProd_prior_brm)
```

    ##  Family: gaussian 
    ##   Links: mu = identity; sigma = identity 
    ## Formula: responseCategory_proportion ~ mean_rating + (1 | itemName) 
    ##    Data: df_prior_freeProd (Number of observations: 70) 
    ##   Draws: 4 chains, each with iter = 4000; warmup = 2000; thin = 1;
    ##          total post-warmup draws = 8000
    ## 
    ## Group-Level Effects: 
    ## ~itemName (Number of levels: 36) 
    ##               Estimate Est.Error l-95% CI u-95% CI Rhat Bulk_ESS Tail_ESS
    ## sd(Intercept)     0.07      0.04     0.00     0.15 1.00     1259     2385
    ## 
    ## Population-Level Effects: 
    ##             Estimate Est.Error l-95% CI u-95% CI Rhat Bulk_ESS Tail_ESS
    ## Intercept      -0.27      0.11    -0.49    -0.05 1.00     3506     4680
    ## mean_rating     0.91      0.19     0.55     1.29 1.00     3379     4896
    ## 
    ## Family Specific Parameters: 
    ##       Estimate Est.Error l-95% CI u-95% CI Rhat Bulk_ESS Tail_ESS
    ## sigma     0.17      0.02     0.13     0.21 1.00     2309     3021
    ## 
    ## Draws were sampled using sampling(NUTS). For each parameter, Bulk_ESS
    ## and Tail_ESS are effective sample size measures, and Rhat is the potential
    ## scale reduction factor on split chains (at convergence, Rhat = 1).

``` r
df_long_scaled4lm_wide <- df_long_scaled4lm %>%
  pivot_wider(names_from = "answerType", values_from = "mean_rating")

df_prior_freeProd_raw <- read_delim("results_QA-overinfo-freeTyping-extendedExpt_100_anonymized_categorized.csv") %>% 
  filter(trial_type == "main") %>%
  filter(category != 'yes') %>%
  left_join(., df_long_scaled4lm_wide, by=c('itemName')) %>%
  mutate(
    category = ifelse(category == 'competitor/other', 'competitor', category),
    category = factor(category, levels = c('competitor', 'sameCategory', 'otherCategory', 'fullList', 'taciturn', 'other'))
    )
# df_prior_freeProd_raw %>% write_csv("data/results_QA-overinfo-freeTyping_priorElicitation01_pilots_summary.csv")

contrasts(df_prior_freeProd_raw$category)
```

    ##               sameCategory otherCategory fullList taciturn other
    ## competitor               0             0        0        0     0
    ## sameCategory             1             0        0        0     0
    ## otherCategory            0             1        0        0     0
    ## fullList                 0             0        1        0     0
    ## taciturn                 0             0        0        1     0
    ## other                    0             0        0        0     1

``` r
# exploring multinomial regression, regressing the raw category of the response against the mean ratings for all options as numeric predictors, with by-item and by-subject effects
multinom_freeProd_prior_brm <- brms::brm(category ~ competitor + sameCategory + otherCategory + (1 | itemName) + (1 | submission_id), 
                                   data = df_prior_freeProd_raw,
                                   family = "categorical",
                                   control = list(adapt_delta = 0.99),
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
summary(multinom_freeProd_prior_brm)
```

    ##  Family: categorical 
    ##   Links: musameCategory = logit; muotherCategory = logit; mufullList = logit; mutaciturn = logit; muother = logit 
    ## Formula: category ~ competitor + sameCategory + otherCategory + (1 | itemName) + (1 | submission_id) 
    ##    Data: df_prior_freeProd_raw (Number of observations: 785) 
    ##   Draws: 4 chains, each with iter = 4000; warmup = 2000; thin = 1;
    ##          total post-warmup draws = 8000
    ## 
    ## Group-Level Effects: 
    ## ~itemName (Number of levels: 36) 
    ##                               Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(musameCategory_Intercept)      0.74      0.22     0.34     1.20 1.00
    ## sd(muotherCategory_Intercept)     2.91      2.68     0.10    10.01 1.00
    ## sd(mufullList_Intercept)          1.67      1.07     0.11     4.21 1.00
    ## sd(mutaciturn_Intercept)          0.83      0.22     0.44     1.30 1.00
    ## sd(muother_Intercept)             0.90      0.24     0.50     1.42 1.00
    ##                               Bulk_ESS Tail_ESS
    ## sd(musameCategory_Intercept)      2291     2780
    ## sd(muotherCategory_Intercept)     1626     1861
    ## sd(mufullList_Intercept)          1244     1630
    ## sd(mutaciturn_Intercept)          2606     3188
    ## sd(muother_Intercept)             2206     2677
    ## 
    ## ~submission_id (Number of levels: 100) 
    ##                               Estimate Est.Error l-95% CI u-95% CI Rhat
    ## sd(musameCategory_Intercept)      1.09      0.22     0.69     1.57 1.00
    ## sd(muotherCategory_Intercept)     2.04      1.85     0.07     6.87 1.00
    ## sd(mufullList_Intercept)          3.05      1.14     1.34     5.77 1.00
    ## sd(mutaciturn_Intercept)          2.66      0.34     2.08     3.40 1.00
    ## sd(muother_Intercept)             0.64      0.26     0.08     1.15 1.00
    ##                               Bulk_ESS Tail_ESS
    ## sd(musameCategory_Intercept)      2561     4217
    ## sd(muotherCategory_Intercept)     2356     3548
    ## sd(mufullList_Intercept)          1915     2906
    ## sd(mutaciturn_Intercept)          2515     4591
    ## sd(muother_Intercept)             1313     1270
    ## 
    ## Population-Level Effects: 
    ##                               Estimate Est.Error l-95% CI u-95% CI Rhat
    ## musameCategory_Intercept          0.55      1.29    -2.00     3.14 1.00
    ## muotherCategory_Intercept       -30.18     22.87   -90.09    -5.75 1.00
    ## mufullList_Intercept            -13.43      6.23   -28.36    -4.56 1.00
    ## mutaciturn_Intercept              0.71      1.39    -2.05     3.46 1.00
    ## muother_Intercept                -0.91      1.42    -3.76     1.86 1.00
    ## musameCategory_competitor        -6.53      1.86   -10.46    -2.97 1.00
    ## musameCategory_sameCategory       5.99      1.74     2.62     9.58 1.00
    ## musameCategory_otherCategory     -2.17      1.74    -5.74     1.17 1.00
    ## muotherCategory_competitor       18.86     26.83   -16.09    86.09 1.00
    ## muotherCategory_sameCategory      2.22     19.72   -37.20    41.42 1.00
    ## muotherCategory_otherCategory    11.96     19.42   -18.01    56.97 1.00
    ## mufullList_competitor           -18.73     10.36   -44.12    -3.15 1.00
    ## mufullList_sameCategory          27.35     13.34     9.10    60.75 1.00
    ## mufullList_otherCategory          8.29      6.99    -3.04    24.55 1.00
    ## mutaciturn_competitor            -8.87      1.98   -12.80    -5.07 1.00
    ## mutaciturn_sameCategory           5.69      1.84     2.13     9.37 1.00
    ## mutaciturn_otherCategory          3.38      1.72     0.05     6.73 1.00
    ## muother_competitor               -8.71      2.20   -13.16    -4.42 1.00
    ## muother_sameCategory              7.62      2.12     3.67    12.00 1.00
    ## muother_otherCategory             4.23      1.88     0.61     8.00 1.00
    ##                               Bulk_ESS Tail_ESS
    ## musameCategory_Intercept          5995     5615
    ## muotherCategory_Intercept         1904     1268
    ## mufullList_Intercept              2396     2279
    ## mutaciturn_Intercept              5233     5627
    ## muother_Intercept                 4755     5885
    ## musameCategory_competitor         4113     4620
    ## musameCategory_sameCategory       4457     4916
    ## musameCategory_otherCategory      4668     5319
    ## muotherCategory_competitor        2219     1408
    ## muotherCategory_sameCategory      2603     1926
    ## muotherCategory_otherCategory     3148     1852
    ## mufullList_competitor             2580     1702
    ## mufullList_sameCategory           2419     1872
    ## mufullList_otherCategory          2840     1925
    ## mutaciturn_competitor             4437     5446
    ## mutaciturn_sameCategory           4954     5363
    ## mutaciturn_otherCategory          5125     5730
    ## muother_competitor                3667     4548
    ## muother_sameCategory              4445     5408
    ## muother_otherCategory             4396     5242
    ## 
    ## Draws were sampled using sampling(NUTS). For each parameter, Bulk_ESS
    ## and Tail_ESS are effective sample size measures, and Rhat is the potential
    ## scale reduction factor on split chains (at convergence, Rhat = 1).

## Exploratory analysis without participant exclusions

Since a relatively large proportion of participants was excluded due to
attention check failure, the plot below explores whether there are
qualitative differences between the cleaned results with 60 subjects and
non-cleaned results with 80 subjects. This does not seem to be the case.

![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-18-1.png)<!-- -->

## Extracting weakest items

Below, the vignettes are sorted in terms of difference between mean
sizes. The items with smaller differences are taken to be weaker items.

``` r
df_weak_items <- df_clean_main_summary_unique %>% group_by(itemName) %>%
  mutate(response_range = max(mean) - min(mean)) %>%
  arrange(response_range)

df_weak_items %>% select(itemName, response_range) %>% unique()
```

    ## # A tibble: 36 × 2
    ## # Groups:   itemName [36]
    ##    itemName                             response_range
    ##    <chr>                                         <dbl>
    ##  1 electronics-console                            8.91
    ##  2 plants-green                                  17.5 
    ##  3 plants-flowers                                17.8 
    ##  4 furniture-indoors                             21.0 
    ##  5 friendsActivities-videoEntertainment          21.6 
    ##  6 movie-fantasy                                 24.4 
    ##  7 waterSport-motor                              27.5 
    ##  8 cafe-pizza                                    30.0 
    ##  9 disney-princess                               30.1 
    ## 10 dutyFree-sweets                               30.6 
    ## # … with 26 more rows

``` r
cat("Top 10 weakes items (worst to best): ", df_weak_items %>% pull(itemName) %>% unique() %>% .[1:10])
```

    ## Top 10 weakes items (worst to best):  electronics-console plants-green plants-flowers furniture-indoors friendsActivities-videoEntertainment movie-fantasy waterSport-motor cafe-pizza disney-princess dutyFree-sweets

Below, several further computations try to extract in a principled way
which items did not work well based on free production + slider rating
results.

For checking if the prior elicitation values are predictive of the
proportion of free production response patterns (specifically, taciturn
rate), several metrics on prior elicitation results can be computed:

Option 1: compute the difference between the mean (by-vignette)
competitor rating and the highest alternative rating. A difference of 0
indicates that the competitor was rated highest, while a negative
difference means that another option was rated higher.

Option 2: compute the difference between the competitor rating and the
mean over the same category alternatives (a) or other category
alternatives (b).

Option 3: compute the average change in beliefs (i.e., the absolute
difference to the rating 50 ) of the competitor (an approximation of the
presence of an obvious alternative). Vignettes with smallest difference
are assumed to be weakest.

For checking if vignette worked well overall, we focus on the pattern of
the free production data. More specifically, we assume that the
prototype response pattern would put 0.7 of responses into the
competitor category and 0.3 of responses into sameCategory responses,
and 0 in other response categories.

Option 4: compute a distance between the prototype distribution and the
observed distribution – Wasserstein distance

Option 5: TBD: compute mean differences on prior elicitation data but
add some uncertainty term

``` r
# option 1: compute differences between competitor and the most salient other option
df_clean_main_summary_unique_wide <- df_clean_main_summary_unique %>%
  group_by(itemName) %>% select(-n, -empirical_stat, -ci_lower, -ci_upper) %>%
  mutate(max_rating = max(mean), answerType = factor(answerType)) %>% ungroup() %>%
  pivot_wider(names_from = "answerType", values_from = "mean") %>%
  rowwise() %>%
  mutate(competitor_vs_maxAlternative = competitor - max_rating,
         competitor_vs_sameCategory = competitor - mean(sameCategory1, sameCategory2), # option 2a
         competitor_vs_otherCategory = competitor - mean(otherCategory1, otherCategory2), # option 2b
          sameCat_changeBeliefs = competitor-50) # option 3 
```

    ## worst items according to option 1:  bookingAgency-lowClassAccommodation petAdoption-dogs clothing-beach movie-fantasy bookingAgency-highClassAccommodation kidsActivities-sports clothing-winter books-fantasy friendsActivities-videoEntertainment bar-tea

    ## 
    ## worst items according to option 2a (difference to same category):  bookingAgency-lowClassAccommodation petAdoption-dogs clothing-beach bookingAgency-highClassAccommodation books-fantasy bar-tea gym-yoga electronics-console disney-princess clothing-winter

    ## 
    ## worst items according to option 2b (difference to other category):  electronics-console movie-fantasy plants-flowers cafe-pizza plants-green friendsActivities-videoEntertainment clothing-beach furniture-indoors petAdoption-dogs waterSport-motor

    ## 
    ## worst items according to option 3 (change in beliefs for competitor):  petAdoption-dogs electronics-console friendsActivities-videoEntertainment furniture-indoors clothing-beach bookingAgency-lowClassAccommodation movie-fantasy bar-tea plants-green plants-flowers

Option 4:

``` r
d_clean_main_collapsedCompetitor_summary_100_wBaseline <- d_clean_main_collapsedCompetitor_summary_100 %>%
  mutate(expected_prop = case_when(
    answerType == "competitor" ~ 0.7,
    answerType == "sameCategory" ~ 0.3,
    TRUE ~ 0.00001
  ))

d_clean_main_collapsedCompetitor_summary_100_wBaseline <- d_clean_main_collapsedCompetitor_summary_100_wBaseline %>% group_by(itemName) %>%
  mutate(wasserstein_dist = sum(abs(responseCategory_proportion - expected_prop)))

cat("items with the largest Wasserstein distance relative to expected free production distribution:  ", d_clean_main_collapsedCompetitor_summary_100_wBaseline %>% arrange(desc(wasserstein_dist)) %>% pull(itemName) %>% unique() %>% .[1:10])
```

    ## items with the largest Wasserstein distance relative to expected free production distribution:   movie-fantasy friendsActivities-boardGames movie-western furniture-outdoors kidsActivities-crafts disney-action plants-green furniture-indoors electronics-console clothing-winter

As an alternative which might be more appropriate for a discrete
distribution, compute KL divergence between observed and expected
distribution.

``` r
itemNames <- d_clean_main_collapsedCompetitor_summary_100_wBaseline %>% arrange(itemName) %>% pull(itemName) %>% unique()

kl_divs <- c()

for (i in itemNames) {
  
  observed_dist <- d_clean_main_collapsedCompetitor_summary_100_wBaseline %>% filter(itemName == i) %>% arrange(answerType) %>% .$responseCategory_proportion
  expected_dist <- d_clean_main_collapsedCompetitor_summary_100_wBaseline %>% filter(itemName == i) %>% arrange(answerType) #%>% .$expected_prop
  if (sum(expected_dist$expected_prop) > 1) {
    expected_dist[expected_dist$answerType=='sameCategory', 'expected_prop'] <- 0.3 - 0.00001 * (length(observed_dist) - 2)
  }
  
  expected_dist <- expected_dist %>% .$expected_prop
  
  x <- rbind(observed_dist, expected_dist) 
  kl <- philentropy::KL(x)
  kl_divs <- append(kl_divs, as.numeric(kl))
}
```

    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.
    ## Metric: 'kullback-leibler' using unit: 'log2'; comparing: 2 vectors.

``` r
kl_divs
```

    ##  [1]  8.2437457  3.9618165  6.6400199  7.9216805  7.3910812  2.0816886
    ##  [7]  0.5720545  2.6546327  8.3399050  7.2473664  7.5477302 13.7096815
    ## [13]  3.7286617  3.2268571  8.9796874  3.0414063 10.6876804  6.8382030
    ## [19]  9.0059496  9.4982241  1.7084898  4.4616141  9.0744349  6.0201135
    ## [25] 12.3663661 12.6064759 11.4527131  3.6980451  8.4569034  9.3922394
    ## [31]  2.9848103  2.9714129  7.6709774  5.4236361  7.2960093  6.5754196

``` r
kl_df <- tibble('itemName' = itemNames, 'kl' = kl_divs) %>% arrange(desc(kl))
kl_df
```

    ## # A tibble: 36 × 2
    ##    itemName                        kl
    ##    <chr>                        <dbl>
    ##  1 disney-princess              13.7 
    ##  2 movie-western                12.6 
    ##  3 movie-fantasy                12.4 
    ##  4 petAdoption-dogs             11.5 
    ##  5 friendsActivities-boardGames 10.7 
    ##  6 furniture-outdoors            9.50
    ##  7 plants-green                  9.39
    ##  8 kidsActivities-crafts         9.07
    ##  9 furniture-indoors             9.01
    ## 10 electronics-console           8.98
    ## # … with 26 more rows

Checking if either measure derived from the prior elicitation correlates
well with the Wasserstein results or the raw taciturn proportion:

    ## correlation of by-vignette free production Wasserstein distances and prior elicitation differences between competitor and most salient alternative:  -0.2531127

    ## 
    ## 
    ## correlation of by-vignette free production Wasserstein distances and prior elicitation differences between competitor and same category alternatives:  -0.3602663

    ## 
    ## 
    ## correlation of by-vignette free production Wasserstein distances and prior elicitation differences between competitor and other category alternatives:  -0.4814068

    ## 
    ## 
    ## correlation of by-vignette free production Wasserstein distances and prior elicitation changes in beliefs for competitor:  -0.2652146

    ## correlation of by-vignette free production taciturn response proportions and prior elicitation differences between competitor and most salient alternative:  -0.4466134

    ## 
    ## 
    ## correlation of by-vignette free production taciturn response proportions and prior elicitation differences between competitor and same category alternatives:  -0.4315435

    ## 
    ## 
    ## correlation of by-vignette free production taciturn response proportions and prior elicitation differences between competitor and other category alternatives:  -0.4837104

    ## 
    ## 
    ## correlation of by-vignette free production taciturn response proportions and prior elicitation changes in beliefs for competitor:  -0.4177378

Alternatively, fitting linear models:

    ## predicting by-vignette free production Wasserstein distances as a function of prior elicitation differences between competitor and most salient alternative:

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ competitor_vs_maxAlternative_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.67807 -0.34171  0.03985  0.33346  0.62191 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                         0.87806    0.07238  12.131 6.66e-14 ***
    ## competitor_vs_maxAlternative_alpha -0.01884    0.01235  -1.526    0.136    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.382 on 34 degrees of freedom
    ## Multiple R-squared:  0.06407,    Adjusted R-squared:  0.03654 
    ## F-statistic: 2.327 on 1 and 34 DF,  p-value: 0.1364

    ## 
    ## 
    ## predicting by-vignette free production Wasserstein distances as a function of prior elicitation differences between competitor and same category alternatives:

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ competitor_vs_sameCategory_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.64276 -0.32718  0.00682  0.25676  0.72290 
    ## 
    ## Coefficients:
    ##                                   Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                       1.044298   0.079497  13.136 7.06e-15 ***
    ## competitor_vs_sameCategory_alpha -0.009415   0.004181  -2.252   0.0309 *  
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3684 on 34 degrees of freedom
    ## Multiple R-squared:  0.1298, Adjusted R-squared:  0.1042 
    ## F-statistic: 5.071 on 1 and 34 DF,  p-value: 0.0309

    ## 
    ## 
    ## predicting by-vignette free production Wasserstein distances as a function of prior elicitation differences between competitor and other category alternatives:

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ competitor_vs_otherCategory_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.82820 -0.22799  0.02744  0.31744  0.59994 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                        1.404197   0.158740   8.846 2.44e-10 ***
    ## competitor_vs_otherCategory_alpha -0.014367   0.004486  -3.203  0.00295 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3461 on 34 degrees of freedom
    ## Multiple R-squared:  0.2318, Adjusted R-squared:  0.2092 
    ## F-statistic: 10.26 on 1 and 34 DF,  p-value: 0.002954

    ## 
    ## 
    ## predicting by-vignette free production Wasserstein distances as a function of prior elicitation changes in beliefs for competitor:

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ competitor_vs_beliefsChange_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.65944 -0.32958  0.09866  0.27035  0.67318 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)   
    ## (Intercept)                        0.603092   0.213814   2.821  0.00794 **
    ## competitor_vs_beliefsChange_alpha -0.009379   0.005848  -1.604  0.11799   
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3807 on 34 degrees of freedom
    ## Multiple R-squared:  0.07034,    Adjusted R-squared:  0.043 
    ## F-statistic: 2.572 on 1 and 34 DF,  p-value: 0.118

    ## predicting by-vignette free production taciturn response proportions as a function of prior elicitation differences between competitor and most salient alternative:

    ## 
    ## Call:
    ## lm(formula = taciturn_props ~ competitor_vs_maxAlternative_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.22058 -0.07251 -0.01133  0.07070  0.22942 
    ## 
    ## Coefficients:
    ##                                     Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                         0.270584   0.022481  12.036 8.28e-14 ***
    ## competitor_vs_maxAlternative_alpha -0.011161   0.003835  -2.911  0.00632 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1187 on 34 degrees of freedom
    ## Multiple R-squared:  0.1995, Adjusted R-squared:  0.1759 
    ## F-statistic: 8.472 on 1 and 34 DF,  p-value: 0.006323

    ## 
    ## 
    ## predicting by-vignette free production taciturn response proportions as a function of prior elicitation differences between competitor and same category alternatives:

    ## 
    ## Call:
    ## lm(formula = taciturn_props ~ competitor_vs_sameCategory_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.21711 -0.07734 -0.01271  0.07059  0.31800 
    ## 
    ## Coefficients:
    ##                                   Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                       0.347450   0.025817  13.458 3.53e-15 ***
    ## competitor_vs_sameCategory_alpha -0.003787   0.001358  -2.789  0.00859 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1196 on 34 degrees of freedom
    ## Multiple R-squared:  0.1862, Adjusted R-squared:  0.1623 
    ## F-statistic: 7.781 on 1 and 34 DF,  p-value: 0.00859

    ## 
    ## 
    ## predicting by-vignette free production taciturn response proportions as a function of prior elicitation differences between competitor and other category alternatives:

    ## 
    ## Call:
    ## lm(formula = taciturn_props ~ competitor_vs_otherCategory_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.25882 -0.07908  0.02275  0.07398  0.20506 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                        0.461520   0.053233   8.670 3.95e-10 ***
    ## competitor_vs_otherCategory_alpha -0.004848   0.001504  -3.223   0.0028 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1161 on 34 degrees of freedom
    ## Multiple R-squared:  0.234,  Adjusted R-squared:  0.2114 
    ## F-statistic: 10.39 on 1 and 34 DF,  p-value: 0.002801

    ## 
    ## 
    ## predicting by-vignette free production taciturn response proportions as a function of prior elicitation changes in beliefs for competitor:

    ## 
    ## Call:
    ## lm(formula = taciturn_props ~ competitor_vs_beliefsChange_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.21407 -0.09228  0.01119  0.06399  0.29003 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)  
    ## (Intercept)                        0.128476   0.067663   1.899   0.0661 .
    ## competitor_vs_beliefsChange_alpha -0.004961   0.001851  -2.681   0.0112 *
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1205 on 34 degrees of freedom
    ## Multiple R-squared:  0.1745, Adjusted R-squared:  0.1502 
    ## F-statistic: 7.187 on 1 and 34 DF,  p-value: 0.01124

Combine all these results to see if the selected vignettes overlap.
Additionally, manually extracted (by Polina) weak items are added.

Option 5: explore influence of adding standard deviation on predicting
wasserstein distance / taciturn response proportion

``` r
# extract mean + SD by item
sliderRating_competitor_mean_sd_sum <- df_clean_main_summary_sd %>% filter(answerType == "competitor") %>%
  select(itemName, mean, sd) %>% unique() 
sliderRating_sameCat_mean_sd_sum <- df_clean_main_summary_sd %>% filter(answerType == "sameCategory") %>%
  select(itemName, mean, sd) %>% unique() 

lm_comp_wSD <- lm(wasserstein_dist_alpha ~ sliderRating_competitor_mean_sd_sum$mean + sliderRating_competitor_mean_sd_sum$sd)
summary(lm_comp_wSD)
```

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ sliderRating_competitor_mean_sd_sum$mean + 
    ##     sliderRating_competitor_mean_sd_sum$sd)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.62541 -0.32570  0.05164  0.29573  0.66948 
    ## 
    ## Coefficients:
    ##                                           Estimate Std. Error t value Pr(>|t|)
    ## (Intercept)                               0.825764   0.426102   1.938   0.0612
    ## sliderRating_competitor_mean_sd_sum$mean -0.005667   0.008467  -0.669   0.5079
    ## sliderRating_competitor_mean_sd_sum$sd    0.008494   0.014277   0.595   0.5559
    ##                                           
    ## (Intercept)                              .
    ## sliderRating_competitor_mean_sd_sum$mean  
    ## sliderRating_competitor_mean_sd_sum$sd    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3846 on 33 degrees of freedom
    ## Multiple R-squared:  0.07913,    Adjusted R-squared:  0.02332 
    ## F-statistic: 1.418 on 2 and 33 DF,  p-value: 0.2566

``` r
lm_sameCat_wSD <- lm(wasserstein_dist_alpha ~ sliderRating_sameCat_mean_sd_sum$mean + sliderRating_sameCat_mean_sd_sum$sd)
summary(lm_sameCat_wSD)
```

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ sliderRating_sameCat_mean_sd_sum$mean + 
    ##     sliderRating_sameCat_mean_sd_sum$sd)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.76952 -0.21927  0.01535  0.26117  0.79755 
    ## 
    ## Coefficients:
    ##                                        Estimate Std. Error t value Pr(>|t|)  
    ## (Intercept)                            0.975913   0.391031   2.496   0.0177 *
    ## sliderRating_sameCat_mean_sd_sum$mean  0.010384   0.005515   1.883   0.0686 .
    ## sliderRating_sameCat_mean_sd_sum$sd   -0.003265   0.015715  -0.208   0.8367  
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3791 on 33 degrees of freedom
    ## Multiple R-squared:  0.1054, Adjusted R-squared:  0.05122 
    ## F-statistic: 1.945 on 2 and 33 DF,  p-value: 0.1591

Note of more analysis options: KL divergence? Bootstrapping idea? also
compute Wasserstein distance (or thelike) on the slider rating results,
and compare that value to the values from free production?

## Preprocessing for RSA model fitting

``` r
# TODO: z-scoring?
df_clean_main_long_zScored <- df_clean_main_wItems_long %>% 
  group_by(itemName, answerType) %>%
  mutate(mean = mean(response),
         sd = sd(response),
         response_zscored = (response - mean) / sd,
         response_zscored = ifelse(is.na(response_zscored), 0, response_zscored),
         mean_zScored = mean(response_zscored)) 

df_clean_main_long_zScored_unique <- df_clean_main_long_zScored %>% 
  select(itemName, answerType, mean, mean_zScored) %>% unique()

#df_clean_main_long_zScored_unique %>% write_csv("priorElicitation_byVignette_byCategory_means.csv")
```
