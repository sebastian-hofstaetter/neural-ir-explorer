# Information retrieval explorer

ir-explorer is a vue.js based user interface for any search engine (the search engine only has to expose a small rest api)

Features:
* it works with **any** search engine
* it allows to compare and analyze results for different parameter settings for the same query in one view


## Run the web-server

set FLASK_APP=api.py
flask run

## Run the webpack development builder

npm run build

## Search engine dependency

When you want to use ir-explorer with a search engine, you have to expose the following rest api endpoints: 

### Collections


### Search 