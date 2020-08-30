# thingiverse-browser
author: Thijs Roumen 
date: 2020.07.02

usage: python3 browser.py -s searchTerm -n imageCount

A simple tool to retreive preview images and basic data of thingiverse models. It automatically runs a series of queries using the thingiverse API based on your search term stores that data in a CSV file and creates a folder structure with preview images to get a sense for the models in each category
folder structure looks like this:

search term

+--- all-models-(number of models)  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id1.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id2.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_idn.jpg  

+--- hasMakes-(n)  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id1.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id2.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_idn.jpg  

+--- isRemix-(n)  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id1.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id2.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_idn.jpg  

+--- isRemix-and-hasMakes-(n)  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id1.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id2.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_idn.jpg  

+--- customizable-(n)  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id1.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id2.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_idn.jpg  

+--- customizable-and-hasMakes(n)  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id1.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_id2.jpg  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  
&nbsp;&nbsp;&nbsp;&nbsp;+--- thingiverse_idn.jpg  


# Getting Started
first of all sign up for a thingiverse account and set up an App on thingiverse (doesnt have to be public, but you need it to get an API key)
https://www.thingiverse.com/developers/getting-started

make a separate file called "api-key" next to this python file and put just the API key in it

install all dependencies:
* [requests](https://requests.readthedocs.io/en/master/): pip3 install requests
* [json](https://docs.python.org/3/library/json.html): pip3 install json
* [csv](https://docs.python.org/3/library/csv.html): pip3 install csv
