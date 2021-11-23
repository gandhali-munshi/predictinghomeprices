#==================================================
# Most available data and information come in the
# form of unstructured text. You can analyze this
# text to gain insights into a phenomenon of
# interest 
#==================================================

#install.packages('tidytext')
#install.packages('SnowballC')
#install.packages('tm')
#install.packages('textdata')

library(wordcloud)
library(udpipe)
library(lattice)

library(dplyr)
library(tidyverse)
library(tidytext)

#Stemming packages
library(SnowballC)
#library(hunspell)
#library(proustr)
library(tm)

#####################################################
#============Setup the Working Directory============#
# Set the working directory to the project folder by#
# running the appropriate code below.               #
#####################################################

wd = "~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Final Data"

setwd(wd)
temptable = paste(wd, "/final_dataset_description.csv", sep = "")
tweets_data = read.csv(temptable, header = TRUE)

summary(tweets_data)

#===============================
tweets_data<-data.frame(lapply(tweets_data, as.character),stringsAsFactors = FALSE)
glimpse(tweets_data)

phone_tweets = tweets_data %>% 
  select(Description)

tidy_dataset = phone_tweets %>%
  unnest_tokens(word, Description)

# Count the most popular words
tidy_dataset %>%
  count(word) %>%
  arrange(desc(n))


# Remove Stop words
data("stop_words")

tidy_dataset2 = tidy_dataset %>%
  anti_join(stop_words)

tidy_dataset2 %>%
  count(word) %>%
  arrange(desc(n))

#==============================================
# Remove the numerical values from the column
#==============================================
patterndigits = '\\b[0-9]+\\b'


# Alternative
tidy_dataset2$word = tidy_dataset2$word %>%
  str_replace_all(patterndigits, '')

tidy_dataset2 %>%
  count(word) %>%
  arrange(desc(n))


#=======================================
# Replace all new lines, tabs, and
# blank spaces with a value of nothing
# and then filter out those values
#=======================================

# Alternative
tidy_dataset2$word = tidy_dataset2$word %>%
  str_replace_all('[:space:]', '')

tidy_dataset3 = tidy_dataset2 %>% 
  filter(!(word == ''))

tidy_dataset3 %>%
  count(word) %>%
  arrange(desc(n))

#====================================
# Remove TMobine and Sprint from list
#====================================
list_remove = c("oklahoma","city",",","auction.com",".","zip","code","approximately")

tidy_dataset3 = tidy_dataset3 %>%
  filter(!(word %in% list_remove))

head(tidy_dataset3,25)
#=======================================
# Using the SnowballC package, run the
# function wordStem() on the data to
# apply stemming to the data
#=======================================

# StemData
tidy_dataset4 = tidy_dataset3 %>%
  mutate_at("word", funs(wordStem((.), language="en")))

tidy_dataset4 %>%
  count(word) %>%
  arrange(desc(n))

#use nrc Package
allnrcs=get_sentiments("nrc")

#Just filter to Joy and Sadness
nrc_joysad = get_sentiments('nrc') %>%
  filter(sentiment == 'joy' | 
           sentiment == 'sadness')
nrow(nrc_joysad)

#Join joy/sadness subset to tweets
newjoin2 = inner_join(tidy_dataset4, nrc_joysad)

#Words tweeted with joy meaning
joy = newjoin2 %>% 
  filter(sentiment == "joy")

#Words tweeted with sad meaning
sadness = newjoin2 %>% 
  filter(sentiment == "sadness")

#sum the trust words and create top 10
counts5 = count(joy, word, sort = TRUE)
counts5 = rename(counts5, freq = n)
top10_joy = top_n(counts5, 10)

#sum the fear words and create top 10
counts6 = count(sadness, word, sort = TRUE)
counts6 = rename(counts6, freq = n)
top10_sadness = top_n(counts6, 10)

#difference b/t joy and sadness
joy_sadness_diff=tidy_dataset4 %>%
  inner_join(get_sentiments('nrc')) %>% 
  count(sentiment) %>% 
  spread(sentiment, n, fill = 0) %>% 
  mutate(diffsent = joy - sadness) %>%
  select('joy','sadness','diffsent')

#Plot Trust
colourCount = length(unique(top10_joy$word))
getPalette = colorRampPalette(brewer.pal(9, "Set1"))

top10_joy %>%
  mutate(word = reorder(word, freq)) %>%
  ggplot(aes(x = word, y = freq)) +
  geom_col(fill = getPalette(colourCount)) +
  ggtitle("top 10 Joy Words") +
  coord_flip()

#Plot Fear
colourCount = length(unique(top10_sadness$word))
getPalette = colorRampPalette(brewer.pal(9, "Set1"))

top10_sadness %>%
  mutate(word = reorder(word, freq)) %>%
  ggplot(aes(x = word, y = freq)) +
  geom_col(fill = getPalette(colourCount)) +
  ggtitle("Top 10 Sadness Words") +
  coord_flip()

#Just filter to negative and positive
nrc_negpos = get_sentiments('nrc') %>%
  filter(sentiment == 'positive' | 
           sentiment == 'negative')
nrow(nrc_negpos)

#Join positive/negative subset to tweets
newjoin3 = inner_join(tidy_dataset4, nrc_negpos)

#Words tweeted with positive meaning
positive = newjoin3 %>% 
  filter(sentiment == "positive")

#Words tweeted with negative meaning
negative = newjoin3 %>% 
  filter(sentiment == "negative")

#sum the positive words and create top 10
counts7 = count(positive, word, sort = TRUE)
counts7 = rename(counts7, freq = n)
top10_positive = top_n(counts7, 10)

#sum the negative words and create top 10
counts8 = count(negative, word, sort = TRUE)
counts8 = rename(counts8, freq = n)
top10_negative = top_n(counts8, 10)

#difference b/t positive and negative
pos_neg_diff=tidy_dataset4 %>%
  inner_join(get_sentiments('nrc')) %>% 
  count(sentiment) %>% 
  spread(sentiment, n, fill = 0) %>% 
  mutate(diffsent = positive - negative) %>%
  select('positive','negative','diffsent')


#Plot Positive
colourCount = length(unique(top10_positive$word))
getPalette = colorRampPalette(brewer.pal(9, "Set1"))

top10_positive %>%
  mutate(word = reorder(word, freq)) %>%
  ggplot(aes(x = word, y = freq)) +
  geom_col(fill = getPalette(colourCount)) +
  ggtitle("Top 10 Positive Words") +
  coord_flip()

#Plot Negative
colourCount = length(unique(top10_negative$word))
getPalette = colorRampPalette(brewer.pal(9, "Set1"))

top10_negative %>%
  mutate(word = reorder(word, freq)) %>%
  ggplot(aes(x = word, y = freq)) +
  geom_col(fill = getPalette(colourCount)) +
  ggtitle("Top 10 Negative Words") +
  coord_flip()







#Just filter to fear and trust
nrc_trusfear = get_sentiments('nrc') %>%
  filter(sentiment == 'trust' | 
           sentiment == 'fear')
nrow(nrc_trusfear)

#Join trust/fear subset to tweets
newjoin4 = inner_join(tidy_dataset4, nrc_trusfear)

#Words tweeted with trust meaning
trust = newjoin4 %>% 
  filter(sentiment == "trust")

#Words tweeted with fear meaning
fear = newjoin4 %>% 
  filter(sentiment == "fear")

#sum the trust words and create top 10
counts1 = count(trust, word, sort = TRUE)
counts1 = rename(counts1, freq = n)
top10_trust = top_n(counts1, 10)

#sum the fear words and create top 10
counts2 = count(fear, word, sort = TRUE)
counts2 = rename(counts2, freq = n)
top10_fear = top_n(counts2, 10)

#difference b/t trust and fear
trus_fear_diff=tidy_dataset4 %>%
  inner_join(get_sentiments('nrc')) %>% 
  count(sentiment) %>% 
  spread(sentiment, n, fill = 0) %>% 
  mutate(diffsent = trust - fear) %>%
  select('trust','fear','diffsent')


#Plot Trust
colourCount = length(unique(top10_trust$word))
getPalette = colorRampPalette(brewer.pal(9, "Set1"))

top10_trust %>%
  mutate(word = reorder(word, freq)) %>%
  ggplot(aes(x = word, y = freq)) +
  geom_col(fill = getPalette(colourCount)) +
  ggtitle("Top 10 Trust Words") +
  coord_flip()

#Plot Fear
colourCount = length(unique(top10_fear$word))
getPalette = colorRampPalette(brewer.pal(9, "Set1"))

top10_fear %>%
  mutate(word = reorder(word, freq)) %>%
  ggplot(aes(x = word, y = freq)) +
  geom_col(fill = getPalette(colourCount)) +
  ggtitle("Top 10 Fear Words") +
  coord_flip()


ud_model = udpipe_download_model(language = "english")

#NOUNS
tidy_post1=tidy_dataset4 %>%
  select(word)

ud_model = udpipe_load_model(ud_model$file_model)

tagging_data = as.data.frame(udpipe_annotate(ud_model, x = tidy_post1$word))

post_stats = txt_freq(tagging_data$upos)

#SEE BREAKOUT OF NOUNS/ADJECTIVES/VERBS
new_list=post_stats%>%
  filter(key %in% c("NOUN", "ADJ", "VERB"))

noun_stats = subset(tagging_data, upos %in% c("NOUN"))

noun_stats2 = txt_freq(noun_stats$token)
noun_stats2$key = factor(noun_stats2$key, levels = rev(noun_stats2$key))

noun_stats2 %>%
  slice(1:20) %>%
  ggplot(aes(x=key, y=as.factor(freq), fill=freq)) +
  coord_flip() +
  theme_light(base_size = 15) +
  labs(
    x='Frequency',
    y='',
    title='Noun Occurrences'
  ) +
  theme(
    legend.position = 'none',
    panel.grid = element_blank(),
    axis.title = element_text(size = 10),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10),
    title = element_text(size = 13)
  ) +
  scale_fill_gradient(low="orange", high="orange3") +
  geom_col()

#ADJECTIVES
adjstats = subset(tagging_data, upos %in% c("ADJ"))

adjstats2 = txt_freq(adjstats$token)

adjstats2$key = factor(adjstats2$key, levels = rev(adjstats2$key))

adjstats2 %>%
  slice(1:20) %>%
  ggplot(aes(x=key, y=as.factor(freq), fill=freq)) +
  coord_flip() +
  theme_light(base_size = 15) +
  labs(
    x='Frequency',
    y='',
    title='Adjective Occurrences'
  ) +
  theme(
    legend.position = 'none',
    panel.grid = element_blank(),
    axis.title = element_text(size = 10),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10),
    title = element_text(size = 13)
  ) +
  scale_fill_gradient(low="chartreuse", high="chartreuse3") +
  geom_col()

#VERBS
verbstats = subset(tagging_data, upos %in% c("VERB"))

verbstats2 = txt_freq(verbstats$token)

verbstats2$key = factor(verbstats2$key, levels = rev(verbstats2$key))

verbstats2 %>%
  slice(1:20) %>%
  ggplot(aes(x=key, y=as.factor(freq), fill=freq)) +
  coord_flip() +
  theme_light(base_size = 15) +
  labs(
    x='Frequency',
    y='',
    title='Verb Occurrences'
  ) +
  theme(
    legend.position = 'none',
    panel.grid = element_blank(),
    axis.title = element_text(size = 10),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10),
    title = element_text(size = 13)
  ) +
  scale_fill_gradient(low="tan", high="tan3") +
  geom_col()

#write out trust/fear data sets
write.csv(write.csv(trust,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/trust_sentiment.csv", row.names = FALSE)
)
write.csv(write.csv(top10_trust,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/top_10_trust.csv", row.names = FALSE)
)

write.csv(write.csv(fear,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/fear_sentiment.csv", row.names = FALSE)
)

write.csv(write.csv(top10_fear,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/top_10_fear.csv", row.names = FALSE)
)


#write out positive/negative sentiments
write.csv(write.csv(positive,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/positive_sentiment.csv", row.names = FALSE)
)
write.csv(write.csv(top10_positive,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/top_10_positive.csv", row.names = FALSE)
)
write.csv(write.csv(negative,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/negative_sentiment.csv", row.names = FALSE)
)
write.csv(write.csv(top10_negative,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/top_10_negative.csv", row.names = FALSE)
)

#write out joy sentiment
write.csv(write.csv(joy,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/joy_sentiment.csv", row.names = FALSE)
)
write.csv(write.csv(top10_joy,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/top_10_joy.csv", row.names = FALSE)
)

#Write out adjectives
write.csv(write.csv(adjstats2,"~/github-classroom/msis5193-pds1-2021fall-online/MSIS5193_BGJRGroup_Project/Raw Data/adjectives.csv", row.names = FALSE)
)
