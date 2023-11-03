import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def main():
    st.title("Word Cloud Example")

    # Sample text data
    text = "This is a word cloud example for Streamlit. Streamlit is a great tool for building web apps."

    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    # Display the word cloud using Matplotlib
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot()

if __name__ == "__main__":
    main()
