
# Intro

This project is about predicting criminal activities in Tegucigalpa, capital of Honduras, which is one of the countries with the highest levels of violence and corruption in latin america. The project goal is to create a classifier that classifies local news and their location in order to identify high risk areas. 

My inspiration to build this project is the way that people in Tegucigalpa get to know which neighbourhoods are safer than others which is basically through media and by word of mouth. My dream would be to be able to generate an algorithm that might evaluate the probability of a criminal event happening someplace at a certain date. With this people could be advised to take caution or avoid passing by the higher risk areas and also support police officers. For now, I see this project as the starting point.


# Project Quick start

## Jupyter Notebooks

If you want to see the code for analysis, machine learning models and tests you can navigate to the notebooks folder and view them in github (or download them to run them in Jupyter)

In order to run the project that trains the models and shows the model results you will need to follow the next steps:
Note: The site is not yet production ready.
Note: There are two separate servers, one for the backend and another for the frontend.

1. Start the Flask server (backend)

`python ./server/backend/start.py` 

2. Start the lite NodeJs server that serves Angular pages (frontend)

`npm start --prefix server/frontend` 


# Site modules (tabs):
- Results: Here the user can run the implemented Machine Learning models and see the train/test data results. The main idea is to demonstrate the perfomance of the implemented model in order to measure improvements.
- Article Viewer: This module is to visualize case by case how well the ML model perfomed. 
    - Topic Explorer: Here we can inspect what was the category of the article and how did the model classified it.
    - Entity Explorer: Here we can see the entities of each article and the entities that the model identified.
- Map Viewer: [under construction] The results will be shown on a heatmap using google maps api. 

# Project Structure

- notebooks: a series of jupyter notebooks where I analyzed the data and experimented with classification models. 
- scrapper: a python script that uses Beatiful Soup library to scrape articles from a news site.
- ner: the Named Entity Recognition (ner) trainer. 
- pos_tagger: 
- server/backend: a small Flask server that serves the frontend with data and calls the trainer modules.
    - location: 
- server/frontend Server: a lite nodeJS server that serves Angular 2 sites.


# Project Activities

### Phase 1 Data Recolection
- Scrape news from a local Honduran news site: **100%**
- Get a list of Colonias (neighbourhoods) in Tegucigalpa: **100%**
- Basic project folder structure **100%**
- Get up cloud/git **100%**

-------
### Phase 2 Initial Exploration / Data Preparation 
- Basic feature extraction **100%**
- Manually Extract category of event from articles * **100%**
- Manually Extract location entities of event from articles *  **100%**
- Initial exploration **100%**

( * Developed a tool to view each article, classify the topic and select the location entities from text )

-------
### Phase 3 First Models 
- Topic Classifier **100%**
- Part of Speech (POS) tagger **100%**
- Name Entity Recognition **100%**
- Relationship Extraction **100%**

------
### Phase 4 Minimal Site / Backend
- Frontend
    - Results **100%**
    - Article Explorer **90%**
    - Map Viewer **50%**
- Backend
    - Train and Evaluate Models **100%**
    - Frontend API 
        - Results **100%**
        - Article Explorer **100%**
        - Map **30%**

------
### Phase 5 Site and Model Improvement
- Topic Classifier **100%**
- Part of Speech (POS) tagger **100%**
- Name Entity Recognition **50%**
- Relationship Extraction **50%**

 
