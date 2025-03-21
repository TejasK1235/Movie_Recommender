from setuptools import setup

REPO_NAME = "Movie-Recommender"
AUTHOR_USER_NAME = "TejasK1235"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['flask','nltk','pandas','numpy','scikit-learn','pickle','requests','seaborn','matplotlib']


setup(
    name="Movie_Recommender",
    version="0.0.1",
    author="Tejas Kothavale",
    author_email="kothavaleptejas@gmail.com",
    packages=[SRC_REPO],
    install_requires=LIST_OF_REQUIREMENTS
)
