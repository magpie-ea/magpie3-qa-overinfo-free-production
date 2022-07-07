library(tidyverse)
library(tidyboot)
library(aida)

##################################################

# these options help Stan run faster
options(mc.cores = parallel::detectCores())

# use the aida-theme for plotting
theme_set(theme_aida())

# global color scheme / non-optimized
project_colors = c("#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000")

# setting theme colors globally
scale_colour_discrete <- function(...) {
  scale_colour_manual(..., values = project_colors)
}
scale_fill_discrete <- function(...) {
  scale_fill_manual(..., values = project_colors)
} 

##################################################

answerOrder <- c('taciturn', 'competitor', 'same category', 'other category', 'exhaustive', 'unclassified')

# by item stats and plot
d_byItem <- read_delim('QA-overinfo-annotated.csv', delim = ";") %>% 
  rename(exhaustive = full) %>% 
  group_by(itemName) %>% 
  summarize(
    taciturn = sum(taciturn, na.rm = T),
    competitor = sum(competitor, na.rm = T),
    `same category` = sum(`same category`, na.rm = T),
    `other category` = sum(`other category`, na.rm = T),
    exhaustive = sum(exhaustive, na.rm = T),
    # unclassified = sum(other, na.rm = T)
  ) %>% 
  pivot_longer(cols = -itemName, names_to = 'answerType', values_to = "count") %>% 
  group_by(itemName) %>% 
  mutate(
    proportion = count / sum(count),
    answerType = factor(answerType, levels = answerOrder)
  )
  
d_byItem %>% 
  ggplot(aes(x = answerType, fill = answerType, y = count)) +
  geom_col() +
  # geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), alpha = 0.3, width =0.2) +
  facet_grid( itemName ~ . ) +
  theme(legend.position = 'none') +
  xlab('answer type') +
  ylab('observed response types') +
  theme(strip.text.y = element_text(angle = 0))

# overal stats and plots

d_global <- d_byItem %>% ungroup() %>% 
  group_by(answerType) %>% 
  summarize(
    count = sum(count),
    proportion = mean(proportion)
    )

d_byItem %>% 
  ggplot(aes(x = answerType, fill = answerType, y = count)) +
  geom_col() +
  # geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), alpha = 0.3, width =0.2) ++
  theme(legend.position = 'none') +
  xlab('answer type') +
  ylab('observed response types')



