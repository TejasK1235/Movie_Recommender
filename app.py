import pickle
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=22f1f6bd82f63d4bcf9739e38198e938&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return "static/babrao.jpeg"  
    except requests.exceptions.RequestException:
        return "static/babrao.jpeg" 

def recommend(movie):
    if movie not in movies['title'].values:
        return None, None  

    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Load movie data
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def home():
    movie_list = movies['title'].values
    recommendations = []
    api_error = False
    movie_not_found = False
    
    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        if selected_movie:
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            if recommended_movie_names is None:
                if selected_movie not in movie_list:
                    movie_not_found = True  # Movie doesn't exist in dataset
                else:
                    api_error = True  
            else:
                recommendations = zip(recommended_movie_names, recommended_movie_posters)
    
    return render_template(
        'index.html', 
        movie_list=movie_list, 
        recommendations=recommendations,
        api_error=api_error, 
        movie_not_found=movie_not_found
    )

if __name__ == '__main__':
    app.run(debug=True)
