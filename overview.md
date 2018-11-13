# Project Overview
This is to provide a more detailed outline of the envisioned project. 

## Website 
A website that will analyze/classify images (or URLs) based on user input. The user can upload a photo or add a link to an image. The image will then be analyzed and likely stored. The analysis along with the image will be displayed on our website. Our analysis will be based on machine learning of our choice. An example would be "Person" or "Not a person". Or we could classify into 3-10 groups. 

We will also be using an API to do analysis for us. We will use Microsoft Azure API for detailed analysis. We will also display this information on the website. 

### Here is an example of what the website could look like. 
![alt text](https://github.com/warnerm06/Final_Project_Img_Analysis/blob/master/Website_design_concept.JPG "Logo Title Text 1")

## Machine Learning
Machine learning will be the most challenging portion. We are analyzine images not csv files. Each images is represented as a matrix of pixels and associated RGB colors. A 32 x 32 pixel image would be represented as a matrix 32 tall by 32 wide of RGB colors.  

Here is an example of a 2 x 3 pixel image represented by RGB matrix. 

[[[234], [237]],  
[[245], [206]],  
[[245], [296]]]

## Good news! 
I've found a couple of tutorials on how to do image analaysis. We can easily follow along and complete the ML portion. We can continue to search for tutorials but these are the two best I found. 

### Option 1: The easiest Option. 
Use the CIFAR-10 Dataset to classify images into 10 categories. 
https://www.cs.toronto.edu/~kriz/cifar.html

Follow This tutorial: 
https://www.learnopencv.com/image-classification-using-convolutional-neural-networks-in-keras/

I've ran this code and it works. It takes ~6hrs to run the code through 50 epochs. 
We would spend our time optimizing the algorithm and understanding it. 

### Option 2: Get our Own Dataset
Use our own dataset to build a "Person" vs "Not a person" algorithm.

Follow this tutorial:
https://www.pyimagesearch.com/2017/12/11/image-classification-with-keras-and-deep-learning/

Gather the our dataset following this tutorial:
https://www.pyimagesearch.com/2017/12/04/how-to-create-a-deep-learning-dataset-using-google-images/

Pros to this is that it will be our own dataset. We will spend time collecting data as well as time training our model. 

### Option 3: Build our own dataset and model without following a tutorial. 
This would be the hardest option but doable. This opens up endless possibilities. 

## User Interface
The website that faces the client. THis would include the HTML, CSS and Javascript to build the website. 

## Database
We will need to store our image labels in some form of database. It could by SQLite, SQL or MongoDB. We will also store image filepaths there. If we want the info to be permanent SQLite may not work. 

## Azure API
We will use Microsoft Azure Cognitive Services API to do image classification. We send a url and it will send back JSON data about the image. We will then display it on our website and store the data in our database. 

I have a working Jupyter notebook of this in the Azure API folder. You will need add in the API keys I sent via slack. 

## Flask App
The flask app will be the backend of the program. It will be used as our webserver and serve HTML, JS and CSS. It will also do our database queries. 

## Image Storage
If we want to store the user images we will need permanent storage. We can use Heroku (a special heroku storage), AWS or Azure for this. Storing them in the local folder won't work because Heroku files get deleted when it shuts down.

## Other Bonus Items
Any bonus items should probably be worked on last if time remains. 








