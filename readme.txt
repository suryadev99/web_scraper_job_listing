#Instructions for setting it up
#To install all libraries
pip install -r requirements.txt

#to use a particular version of python
py -3.9 -m pip install -r requirements.txt

#create virtual env
py -3.9 -m venv myenv

#activate virtual env
myenv\Scripts\activate

#To run the script
py -3.9 scraping.py
