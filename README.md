# NLP in Finance 

## Project 1: NLP on Financial Statements

In this project, I have done NLP anlaysis on **10-k financial statements** to generate an alpha factor. 

### Step 1:  Get list of `10-Ks`

1. Use  `request` moduel to extract `10-k` reports from `SEC` API. Download  10-Ks html files for a few companies based on their `CIK`.

<img src="https://github.com/bondxue/NLP-for-Finance/blob/master/Sentiment_Analysis_for_Financial_Statements/images/sec_api.png" width="600"> 

+ One tricky thing is that `SEC` has a limit on the number of calls we can make to the website per second. In order to avoid hiting that limit, I have created the `SecAPI` class to cache data from the `SEC`.  

  <img src="https://github.com/bondxue/NLP-for-Finance/blob/master/Sentiment_Analysis_for_Financial_Statements/images/html.png" width="600">

2. Use `re` for tags  (`<DOCUMENT>`, `</DOCUMENT>`, `<Type>`) to extract sections contain 10-information and create dictionary for 10-Ks. 

### Step 2:  Preprocess the data

1. The text for document are very messy,  we need to **clean up** by removing the html and lowering case all the text using `BeautifulSoup`. 
2. With text cleaned up, we need to **lemmatize** verbs in the list of words.
3. remove the **stopwords** 

### Step 3: Analysis on 10-Ks

#### Loughran McDonald Sentiment Word Lists

use the **Loughran and McDonald sentiment word lists** .  The word lists cover the following sentiment:`Negative`, `Positive`, `Uncertainty`, `Litigious`, `Constraining`, `Superfluous`, `Interesting`, `Modal`. We choose a few of them to do sentiment analysis on the 10-Ks.

<img src="https://github.com/bondxue/NLP-for-Finance/blob/master/Sentiment_Analysis_for_Financial_Statements/images/dict.png" width="600">

#### Bag of Words

Using the sentiment word lists, we generate sentiment **bag of words** from 10-K documents. (ignore words are not in `sentiment_words`)

Use **bag of words**, calculate the **jaccard similarity** on the bag of words and plot it over time. 

+ Since the input, `bag_of_words_matrix`, is a bag of words for each time period in order, we just need to compute the jaccard similarities for each *neighboring* bag of words. 

<img src="https://github.com/bondxue/NLP-for-Finance/blob/master/Sentiment_Analysis_for_Financial_Statements/images/bow.png" width="600">


#### TFIDF

use the sentiment word list, try to use alternative sentiment **TFIDF** model from 10-K documents. 

Then calculate the **cosine similarity** for each *neighboring* bag of words. 

<img src="https://github.com/bondxue/NLP-for-Finance/blob/master/Sentiment_Analysis_for_Financial_Statements/images/tfidf.png" width="600">



### Step 4: Evaluate Alpha Factors

We want to evaluate the alpha factors only considering cosine similarities here. We use the yearly pricing from Quotemedia to run the factor agaist, since 10-Ks are produced annually. 



## PART 2: Sentiment Analysis with Neural Networks 

When deciding the value of a company, it's important to follow the news. For example, a product recall or natural disaster in a company's product chain. We want to be able to turn this information into a signal.

For this project, I will use posts from the social media site [StockTwits](https://en.wikipedia.org/wiki/StockTwits). The community on StockTwits is full of investors, traders, and entrepreneurs. Each message posted is called a *Twit*. This is similar to Twitter's version of a post, called a Tweet. I will build a model around these twits that generate a sentiment score.

After collecting a bunch of twits, then hand labeled the sentiment of each. To capture the degree of sentiment, we'll use a five-point scale: `very negative`, `negative`, `neutral`, `positive`, `very positive`. Each twit is labeled -2 to 2 in steps of 1, from very negative to very positive respectively. I will build a sentiment analysis model that will learn to assign sentiment to twits on its own, using this labeled data.




