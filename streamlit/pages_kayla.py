import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import circlify
from collections import Counter
import nltk
from nltk.corpus import stopwords
# import streamlit as st


stopwords = nltk.corpus.stopwords.words('english')
stopwords += ['used', 'using', 'use', 'the', 'our', 'project']
stopwords += ['system', 'also', 'building', 'synthetic', 'sequence', 'biology', 'process', 'create', 'new', 'ability', 'igem', 'team', 'thus', 'make',
 'found', 'allow', 'due', 'within', 'problem', 'aim', 'work', 'provide', 'many', 'able', 'based', 'current', 'method', 'issue', 'toward', 'new',
 'different', 'life']

def get_df(name):
  web = 'https://raw.githubusercontent.com/'
  repo = 'kaylaque/project-discovery-dashboard/main/data/interim/'
  url = web + repo + name
  response = requests.get(url)
  with open(name, 'wb') as f:
      f.write(response.content)

  return(pd.read_csv(name,  lineterminator='\n'))

def yearly_plot(df, col, var):
  # Create a timeseries plot

  ax = sns.lineplot(x=df[~df[col].isna()][col].unique().tolist(), 
                        y=df[col].value_counts().tolist()[::-1]
                        )

  # Add an xlabel
  ax.set_xlabel(col)

  # Add a ylabel
  ax.set_ylabel('Count')
  ax.set_title(f'iGEM {var} Year by Year')
  # Show the plot
  plt.show()

def yearly_plot_multi(df, col, var, condition, cond_col, size):
  # Create a timeseries plot
  
  fig = plt.subplots(figsize=size)
  for cond in condition:
    ax = sns.lineplot(x=df[(df[cond_col] == cond) & (~df[cond_col].isna())][col].unique().tolist(), 
                          y=df[(df[cond_col] == cond) & (~df[cond_col].isna())][col].value_counts().tolist()[::-1],
                          label=cond)

  # Add an xlabel
  ax.set_xlabel(col)

  # Add a ylabel
  ax.set_ylabel('Count')
  ax.set_title(f'iGEM {var} Year by Year')
  ax.legend()
  # Show the plot
  plt.show()

def barplot(df, col, var, size):
  # Create a timeseries plot
  fig = plt.subplots(figsize=size)
  ax = sns.barplot(x=df[~df[col].isna()][col].unique().tolist(), 
                        y=df[col].value_counts().tolist()[::-1]
                        )

  # Add an xlabel
  ax.set_xlabel(col)

  # Add a ylabel
  ax.set_ylabel('Count')
  ax.set_title(f'iGEM {var} distribution')
  # Show the plot
  plt.show()


#create function to get a color dictionary
def get_colordict(palette,number,start):
    pal = list(sns.color_palette(palette=palette, n_colors=number).as_hex())
    color_d = dict(enumerate(pal, start=start))
    return color_d


def get_circle(dff, kolom, title):
  ar = []
  for list_of_strings in dff[kolom]:
    ar.extend(list_of_strings)
  # wordcloud = WordCloud()
  # ar = wordcloud.process_text(all_text)

  # Get the top 10 most frequent words and their frequencies
  top_10_words = Counter(ar).most_common(10)
  words, frequencies = zip(*top_10_words)
  df_words = pd.DataFrame(top_10_words, columns = ['words', 'freq'])
  df_words['percentage'] = (df_words['freq']/sum(frequencies))*100
  df_words['percentage'] = df_words['percentage'].astype(int)

  # compute circle positions:
  circles = circlify.circlify(df_words['percentage'].tolist(),
                              show_enclosure=False,
                              target_enclosure=circlify.Circle(x=0, y=0)
                            )
  n = df_words['percentage'].max()
  color_dict = get_colordict('RdYlBu_r',n ,1)
  fig, ax = plt.subplots(figsize=(9,9), facecolor='white')
  ax.axis('off')
  lim = max(max(abs(circle.x)+circle.r, abs(circle.y)+circle.r,) for circle in circles)
  plt.xlim(-lim, lim)
  plt.ylim(-lim, lim)

  # list of labels
  labels = list(df_words['words'])
  counts = list(df_words['percentage'])
  labels.reverse()
  counts.reverse()

  # print circles
  for circle, label, count in zip(circles, labels, counts):
      x, y, r = circle
      ax.add_patch(plt.Circle((x, y), r, alpha=0.9, color = color_dict.get(count)))
      plt.annotate(label +'\n'+ str(count)+'%', (x,y), size=12, va='center', ha='center')
  plt.title(str(title))
  plt.xticks([])
  plt.yticks([])
  plt.show()

def wordcloud(dff, kolom, stopwords, title) :

  # Menggabungkan semua teks dalam kolom 'content_clean' menjadi satu string
  all_text = ' '.join(dff.dropna(subset=[kolom])[kolom].tolist())

  # Membuat Wordcloud
  wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
  word_counts_raw = wordcloud.process_text(all_text)

  wordcloud.to_file(title + '.png')

  # Access the raw word counts
  word_counts = wordcloud.words_
  # Menampilkan Wordcloud
  plt.figure(figsize=(10, 5))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.title(title)
  plt.axis('off')
  plt.show()
  # return(all_text, word_counts_raw)

df = get_df('processed_team_list.csv')
#TIME SERIES YEARLY
# Plot yearly plot for tracks 1 and 2
condition = df[~df['Track'].isna()]['Track'].unique()
yearly_plot_multi(df, 'Year', 'Tracks', condition, 'Track', (30, 10))

# Plot yearly plot for region 1 and 2
condition = df[~df['Region'].isna()]['Region'].unique()
yearly_plot_multi(df, 'Year', 'Regions', condition, 'Region', (10, 5))

# Plot yearly plot for kind 1 and 2
condition = df[~df['Kind'].isna()]['Kind'].unique()
yearly_plot_multi(df, 'Year', 'Kind', condition, 'Kind', (10, 5))

yearly_plot(df, 'Year', 'Teams Applicants')

#BARPLOT
barplot(df[df['Year']==2023], 'Country', '2023 Country', (40, 10))

barplot(df[df['Year']==2023], 'Track', '2023 Track', (20, 5))

barplot(df[df['Year']==2023], 'Kind', '2023 Kind', (10, 5))

df['Track'] = df['Track'].astype(str)
#WORDCLOUD
get_circle(df, 'Keywords', 'General Keywords')
wordcloud(df, 'Keyword_merged', stopwords, 'wordcloud-general')