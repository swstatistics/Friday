# Friday Data Challange
Data Challange for the vacancy as Data Scientist at Friday [GitHub Link](https://github.com/swstatistics/Friday).

***

## Table of Contents



## workflow description
In this section I will describe my workflow for this project as well as some instructions to read the notebooks and code:  
1. A project folder and git repository is generated and everything is set up on a master and a dev branch (usually other branches / stages would be used for code review and testing) 

2. Setting up the folder for an efficient workflow. This includes:
    * a workflow manager that contains relative paths in the project. This enables 3rd parties to read and run the code on their machine. 
    * a virtual environment for the project is generated and the requirement file for this python environment is added (this could be improved by using docker -> maybe I have time to set this up)   
    * labeling  

3. Taking a good look at the Data and (notebook 00)
    * First the data will be looked at in python to get an Idea what is there and what not. 
    * Next the data will be exported and visualized in Power bi (or an equivalent). This helps to see the structure of the data. Even interactions can be seen.
    
4. Preparing the data for modelling. (notebooks 01 + 02)
    * The data is grouped, binned and one-hot-encoded to be analyzed with a model (in this case a GLM)
    * For this project, I wrote a simple modelling engine, that allows:
        * Changing the binning, grouping and taking in and out features very easy
        * the return value of the engine is a dictionary with all the necessary information to fit, predict and plot the data for the train as well as the test data.

    



## Setup
* Create a python environment and install the requirements.txt with pip. 
* For power bi: go to the windows apps store and install the power bi for desktop app.


