'''An application that analyzes the sentiment of a

given text as positive, negative, or neutral using a
simple sentiment analysis library'''
from textblob import TextBlob

def sentiment_analysis():
    text = input("Enter a sentence: ")
    analysis = TextBlob(text)
    print("Sentiment:", "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral")

sentiment_analysis()