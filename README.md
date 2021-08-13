# Movie_Recomendation_System
## Content based recommendation system reccomend the similar movies on the basis of genre and analyses the sentiments on the reviews given by the user for that movie.

https://user-images.githubusercontent.com/71813414/127608723-9c577fe9-a59a-4c9f-b99b-17c9b815fb39.mp4

 This application provide better user experiance and best recomendation for cinephile.Users need not to  worry if the movie that they looking for is not auto-suggested. Just type the movie name and click on "enter". they will be good to go eventhough if you made some typo errors.

 The core recommendation engine devloped by cosine similarity .Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.
 
![cosine_sim](https://user-images.githubusercontent.com/71813414/127610604-ae425b7c-4418-4f27-9718-7b6f0217e53b.png)

## Data Collection
    Data collected from TMDB site through API.
    Through Ajax request I was able to get the data.

## Sentiment Analysis
    Web Scraping(beatufulSoup library) is used to collect the reviews 
    used TfidfVectorizer to convert into vector . 
    Naive Bayes algorithm used for making model 
## Data set
   https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset
 


