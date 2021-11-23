library(wordcloud)
library(udpipe)
library(lattice)

library(tidyverse)
library(tidytext)

#Stemming packages
library(SnowballC)
#library(hunspell)
#library(proustr)

library(tm)

#################################################
#==============Sentiment Analysis===============#
# Conduct various assessments to understand the #
# sentiment of tweets related to the airline    #
# industry                                      #
#################################################

tempable ="https://github.com/RobertSCookOSU/MSIS5193_BGJRGroup_Project/blob/main/Final%20Data/final_dataset_comparison_description.csv"
desc_data = read.csv(temptable, header = TRUE)
print(desc_data)



sentiment_desc = select(desc_data, Description, Zip)

tidy_dataset = unnest_tokens(sentiment_desc , word, Description)

counts = count(tidy_dataset, word)

result1 = arrange(counts, desc(n))
print(result1)

# Remove stop words from the data by
# using the dataset stop_words found
# in the tidytext package
#=====================================
data("stop_words")

tidy_dataset2 = anti_join(tidy_dataset, stop_words)

counts2 = count(tidy_dataset2, word)

arrange(counts2, desc(n))
#==============================================
# Remove the numerical values from the column 
# word. tidytext automatically makes all 
# words lower case, no conversion necessary.
#==============================================
patterndigits = '\\b[0-9]+\\b'

# Use regex
tidy_dataset2$word = str_remove_all(tidy_dataset2$word, patterndigits)

counts3 = count(tidy_dataset2, word)

arrange(counts3, desc(n)) %>%
  ungroup %>%
  slice(1:15)
#=======================================
# Replace all new lines, tabs, and
# blank spaces with a value of nothing
# and then filter out those values
#=======================================

tidy_dataset2$word = str_replace_all(tidy_dataset2$word, '[:space:]', '')

tidy_dataset3 = filter(tidy_dataset2,!(word == ''))

counts4 = count(tidy_dataset3, word)

arrange(counts4, desc(n)) %>%
  ungroup %>%
  slice(1:15)
#=======================
# Remove some names
#=======================
list_filter = c("Oklahoma","city","home",
                "auction",".com")

tidy_dataset3 = filter(tidy_dataset3, !(word %in% list_filter))
#==============================
# Plot the the words with a
# proportion greater than 0.5
#==============================
frequency = tidy_dataset3 %>%
  count(word) %>%
  arrange(desc(n)) %>%
  mutate(proportion = (n / sum(n)*100)) %>%
  filter(proportion >= 0.5)

library(scales)

ggplot(frequency, aes(x = proportion, y = word)) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
 labs(y = 'Word', x = 'Proportion')
#=======================================
# Using the SnowballC package, run the
# function wordStem() on the data to
# apply stemming to the data
#=======================================
tidy_dataset4 = mutate_at(tidy_dataset3, "word", funs(wordStem((.), language="en")))

counts5 = count(tidy_dataset4, word)

arrange(counts5, desc(n)) %>%
  ungroup %>%
  slice(1:15)
#===============================================


positive = tidy_dataset4 %>% 


counts5 = count(positive, word, sort = TRUE)
counts5 = rename(counts5, freq = n)
positive2 = top_n(counts5, 21)

colourCount = length(unique(positive2$word))
getPalette = colorRampPalette(brewer.pal(9, "Set1"))

positive2 %>%
  mutate(word = reorder(word, freq)) %>%
  ggplot(aes(x = word, y = freq)) +
  geom_col(fill = getPalette(colourCount)) +
  coord_flip()
#################################################
# Positive negative sentiments
##################################################

nrc_posneg = get_sentiments('nrc') %>%
  filter(sentiment == 'positive' | 
           sentiment == 'negative')
nrow(nrc_posneg)
newjoin = inner_join(tidy_dataset4, nrc_posneg)
counts7 = count(newjoin,word, sentiment)
spread1 = spread(counts7, sentiment, n, fill = 0)
content_data_posneg=mutate(spread1, diffsent = positive - negative,linenumber = row_number())
desc_posneg = arrange(content_data_posneg, desc(diffsent))
print(desc_posneg)

desc_posneg2 = desc_posneg %>%
  slice(1:10,253:262)

ggplot(desc_posneg2, aes(x=linenumber, y=diffsent, fill=word)) +
  coord_flip() +
  theme_light(base_size = 15) +
  labs(
    x='Index Value',
    y='diffsent'
  ) +
  theme(
    legend.position = 'bottom',
    panel.grid = element_blank(),
    axis.title = element_text(size = 10),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10)
  ) +
  geom_col()

###########################################################
# Trust and Fear
##########################################################
nrc_trustfear = get_sentiments('nrc') %>%
  filter(sentiment == 'trust' | 
           sentiment == 'fear')
nrow(nrc_trustfear)
newjoin3 = inner_join(tidy_dataset4, nrc_trustfear)
counts9 = count(newjoin3,word, sentiment)
spread1 = spread(counts9, sentiment, n, fill = 0)
content_data_trufe=mutate(spread1, trustworthy = trust - fear,linenumber = row_number())
desc_trustfear = arrange(content_data_trufe, desc(trustworthy))
print(desc_trustfear)

desc_trustfear2 = desc_trustfear %>%
  slice(1:10,253:262)

ggplot(desc_trustfear2, aes(x=linenumber, y=trustworthy, fill=word)) +
  coord_flip() +
  theme_light(base_size = 15) +
  labs(
    x='Index Value',
    y='trustworthy'
  ) +
  theme(
    legend.position = 'bottom',
    panel.grid = element_blank(),
    axis.title = element_text(size = 10),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10)
  ) +
  geom_col()



##########################################################
#Joy and disgust
##########################################################

nrc_joydis = get_sentiments('nrc') %>%
  filter(sentiment == 'joy' | 
           sentiment == 'disgust')
nrow(nrc_joydis)
newjoin = inner_join(tidy_dataset4, nrc_joydis)
counts7 = count(newjoin,word, sentiment)
spread1 = spread(counts7, sentiment, n, fill = 0)
content_data_joydis=mutate(spread1, diffjoydis = joy - disgust,linenumber = row_number())
desc_joydis = arrange(content_data_joydis, desc(diffjoydis))
print(desc_joydis)

desc_joydis2 = desc_joydis %>%
  slice(1:10,253:262)

ggplot(desc_joydis2, aes(x=linenumber, y=diffjoydis, fill=word)) +
  coord_flip() +
  theme_light(base_size = 15) +
  labs(
    x='Index Value',
    y='diffjoydis'
  ) +
  theme(
    legend.position = 'bottom',
    panel.grid = element_blank(),
    axis.title = element_text(size = 10),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10)
  ) +
  geom_col()


