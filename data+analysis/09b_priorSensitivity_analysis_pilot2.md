PragmaticQA E4: Prior Sensitivity Free Production: Pilot 2
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

- Pilot 1: five vignettes only were chosen here: cardBlanche,
  icecreamFlavors, streamingOptions, coffeeShops, socialMedia. N=30 were
  recruited.
- **Pilot 2** (analysed here): we use ten vignettes after the logical
  structure was adjusted. All items were used. N=30 were recruited.

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
  unnest(category)
  
d_main_clean
```

    ## # A tibble: 112 × 14
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
    ## # … with 102 more rows, 4 more variables: languages <chr>, responseTime <dbl>,
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

Below the single category proportions are displayed by condition.

``` r
df_answerOptions_global_summary <- d_main_clean %>% 
  group_by(category) %>% 
  summarise(answerType_count = n(), 
            answerType_proportion = answerType_count / nrow(d)
            )

df_answerOptions_byCondition_summary <- d_main_clean %>% 
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

![](09b_priorSensitivity_analysis_pilot2_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

Below, the response categories are plotted by-item, so as to check if
respondents might have chosen different strategies, e.g., full-list
responses, in e.g. commercial contexts so as to not loose customers:

``` r
df_answerOptions_byCondition_byItem_summary <- d_main_clean %>% 
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

![](09b_priorSensitivity_analysis_pilot2_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

We can also looks at the bootstrapped CIs over the rate of exceptive
answers; while the difference is larger, the CIs overlap.

``` r
d_main_binary_summary <- d_main_clean %>% 
  mutate(is_exceptive = ifelse(category == "exceptive", 1, 0)) %>%
  group_by(condition) %>% 
  tidyboot_mean(column = is_exceptive)
```

    ## Warning: `as_data_frame()` was deprecated in tibble 2.0.0.
    ## ℹ Please use `as_tibble()` instead.
    ## ℹ The signature and semantics have changed, see `?as_tibble`.
    ## ℹ The deprecated feature was likely used in the purrr package.
    ##   Please report the issue at <]8;;https://github.com/tidyverse/purrr/issueshttps://github.com/tidyverse/purrr/issues]8;;>.

    ## Warning: `cols` is now required when using unnest().
    ## Please use `cols = c(strap)`

``` r
d_main_binary_summary
```

    ## # A tibble: 2 × 6
    ##   condition      n empirical_stat ci_lower   mean ci_upper
    ##   <chr>      <int>          <dbl>    <dbl>  <dbl>    <dbl>
    ## 1 high_prior    55         0.0545    0     0.0541    0.12 
    ## 2 low_prior     57         0.246     0.145 0.247     0.357
