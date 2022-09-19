# -*- coding: utf-8 -*-
"""Fandango_movie_ratings_EDA.ipynb



# VINEET SRIVASTAVA
## Project: Exploratory Data Analysis: Fandango Movie rating discrepancies and comparsion with other movie sities

### The Data


#### all_sites_scores.csv

-----

`all_sites_scores.csv` contains every film that has a Rotten Tomatoes rating, a RT User rating, a Metacritic score, a Metacritic User score, and IMDb score, and at least 30 fan reviews on Fandango. The data from Fandango was pulled on Aug. 24, 2015.

Column | Definition
--- | -----------
FILM | The film in question
RottenTomatoes | The Rotten Tomatoes Tomatometer score  for the film
RottenTomatoes_User | The Rotten Tomatoes user score for the film
Metacritic | The Metacritic critic score for the film
Metacritic_User | The Metacritic user score for the film
IMDB | The IMDb user score for the film
Metacritic_user_vote_count | The number of user votes the film had on Metacritic
IMDB_user_vote_count | The number of user votes the film had on IMDb

----
----

#### fandango_scape.csv

`fandango_scrape.csv` contains every film 538 pulled from Fandango.

Column | Definiton
--- | ---------
FILM | The movie
STARS | Number of stars presented on Fandango.com
RATING |  The Fandango ratingValue for the film, as pulled from the HTML of each page. This is the actual average score the movie obtained.
VOTES | number of people who had reviewed the film at the time we pulled it.

----

**Import libraries :**
"""

# Commented out IPython magic to ensure Python compatibility.
# IMPORT HERE!

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


"""## Fandango Displayed Scores versus True User Ratings


"""

fandango = pd.read_csv("fandango_scrape.csv")

fandango.head()

fandango.info()

fandango.describe()

# CODE HERE
fig=plt.figure(figsize=(8,4),dpi=150)
sns.scatterplot(x=fandango.RATING, y=fandango.VOTES, data=fandango)
plt.show()

fandango.corr()

"""
    
**Create a new column that is able to strip the year from the title strings and set this new column as YEAR**"""

fandango['Year'] = fandango.FILM.str.split().str[-1].str.replace(r"[()]","")
fandango['Year']

"""*movies in the Fandango DataFrame per year*"""

fandango['Year'].value_counts()

"""**Visualize the count of movies per year with a plot:**"""

fig=plt.figure(figsize=(8,4),dpi=150)
sns.countplot(data=fandango,x='Year')
plt.show()

"""**10 movies with the highest number of votes**"""

fandango.nlargest(10,'VOTES')

len(fandango[fandango['VOTES']==0])

"""**TASK: Create DataFrame of only reviewed films by removing any films that have zero votes.**"""

fan_reviewed = fandango[fandango['VOTES']>0]

fan_reviewed.head()

"""

**Create a KDE plot**"""

plt.figure(figsize=[14,4])
sns.kdeplot(x='RATING',data=fan_reviewed,clip=[0,5], fill=True, label='True Rating')
sns.kdeplot(x='STARS', data=fan_reviewed,clip=[0,5], fill=True, label='stars Displayed')
#plt.legend(loc='best')
plt.legend(bbox_to_anchor=(1.20,0.5))
plt.show()

fan_reviewed['STARS_DIFF'] = fan_reviewed['STARS'] - fan_reviewed['RATING']

fan_reviewed = fan_reviewed.round(2)

fan_reviewed

plt.figure(figsize=(14,6))
sns.countplot(x='STARS_DIFF', data=fan_reviewed)
plt.show()

fan_reviewed[fan_reviewed['STARS_DIFF']==1.0]

"""## Comparison of Fandango Ratings to Other Sites


"""



all_sites.head()

all_sites.info()

all_sites.describe()

"""### Rotten Tomatoes

"""

plt.figure(figsize=(16,6))
sns.scatterplot(x='RottenTomatoes', y='RottenTomatoes_User', data=all_sites)
plt.ylim(0,100)
plt.show()

"""Let's quantify this difference by comparing the critics ratings and the RT User ratings. We will calculate this with RottenTomatoes-RottenTomatoes_User. Note: Rotten_Diff here is Critics - User Score. So values closer to 0 means aggrement between Critics and Users. Larger positive values means critics rated much higher than users. Larger negative values means users rated much higher than critics.

**TASK: Create a new column based off the difference between critics ratings and users ratings for Rotten Tomatoes. Calculate this with RottenTomatoes-RottenTomatoes_User**
"""

all_sites['Rotten_Diff'] = all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']
all_sites.head()

"""Let's now compare the overall mean difference. Since we're dealing with differences that could be negative or positive, first take the absolute value of all the differences, then take the mean. This would report back on average to absolute difference between the critics rating versus the user rating.

**TASK: Calculate the Mean Absolute Difference between RT scores and RT User scores as described above.**
"""

all_sites['Rotten_Diff'].apply(abs).mean()

"""**TASK: Plot the distribution of the differences between RT Critics Score and RT User Score. There should be negative values in this distribution plot. Feel free to use KDE or Histograms to display this distribution.**"""

plt.figure(figsize=(14,6),dpi=200)
sns.histplot(x='Rotten_Diff', data =all_sites, kde=True)
plt.title('RT Critics Score minus RT User Score')
plt.show()

"""**TASK: Now create a distribution showing the *absolute value* difference between Critics and Users on Rotten Tomatoes.**"""

plt.figure(figsize=(14,6),dpi=200)
sns.histplot(x=all_sites['Rotten_Diff'].apply(abs),bins=25,kde=True)
plt.title("Abs Difference between RT Critics Score and RT User Score");
plt.show()

"""**Let's find out which movies are causing the largest differences. First, show the top 5 movies with the largest *negative* difference between Users and RT critics. Since we calculated the difference as Critics Rating - Users Rating, then large negative values imply the users rated the movie much higher on average than the critics did.**

**TASK: What are the top 5 movies users rated higher than critics on average:**
"""

all_sites.nsmallest(5,"Rotten_Diff")

"""**TASK: Now show the top 5 movies critics scores higher than users on average.**"""

all_sites.nlargest(5,'Rotten_Diff')['FILM']

"""## MetaCritic

**TASK: Display a scatterplot of the Metacritic Rating versus the Metacritic User rating.**
"""

all_sites.head()

plt.figure(figsize=(16,6),dpi=200)
sns.scatterplot(x='Metacritic', y='Metacritic_User',data=all_sites)
plt.ylim(0,10)
plt.xlim(0,100)
plt.show()

"""## IMDB

"""

plt.figure(figsize=(16,6),dpi=200)
sns.scatterplot(x='Metacritic_user_vote_count', y='IMDB_user_vote_count',data=all_sites)
plt.show()

all_sites.nlargest(1,'IMDB_user_vote_count')

all_sites.nlargest(1,'Metacritic_user_vote_count')

"""## Fandago Scores vs. All Sites

**TASK: Combine the Fandango Table with the All Sites table. Not every movie in the Fandango table is in the All Sites table, since some Fandango movies have very little or no reviews. We only want to compare movies that are in both DataFrames, so do an *inner* merge to merge together both DataFrames based on the FILM columns.**
"""

df = pd.merge(fandango, all_sites, how='inner', on='FILM')
df.head()

"""### Normalize columns to Fandango STARS and RATINGS 0-5 



"""

df.describe().transpose()['max']

df['RT_Norm'] = np.round(df['RottenTomatoes']/20,1)
df['RTU_Norm'] = np.round(df['RottenTomatoes']/20,1)
df['Meta_Norm'] = np.round(df['Metacritic']/20,1)
df['Meta_U_Norm'] = np.round(df['Metacritic_User']/2,1)
df['IMDB_Norm'] = np.round(df['IMDB']/2,1)

df.head()

"""**TASK: Now create a norm_scores DataFrame that only contains the normalizes ratings. Include both STARS and RATING from the original Fandango table.**"""

norm_scores = df[['FILM','STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']]
norm_scores.head()

"""### Comparing Distribution of Scores Across Sites


"""

plt.figure(figsize=(15,6),dpi=200)
for i in norm_scores.columns[1:]:
    sns.kdeplot(x=norm_scores[i], data=norm_scores,shade=True,clip=[0,5])
plt.legend(norm_scores.columns[1:], bbox_to_anchor=(.25,0.75))
plt.show()

"""**Clearly Fandango has an uneven distribution. We can also see that RT critics have the most uniform distribution. Let's directly compare these two.** 

**TASK: Create a KDE plot that compare the distribution of RT critic ratings against the STARS displayed by Fandango.**
"""

plt.figure(figsize=(15,6),dpi=200)
sns.kdeplot(data=norm_scores[['RT_Norm','STARS']],shade=True,clip=[0,5])
plt.show()

"""**OPTIONAL TASK: Create a histplot comparing all normalized scores.**

**bold text**
### How are the worst movies rated across all platforms?
"""

sns.clustermap(norm_scores.loc[:,['STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']],col_cluster=False)
plt.show()

"""**Fandango is rating much more tha other sites**"""

norm_scores.nsmallest(10,'RT_Norm')

fig,ax = plt.subplots(figsize=(15,6),dpi=200)
sns.kdeplot(data=norm_scores, shade=True, clip=[0,5])
plt.show()

"""**Visualize the distribution of ratings across all sites for the top 10 worst movies.**"""

plt.figure(figsize=(15,6),dpi=200)
worst_films = norm_scores.nsmallest(10,'RT_Norm').drop('FILM',axis=1)
sns.kdeplot(data=worst_films,clip=[0,5],shade=True,palette='Set1')
plt.title("Ratings for RT Critic's 10 Worst Reviewed Films")
plt.show()

"""**Conclusion: Fandango is showing around 3-4 star ratings for films that are clearly bad! **

----
"""