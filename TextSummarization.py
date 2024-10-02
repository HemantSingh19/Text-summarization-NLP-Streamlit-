import streamlit as st
import logging
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
stopwords = list(STOP_WORDS)
nlp = spacy.load("en_core_web_sm")
from heapq import nlargest
import time

st.title("NLP-Powered Summarization:")
st.header("_Crafting Concise Outputs from Lengthy Inputs_ :sunglasses:")

input_column , output_column = st.columns(2)

with input_column:
    text = st.text_area("Text to summarize", height=200,placeholder='Please type here....')

def Text_Summarization(text):
    from string import punctuation
    doc = nlp(text) 
    tokens = [token.text for token in doc]
    punctuation = punctuation+'\n'
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies:
                    word_frequencies[word.text.lower()] = 1
                else:
                    word_frequencies[word.text.lower()] += 1              
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]       
    sentence_token = [sent for sent in doc.sents]
    word_frequencies.keys()
    sentence_score= {}
    for sent in sentence_token: 
        sentence_score[sent.text]=0      
        for token in sent:
            word_lower = token.text.lower()
            if word_lower in word_frequencies: 
                sentence_score[sent.text] += word_frequencies[word_lower]        
    select_lenght = int(len(sentence_token)*0.3)
    summary_sentence = nlargest(select_lenght, sentence_score, key = sentence_score.get)
    final_summary = ' '.join(summary_sentence)                 
    return final_summary

def summary_stream(summary):
    for word in summary.split(" "):
        yield word + " "
        time.sleep(0.02)
        
with output_column:
    if st.button('Generate Summary'):
        if text:    
            summary = Text_Summarization(text)
            st.write_stream(summary_stream(summary))
        else:
            st.write("Please enter text to see the summary.")    

    