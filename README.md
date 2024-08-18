# Demyst.io

Demyst.io is a locally hosted web application containing a natural language processing chatbot assistant with the ability to complete various tasks.

## Acknowledgements
This project was made possible with the use of the following libraries and tools :
* [Tensorflow](https://www.tensorflow.org/) for training our chatbot model
* [Natural Languege Toolkit](https://www.nltk.org/) for preprocessing user text inputs
* [NumPy](https://numpy.org/) for numerical computation
* [Wikipedia](https://pypi.org/project/wikipedia/) for pulling article summaries
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/#:~:text=Beautiful%20Soup%20is%20a%20library,and%20modifying%20the%20parse%20tree.) for webscrapping

## Features
The currently supported features are :
* Pull wikipedia article summary based on user question
* Hold basic social interactions with user
* Perform arithmetic calculations with order of operators

More features are currently under development

## Setup
1. Make sure to have a stable internet connection
2. Clone the repository
~~~bat
git clone https://github.com/NadeemSamaali/Demyst.io
cd Demyst.io
~~~

3. Install the necessary dependencies
~~~bat
call configure.bat
~~~

4. Launch the web application
~~~bat
call run.bat
~~~

To run future instances of Demyst.io, only execute step 4.
