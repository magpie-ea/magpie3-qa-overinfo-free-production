QA free typing analysis
================
Polina Tsvilodub
2022-11-01

# Intro

Below, exploratory analysis of the free production QA experiment data
can be found.

The responses were manually classified by Polina into seven categories:

- The “taciturn” category includes “No, we don’t have XY” responses. It
  also subsumes the responses which include some kind of explanation
  (like “Moana isn’t here today, she is helping her islanders so can’t
  be with us.”).
- The “competitor” category includes responses offering the competitor
  instead of the target object. It includes responses where the
  alternative is the anticipated competitor.
- exploratory: The “competitor/other” category includes responses where
  either additional information was included next to offering the
  competitor or the named competitor differed from our
  preclassification.
- The “sameCategory” option includes responses offering several
  alternatives (2-3) from the same category or offering one option which
  I did not consider a direct competitor.
- The “otherCategory” option includes responses offering 1-2
  alternatives from the different category.
- The “fullList” option includes responses where all alternatives were
  presented.
- The “other” category includes other unclassifiable responses as well
  as responses trying to offer some kind of vague solution to the
  request on top of saying “No” (like “We sell a selection of different
  types of books, I am sure you will find something in the adventure
  section.”).

The standard analysis with one “competitor” category is compared to an
analysis making the distinction between the two competitor-containing
categories. Additionally, single responses were classified as incorrect
with the “yes” category (e.g., “Yes let’s go see it” for the zoo-xl
vignette).

## Summary and exclusions

    ## Subjects who failed attention checks:  108 107 149

    ## 
    ## Subject exclusion rate:  0.03

    ## Number of excluded inccorect ('yes') responses:  14

    ## 
    ## Number of analysed responses:  762

    ## # A tibble: 7 x 2
    ##   category             n
    ##   <chr>            <int>
    ## 1 competitor         234
    ## 2 competitor/other    41
    ## 3 fullList            13
    ## 4 other              118
    ## 5 otherCategory        2
    ## 6 sameCategory       123
    ## 7 taciturn           231

    ## # A tibble: 36 x 2
    ##    itemName                                 n
    ##    <chr>                                <int>
    ##  1 bar-tea                                 17
    ##  2 bar-whiteWine                           21
    ##  3 bookingAgency-highClassAccommodation    18
    ##  4 bookingAgency-lowClassAccommodation     19
    ##  5 books-fantasy                           21
    ##  6 books-romance                           23
    ##  7 cafe-pie                                20
    ##  8 cafe-pizza                              15
    ##  9 clothing-beach                          22
    ## 10 clothing-winter                         22
    ## # … with 26 more rows

    ## 
    ## average number of responses per vignette: 21.16667

    ## 
    ## vignette with most responses:  gym-yoga 27

    ## 
    ## vignette with least responses:  cafe-pizza 15

## Plots

The first plot displays proportions of different response types
(standard analysis) by-vignette.

![](01_main_free_typing_analysis_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

The second plot explores whether there is a qualitative difference when
adding the exploratory “competitor/other” category – this does not seem
to be the case.

![](01_main_free_typing_analysis_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

The plot below shows response proportions by response category averaged
across vignettes. Again, including one competitor category vs two
exploratory categories is compared.

    ## `summarise()` ungrouping output (override with `.groups` argument)`summarise()`
    ## ungrouping output (override with `.groups` argument)

![](01_main_free_typing_analysis_files/figure-gfm/unnamed-chunk-9-1.png)<!-- -->![](01_main_free_typing_analysis_files/figure-gfm/unnamed-chunk-9-2.png)<!-- -->

## Exploring weak vignettes and weird participant behavior

    ## Vignettes receiving the most 'other' responses (mostly 'no but we have other options which might interest you')

    ## # A tibble: 6 x 3
    ##   itemName           answerType responseCategory_proportion
    ##   <chr>              <fct>                            <dbl>
    ## 1 plants-green       other                            0.529
    ## 2 furniture-indoors  other                            0.368
    ## 3 movie-western      other                            0.368
    ## 4 disney-princess    other                            0.364
    ## 5 furniture-outdoors other                            0.286
    ## 6 zoo-xl             other                            0.261

    ## 
    ## Vignettes with highest proportion of competitor responses where either additional information was included or the named competitor differed from our preclassification

    ## # A tibble: 6 x 3
    ##   itemName                           answerType       responseCategory_proporti…
    ##   <chr>                              <fct>                                 <dbl>
    ## 1 kidsActivities-sports              competitor/other                      0.261
    ## 2 touristInfo-clubbing               competitor/other                      0.192
    ## 3 books-romance                      competitor/other                      0.174
    ## 4 furniture-indoors                  competitor/other                      0.158
    ## 5 bookingAgency-lowClassAccommodati… competitor/other                      0.158
    ## 6 plants-flowers                     competitor/other                      0.12

    ## 
    ## Vignettes receiving the most 'taciturn' responses

    ## # A tibble: 6 x 3
    ##   itemName                     answerType responseCategory_proportion
    ##   <chr>                        <fct>                            <dbl>
    ## 1 movie-fantasy                taciturn                         0.625
    ## 2 petAdoption-dogs             taciturn                         0.55 
    ## 3 disney-princess              taciturn                         0.5  
    ## 4 movie-western                taciturn                         0.474
    ## 5 electronics-console          taciturn                         0.458
    ## 6 friendsActivities-boardGames taciturn                         0.438

    ## Number of participants providing taciturn responses only:  7

    ## 
    ## Number of participants providing competitor responses only:  0

    ## 
    ## Number of participants providing 'other' responses only:  0

    ## 
    ## Maximal number of distinct response types provided by a participant:  6

    ## 
    ## Number of participants providing maximal number of distinct response types:  1

    ## 
    ## Average number of response types provided by a participant:  3.521173

Visualize global distribution if participants producing “No” responses
only would be excluded.

    ## `summarise()` ungrouping output (override with `.groups` argument)

![](01_main_free_typing_analysis_files/figure-gfm/unnamed-chunk-12-1.png)<!-- -->

## Follow-up analyses

Below, analyses suggested during the meeting on Nov 10th are
incorporated. First, the length (in terms of characters) of the
anticipated competitor as well as averaged together with the same
category alternatives is extracred. We check whether participants tended
to produce more taciturn responses when the alternatives were longer.

    ## Parsed with column specification:
    ## cols(
    ##   itemName = col_character(),
    ##   settingName = col_character(),
    ##   vignette_start = col_character(),
    ##   vignette_continuation = col_character(),
    ##   question = col_character(),
    ##   taciturn = col_character(),
    ##   answer_template = col_character(),
    ##   itemQuestion = col_character(),
    ##   competitor = col_character(),
    ##   sameCategory1 = col_character(),
    ##   sameCategory2 = col_character(),
    ##   otherCategory1 = col_character(),
    ##   otherCategory2 = col_character(),
    ##   correct_response = col_character()
    ## )

    ## 
    ## Call:
    ## lm(formula = responseCategory_proportion ~ comp_length, data = d_clean_main_collapsedCompetitor_summary_wVignette %>% 
    ##     filter(answerType == "taciturn"))
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.25318 -0.09477  0.00025  0.08843  0.32545 
    ## 
    ## Coefficients:
    ##              Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  0.318915   0.052078   6.124 5.95e-07 ***
    ## comp_length -0.001210   0.003317  -0.365    0.717    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1324 on 34 degrees of freedom
    ## Multiple R-squared:  0.003901,   Adjusted R-squared:  -0.0254 
    ## F-statistic: 0.1331 on 1 and 34 DF,  p-value: 0.7175

    ## 
    ## Call:
    ## lm(formula = responseCategory_proportion ~ sameCat_avg_length, 
    ##     data = d_clean_main_collapsedCompetitor_summary_wVignette %>% 
    ##         filter(answerType == "taciturn"))
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.25090 -0.09921  0.00281  0.08743  0.32044 
    ## 
    ## Coefficients:
    ##                     Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)         0.321815   0.059284   5.428 4.77e-06 ***
    ## sameCat_avg_length -0.001568   0.004291  -0.366    0.717    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1324 on 34 degrees of freedom
    ## Multiple R-squared:  0.003914,   Adjusted R-squared:  -0.02538 
    ## F-statistic: 0.1336 on 1 and 34 DF,  p-value: 0.717

Further, order effects of the trials are investigated. We check if
participants become lazy over the trials and are therefore more likely
to produce taciturn responses towards the end of the experiment. This
seems not to be the case. If anything, participants tended to produce
slightly more taciturn responses in the beginning of the experiment.

``` r
# collapse across items and participants, look at trial number
df_trialNum <- df_clean_main %>% 
  mutate(answerType = ifelse(category == "competitor/other", "competitor", category),
         answerType = factor(answerType, levels = c('competitor', 'sameCategory', 'otherCategory', 'fullList', 'other', 'taciturn'))) %>%
  group_by(submission_id) %>%
  mutate(trialNr_main = (1:n())) %>%
  ungroup() %>%
  group_by(answerType, trialNr_main) %>% 
  summarise(answerType_count = n(), 
            answerType_proportion = answerType_count / nrow(df_clean_main)
            ) 
```

    ## `summarise()` regrouping output by 'answerType' (override with `.groups`
    ## argument)

``` r
df_trialNum %>%
  ggplot(aes(x = trialNr_main, fill = answerType, y = answerType_proportion)) +
  geom_col() +
  facet_wrap(answerType ~ ., ncol = 2) + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  ylab("Global proportion of answer type") +
  xlab("Trial number")
```

![](01_main_free_typing_analysis_files/figure-gfm/unnamed-chunk-14-1.png)<!-- -->

``` r
lm_orderEffect <- lm(answerType_proportion ~ trialNr_main, data = df_trialNum %>% filter(answerType == "taciturn"))
summary(lm_orderEffect)
```

    ## 
    ## Call:
    ## lm(formula = answerType_proportion ~ trialNr_main, data = df_trialNum %>% 
    ##     filter(answerType == "taciturn"))
    ## 
    ## Residuals:
    ##        Min         1Q     Median         3Q        Max 
    ## -0.0074991 -0.0030738 -0.0003437  0.0028512  0.0085458 
    ## 
    ## Coefficients:
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)   0.045135   0.004252  10.616 4.12e-05 ***
    ## trialNr_main -0.001609   0.000842  -1.911    0.105    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.005456 on 6 degrees of freedom
    ## Multiple R-squared:  0.3784, Adjusted R-squared:  0.2748 
    ## F-statistic: 3.653 on 1 and 6 DF,  p-value: 0.1045
