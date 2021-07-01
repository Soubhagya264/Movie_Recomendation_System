import numpy as np
import pandas as pd
from flask import Flask, render_template, request,redirect,flash,url_for
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from website import create_app ,db
from website.models import User
import json
import bs4 as bs
import urllib.request
import pickle
import requests
import json
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_login import login_user,logout_user
from flask_login import login_required, current_user
# load the nlp model and tfidf vectorizer from disk
app = create_app()


@app.route("/login", methods=["POST", 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password=request.form['password']
        
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user,remember=True)
                return redirect(url_for('index'))
            else:
                flash('Incorrect Password , try again.',category='error') 
        else:
            flash('Email doesnot exist',category='error')    
                
                
        
    return render_template('login.html',user=current_user)


@app.route("/SignUP", methods=["POST", 'GET'])
def SignUP():
    if request.method == "POST":
        first_name = request.form['name']
        email = request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists",category='error')
        else:
            new_user=User(email=email,password=generate_password_hash(password,method='sha256'),first_name=first_name)
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash("Account has been created Succesfully !!")
            return redirect(url_for('index'))
    return render_template('Signup.html',user=current_user)

filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('tranform.pkl', 'rb'))


def create_similarity():
    data = pd.read_csv('main_data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data, similarity


def rcmd(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title'] == m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        # excluding first item since it is the requested movie itself
        lst = lst[1:11]
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        print(l)    
        return l


def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["', '')
    my_list[-1] = my_list[-1].replace('"]', '')
    return my_list


def get_suggestions():
    data = pd.read_csv('main_data.csv')
    return list(data['movie_title'].str.capitalize())


@app.route("/")
@app.route("/index", methods=["POST","GET"])
def index():
    return render_template('index.html',user=current_user)


@app.route("/home")
@login_required
def home():
    suggestions = get_suggestions()
    suggestion = json.dumps(suggestions)
    return render_template('home.html', suggestions=suggestion,user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route("/similarity", methods=['POST','GET'])
def similarity():
    print("successfully get into similarity")
    movie = request.form['name']
    rc = rcmd(movie)
    if type(rc) == type('string'):
        return rc
    else:
        m_str = "---".join(rc)
        return m_str


@app.route("/recommend", methods=["POST"])
def recommend():
    # getting data from AJAX request
    title = request.form['title']

    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    rec_movies = request.form['rec_movies']
    rec_posters = request.form['rec_posters']

    suggestions = get_suggestions()

    rec_movies = convert_to_list(rec_movies)
    rec_posters = convert_to_list(rec_posters)

    movie_cards = {rec_posters[i]: rec_movies[i]
                   for i in range(len(rec_posters))}

    try:
            sauce = urllib.request.urlopen(
                'https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')
            soup_result = soup.find_all("div", {"class": "text show-more__control"})
    
            reviews_list = []  # list of reviews
            reviews_status = []  # list of comments (good or bad)
            for reviews in soup_result:
                if reviews.string:
                    reviews_list.append(reviews.string)
                    # passing the review to our model
                    movie_review_list = np.array([reviews.string])
                    movie_vector = vectorizer.transform(movie_review_list)
                    pred = clf.predict(movie_vector)
                    reviews_status.append('Positive' if pred else 'Negative')
    
    # combining reviews and comments into a dictionary
            movie_reviews = {reviews_list[i]: reviews_status[i]
                     for i in range(len(reviews_list))}
    except urllib.error.URLError as e:
       print(e.reason)        

    # passing all the data to the html file
    return render_template('recommend.html', title=title, poster=poster, overview=overview, vote_average=vote_average,
                           vote_count=vote_count, release_date=release_date, runtime=runtime, status=status, genres=genres,
                           movie_cards=movie_cards, reviews=movie_reviews)


if __name__ == '__main__':
    app.run(debug=True)
