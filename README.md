# Anacoreta - Sorian frame of mind #

# :warning: :warning: UNDER DEVELOPMENT :construction: ONLY FOR TESTING PURPROSES :warning: :warning: #

Anacoreta extracts trendings topics and analyzes sentiment in a city (Soria, Spain, in the examples, but it could analyze another city without hard changes).
Using simple natural language processing, it returns ten trending topics and a value for the sentiment [-1, 1].

The app runs a worker which updates the natural language writes sources (newspapers' articles and tweets writing with some keywords or from the city).
When a new text is added to sources, Anacoreta extracts the trending topics and the sentiment analysis and sends
update values through WebSocket to the front.

This project has been carried out exclusively to test some of the technologies used.
At the moment, it is not expected to have a stable short-term version. You can see a deployed version at https://anacoreta.herokuapp.com/.


## Stack ##
Main tools:
- Python
- Flask
- Flask-SocketIO
- TextBlob
- Sklearn
- Redis
- PostgreSQL


## Run on local environment (uncomplete) ##
You need Postgres and Redis installed in your system to run the app.

Rename the .env.example as .env and fill the values.

Create a virtual env and install depencies (see requirements.txt)

Run the webapp:

`gunicorn --worker-class eventlet -w 1 anacoreta:app`


Run the consumers (worker):

`python -m app.tasks.run_consumers`

## How to deploy in Heroku (uncomplete) ##
You need a free or paid Heroku account with _Heroku Postgres_ and _Redis To Go_ add-ons. Then set the environment variables
that contained at the .env.example file.

This project contains a Procfile to deploy in Heroku, so you only need upload the code to the server
and Heroku build the dynos and launch the app, check, for example, [Deploying with Git](https://devcenter.heroku.com/articles/git)
at Heroku docs.


### Inspired by (uncomplete) ###
- [Easy WebSocket with Flask and Gevent](https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent)
- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [How to Mine Popular Trends on GitHub using Python](https://hub.packtpub.com/mine-popular-trends-github-python-part-2/)
- [Topic Modeling in Python with NLTK and Gensim](https://datascienceplus.com/topic-modeling-in-python-with-nltk-and-gensim/)

And many many more I don't remember.


### Next steps ###
- Add tests!!
- Better filter for trending topic words (remove usernames, nonsense strings, etc.)
- Fix some codifications issues
- ...
