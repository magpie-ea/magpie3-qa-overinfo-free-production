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

    ## # A tibble: 10 x 3
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

    ## `summarise()` regrouping output by 'itemName' (override with `.groups` argument)

![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

We further exclude participants who provide the same responses on all
trials (i.e. responses within the range of 5 points, basically just
click trough the experiment).

    ## # A tibble: 40 x 6
    ## # Groups:   submission_id [1]
    ##    itemName        submission_id answerType   response centered_respon… bad_subj
    ##    <chr>                   <dbl> <chr>           <dbl>            <dbl> <lgl>   
    ##  1 petAdoption-do…          4476 competitor          0              -50 TRUE    
    ##  2 petAdoption-do…          4476 sameCategor…        0              -50 TRUE    
    ##  3 petAdoption-do…          4476 sameCategor…        0              -50 TRUE    
    ##  4 petAdoption-do…          4476 otherCatego…        0              -50 TRUE    
    ##  5 petAdoption-do…          4476 otherCatego…        0              -50 TRUE    
    ##  6 touristInfo-ch…          4476 competitor          3              -47 TRUE    
    ##  7 touristInfo-ch…          4476 sameCategor…        3              -47 TRUE    
    ##  8 touristInfo-ch…          4476 sameCategor…        3              -47 TRUE    
    ##  9 touristInfo-ch…          4476 otherCatego…        3              -47 TRUE    
    ## 10 touristInfo-ch…          4476 otherCatego…        3              -47 TRUE    
    ## # … with 30 more rows

    ## 
    ## number of subjects who provided the same responses within 5 points on all main trials: 1

Characteristics of the analysed clean dataset:

    ## 
    ## Number of analysed vignette responses:  480

    ## # A tibble: 36 x 2
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

    ## Warning: `as_data_frame()` is deprecated as of tibble 2.0.0.
    ## Please use `as_tibble()` instead.
    ## The signature and semantics have changed, see `?as_tibble`.
    ## This warning is displayed once every 8 hours.
    ## Call `lifecycle::last_warnings()` to see where this warning was generated.

    ## Warning: `cols` is now required when using unnest().
    ## Please use `cols = c(strap)`

    ## `summarise()` regrouping output by 'itemName' (override with `.groups` argument)

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

    ## `summarise()` regrouping output by 'answerOption_string', 'answerType' (override
    ## with `.groups` argument)

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

## Exploratory analysis without participant exclusions

Since a relatively large proportion of participants was excluded due to
attention check failure, the plot below explores whether there are
qualitative differences between the cleaned results with 60 subjects and
non-cleaned results with 80 subjects. This does not seem to be the case.

![](02_main_prior_eliciation_analysis_files/figure-gfm/unnamed-chunk-16-1.png)<!-- -->

## Extracting weakest items

Below, the vignettes are sorted in terms of difference between mean
sizes. The items with smaller differences are taken to be weaker items.

``` r
df_weak_items <- df_clean_main_summary_unique %>% group_by(itemName) %>%
  mutate(response_range = max(mean) - min(mean)) %>%
  arrange(response_range)

df_weak_items %>% select(itemName, response_range) %>% unique()
```

    ## # A tibble: 36 x 2
    ## # Groups:   itemName [36]
    ##    itemName                             response_range
    ##    <chr>                                         <dbl>
    ##  1 electronics-console                            8.37
    ##  2 plants-green                                  17.7 
    ##  3 plants-flowers                                17.9 
    ##  4 friendsActivities-videoEntertainment          21.0 
    ##  5 furniture-indoors                             21.3 
    ##  6 movie-fantasy                                 24.1 
    ##  7 waterSport-motor                              27.3 
    ##  8 disney-princess                               29.8 
    ##  9 dutyFree-sweets                               30.1 
    ## 10 cafe-pizza                                    30.1 
    ## # … with 26 more rows

``` r
cat("Top 10 weakes items (worst to best): ", df_weak_items %>% pull(itemName) %>% unique() %>% .[1:10])
```

    ## Top 10 weakes items (worst to best):  electronics-console plants-green plants-flowers friendsActivities-videoEntertainment furniture-indoors movie-fantasy waterSport-motor disney-princess dutyFree-sweets cafe-pizza

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
  group_by(itemName) %>%
  mutate(max_rating = max(mean)) %>% ungroup() %>%
  pivot_wider(id_cols = c("itemName", "answerType", "max_rating"), names_from = "answerType", values_from = "mean") %>%
  rowwise() %>%
  mutate(competitor_vs_maxAlternative = competitor - max_rating,
         competitor_vs_sameCategory = competitor - mean(sameCategory1, sameCategory2), # option 2a
         competitor_vs_otherCategory = competitor - mean(otherCategory1, otherCategory2), # option 2b
          sameCat_changeBeliefs = competitor-50) # option 3 
```

    ## worst items according to option 1:  bookingAgency-lowClassAccommodation petAdoption-dogs clothing-beach movie-fantasy kidsActivities-sports bookingAgency-highClassAccommodation books-fantasy clothing-winter bar-tea friendsActivities-videoEntertainment

    ## 
    ## worst items according to option 2a (difference to same category):  bookingAgency-lowClassAccommodation petAdoption-dogs clothing-beach bookingAgency-highClassAccommodation books-fantasy bar-tea gym-yoga electronics-console disney-princess clothing-winter

    ## 
    ## worst items according to option 2b (difference to other category):  electronics-console movie-fantasy plants-flowers cafe-pizza plants-green friendsActivities-videoEntertainment clothing-beach furniture-indoors petAdoption-dogs waterSport-motor

    ## 
    ## worst items according to option 3 (change in beliefs for competitor):  petAdoption-dogs electronics-console friendsActivities-videoEntertainment furniture-indoors clothing-beach bookingAgency-lowClassAccommodation bar-tea movie-fantasy plants-green books-fantasy

Option 4:

``` r
d_clean_main_collapsedCompetitor_summary_100_wBaseline <- d_clean_main_collapsedCompetitor_summary_100 %>%
  mutate(expected_prop = case_when(
    answerType == "competitor" ~ 0.7,
    answerType == "sameCategory" ~ 0.3,
    TRUE ~ 0
  ))
d_clean_main_collapsedCompetitor_summary_100_wBaseline <- d_clean_main_collapsedCompetitor_summary_100_wBaseline %>% group_by(itemName) %>%
  mutate(wasserstein_dist = sum(abs(responseCategory_proportion - expected_prop)))

cat("items with the largest Wasserstein distance relative to expected free production distribution:  ", d_clean_main_collapsedCompetitor_summary_100_wBaseline %>% arrange(desc(wasserstein_dist)) %>% pull(itemName) %>% unique() %>% .[1:10])
```

    ## items with the largest Wasserstein distance relative to expected free production distribution:   movie-fantasy friendsActivities-boardGames movie-western furniture-outdoors kidsActivities-crafts disney-action plants-green furniture-indoors electronics-console clothing-winter

Checking if either measure derived from the prior elicitation correlates
well with the Wasserstein results or the raw taciturn proportion:

    ## correlation of by-vignette free production Wasserstein distances and prior elicitation differences between competitor and most salient alternative:  -0.2430015

    ## 
    ## 
    ## correlation of by-vignette free production Wasserstein distances and prior elicitation differences between competitor and same category alternatives:  -0.355204

    ## 
    ## 
    ## correlation of by-vignette free production Wasserstein distances and prior elicitation differences between competitor and other category alternatives:  -0.476675

    ## 
    ## 
    ## correlation of by-vignette free production Wasserstein distances and prior elicitation changes in beliefs for competitor:  -0.2600998

    ## correlation of by-vignette free production taciturn response proportions and prior elicitation differences between competitor and most salient alternative:  -0.4493714

    ## 
    ## 
    ## correlation of by-vignette free production taciturn response proportions and prior elicitation differences between competitor and same category alternatives:  -0.4326804

    ## 
    ## 
    ## correlation of by-vignette free production taciturn response proportions and prior elicitation differences between competitor and other category alternatives:  -0.4823134

    ## 
    ## 
    ## correlation of by-vignette free production taciturn response proportions and prior elicitation changes in beliefs for competitor:  -0.4148041

Alternatively, fitting linear models:

    ## predicting by-vignette free production Wasserstein distances as a function of prior elicitation differences between competitor and most salient alternative:

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ competitor_vs_maxAlternative_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.68048 -0.34412  0.03891  0.33024  0.61952 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                         0.88048    0.07248  12.148  6.4e-14 ***
    ## competitor_vs_maxAlternative_alpha -0.01813    0.01241  -1.461    0.153    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3831 on 34 degrees of freedom
    ## Multiple R-squared:  0.05905,    Adjusted R-squared:  0.03137 
    ## F-statistic: 2.134 on 1 and 34 DF,  p-value: 0.1533

    ## 
    ## 
    ## predicting by-vignette free production Wasserstein distances as a function of prior elicitation differences between competitor and same category alternatives:

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ competitor_vs_sameCategory_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.64043 -0.33013  0.00707  0.25608  0.72957 
    ## 
    ## Coefficients:
    ##                                   Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                       1.042063   0.079474  13.112 7.45e-15 ***
    ## competitor_vs_sameCategory_alpha -0.009250   0.004175  -2.216   0.0335 *  
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3691 on 34 degrees of freedom
    ## Multiple R-squared:  0.1262, Adjusted R-squared:  0.1005 
    ## F-statistic: 4.909 on 1 and 34 DF,  p-value: 0.03351

    ## 
    ## 
    ## predicting by-vignette free production Wasserstein distances as a function of prior elicitation differences between competitor and other category alternatives:

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ competitor_vs_otherCategory_alpha)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -0.8252 -0.2280  0.0207  0.3142  0.6055 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                        1.402205   0.159987   8.765 3.05e-10 ***
    ## competitor_vs_otherCategory_alpha -0.014295   0.004521  -3.162  0.00329 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3471 on 34 degrees of freedom
    ## Multiple R-squared:  0.2272, Adjusted R-squared:  0.2045 
    ## F-statistic: 9.997 on 1 and 34 DF,  p-value: 0.003291

    ## 
    ## 
    ## predicting by-vignette free production Wasserstein distances as a function of prior elicitation changes in beliefs for competitor:

    ## 
    ## Call:
    ## lm(formula = wasserstein_dist_alpha ~ competitor_vs_beliefsChange_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.66093 -0.33080  0.09659  0.26873  0.67890 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)   
    ## (Intercept)                        0.608484   0.214698   2.834  0.00768 **
    ## competitor_vs_beliefsChange_alpha -0.009230   0.005877  -1.571  0.12552   
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.3813 on 34 degrees of freedom
    ## Multiple R-squared:  0.06765,    Adjusted R-squared:  0.04023 
    ## F-statistic: 2.467 on 1 and 34 DF,  p-value: 0.1255

    ## predicting by-vignette free production taciturn response proportions as a function of prior elicitation differences between competitor and most salient alternative:

    ## 
    ## Call:
    ## lm(formula = taciturn_props ~ competitor_vs_maxAlternative_alpha)
    ## 
    ## Residuals:
    ##       Min        1Q    Median        3Q       Max 
    ## -0.220578 -0.072501 -0.009519  0.064940  0.229599 
    ## 
    ## Coefficients:
    ##                                     Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                         0.270578   0.022416  12.071 7.65e-14 ***
    ## competitor_vs_maxAlternative_alpha -0.011261   0.003839  -2.933  0.00597 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1185 on 34 degrees of freedom
    ## Multiple R-squared:  0.2019, Adjusted R-squared:  0.1785 
    ## F-statistic: 8.603 on 1 and 34 DF,  p-value: 0.00597

    ## 
    ## 
    ## predicting by-vignette free production taciturn response proportions as a function of prior elicitation differences between competitor and same category alternatives:

    ## 
    ## Call:
    ## lm(formula = taciturn_props ~ competitor_vs_sameCategory_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.21633 -0.07681 -0.01194  0.06868  0.32064 
    ## 
    ## Coefficients:
    ##                                   Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                       0.347301   0.025740  13.492 3.28e-15 ***
    ## competitor_vs_sameCategory_alpha -0.003784   0.001352  -2.798   0.0084 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1196 on 34 degrees of freedom
    ## Multiple R-squared:  0.1872, Adjusted R-squared:  0.1633 
    ## F-statistic: 7.831 on 1 and 34 DF,  p-value: 0.008398

    ## 
    ## 
    ## predicting by-vignette free production taciturn response proportions as a function of prior elicitation differences between competitor and other category alternatives:

    ## 
    ## Call:
    ## lm(formula = taciturn_props ~ competitor_vs_otherCategory_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.25824 -0.08139  0.02115  0.07234  0.20730 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                        0.461954   0.053540   8.628 4.42e-10 ***
    ## competitor_vs_otherCategory_alpha -0.004857   0.001513  -3.210  0.00289 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1162 on 34 degrees of freedom
    ## Multiple R-squared:  0.2326, Adjusted R-squared:  0.2101 
    ## F-statistic: 10.31 on 1 and 34 DF,  p-value: 0.002892

    ## 
    ## 
    ## predicting by-vignette free production taciturn response proportions as a function of prior elicitation changes in beliefs for competitor:

    ## 
    ## Call:
    ## lm(formula = taciturn_props ~ competitor_vs_beliefsChange_alpha)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.21439 -0.09174  0.01020  0.06075  0.29268 
    ## 
    ## Coefficients:
    ##                                    Estimate Std. Error t value Pr(>|t|)  
    ## (Intercept)                        0.129187   0.067944   1.901   0.0658 .
    ## competitor_vs_beliefsChange_alpha -0.004943   0.001860  -2.658   0.0119 *
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1207 on 34 degrees of freedom
    ## Multiple R-squared:  0.1721, Adjusted R-squared:  0.1477 
    ## F-statistic: 7.066 on 1 and 34 DF,  p-value: 0.01189

Combine all these results to see if the selected vignettes overlap.
Additionally, manually extracted (by Polina) weak items are added.

    ## # A tibble: 10 x 6
    ##    saliencyDistance sameCategoryDis… otherCategoryDi… changeBeliefsCo…
    ##    <chr>            <chr>            <chr>            <chr>           
    ##  1 friendsActiviti… clothing-winter  waterSport-motor books-fantasy   
    ##  2 bookingAgency-h… bar-tea          friendsActiviti… bookingAgency-l…
    ##  3 bar-tea          disney-princess  petAdoption-dogs plants-green    
    ##  4 petAdoption-dogs petAdoption-dogs movie-fantasy    electronics-con…
    ##  5 clothing-winter  electronics-con… furniture-indoo… movie-fantasy   
    ##  6 movie-fantasy    bookingAgency-h… cafe-pizza       furniture-indoo…
    ##  7 kidsActivities-… books-fantasy    plants-green     clothing-beach  
    ##  8 bookingAgency-l… bookingAgency-l… electronics-con… petAdoption-dogs
    ##  9 clothing-beach   clothing-beach   plants-flowers   friendsActiviti…
    ## 10 books-fantasy    gym-yoga         clothing-beach   bar-tea         
    ## # … with 2 more variables: wassersteinDistance <chr>, human_selection <chr>

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
    ## -0.62542 -0.32571  0.05164  0.29574  0.66949 
    ## 
    ## Coefficients:
    ##                                           Estimate Std. Error t value Pr(>|t|)
    ## (Intercept)                               0.825778   0.426107   1.938   0.0612
    ## sliderRating_competitor_mean_sd_sum$mean -0.005667   0.008467  -0.669   0.5080
    ## sliderRating_competitor_mean_sd_sum$sd    0.008495   0.014277   0.595   0.5559
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
    ## -0.76953 -0.21928  0.01536  0.26117  0.79756 
    ## 
    ## Coefficients:
    ##                                        Estimate Std. Error t value Pr(>|t|)  
    ## (Intercept)                            0.975936   0.391034   2.496   0.0177 *
    ## sliderRating_sameCat_mean_sd_sum$mean  0.010385   0.005515   1.883   0.0686 .
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
```
