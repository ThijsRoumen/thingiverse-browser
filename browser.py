#==========================================
# Title:  browser.py
# Author: Thijs Roumen (firstname.lastname [at] hpi.de)
# Date:   2020.07.05
#==========================================
import requests
import json
import csv
import os
import sys

searchTerm ="laser cut"                     # default search term (if no CLI args provided)
imageCount = 5                              # default imageCount per folder
apiURL = 'https://api.thingiverse.com'      # thingiverse API URL
usage = "usage: {} -s <searchTerm> -n <imageCount>".format(sys.argv[0])

# runs the API call to search with the given parameters (for more documentation: https://www.notion.so/Thingiverse-Search-API-f7ce7608d54d44f7a2b902a83194a8b2)
# string searchTerm
# int show is the number of sample things to inspect, if 0 it shows the max of 10.000 models
# bool hasMakes, isRemix, isCustomizable are all search filters
# string sort contains the sorting criteria, options are: relevant, text, popular, makes, newest if 0 defaults to popular
def runQuery(searchTerm,show,hasMakes,isRemix,isCustomizable,sort):
    filter = ""
    if hasMakes:        filter +="&has_makes=true"
    if show>0:          filter +="&per_page={}".format(show)
    if show==0:         filter +="&per_page=10000"
    if isRemix:         filter +="&is_derivative=true"
    if isCustomizable:  filter +="&customizable=true"
    if sort != 0:       filter += "&sort={}".format(sort)
    else:               filter += "&sort=popular"
    query = "{}/search/{}?access_token={}{}".format(apiURL,searchTerm, apiKey, filter)
    return requests.get(query).json()

# retrieves the file info for a thing ID in a separate API call
def getFileInfo(thing):
    # TODO: update the url to retrieve file data
    query = "{}/things/{}/files/?access_token={}&type=display&size=large".format(apiURL, thing, apiKey)
    return requests.get(query).json()



# retrieves the image info for a thing ID in a separate API call
def getImageInfo(thing):
    query = "{}/things/{}/images/?access_token={}&type=display&size=large".format(apiURL, thing, apiKey)
    return requests.get(query).json()

 # returns a list of the first page of thing ids based on the search result
def getThingIDs (query):
    thing_ids = []
    for thing in query['hits']:
        thing_ids.append(thing['id'])
    return thing_ids

# creates a folder for the given query with selected images
def makeImageFolder(query,term):
    dirname= "{}/{}{}".format(searchTerm,term,query['total'])
    try:
        os.mkdir(dirname)
    except FileExistsError as e:
        pass
    ids = getThingIDs(query)
    for id in ids:
        imageInfo = getImageInfo(id)
        for size in imageInfo[0]['sizes']:
            img_data = requests.get(size['url']).content
            with open("{}/{}.jpg".format(dirname,id), 'wb') as fileHandler:
                fileHandler.write(img_data)

# creates a directory for the search term
# if a directory with that name already exists simply use that
def makeMainDir():
    try:
        os.mkdir(searchTerm)
    except FileExistsError as e:
        print ("directory {} already exists, overwriting that one".format (searchTerm))
        pass

# runs the API calls, documents them in the CSV file and creates a folder with images
# params:
# csv.DictWriter writer writes to the CSV file
# list headers contains the CSV header row names
# string criterium is the name of the specified filtered search
# string searchTerm
# int show is the number of sample things to inspect, if 0 it shows the max of 10.000 models
# bool hasMakes, isRemix, isCustomizable are all search filters
# string sort contains the sorting criteria, options are: relevant, text, popular, makes, newest if 0 defaults to popular

def process(writer,headers,criterium,searchTerm,show,hasMakes,isRemix,isCustomizable,sort):
    query = runQuery(searchTerm,show,hasMakes,isRemix,isCustomizable,sort)
    writer.writerow({headers[0]: criterium, headers[1]: str(query['total']), headers[2]: str(getThingIDs(query))})
    makeImageFolder(query,criterium+"-")

# checks the arguments and sets the globals accordingly
# currently three arguments are supported (but easy to extend): -s for searchterm -n for imageCount and -h for help
# params:
# list args are the CLI arguments
# int n is the current argument to process
def setArgument(args,n):
    if (args[n] == "-s"):
        global searchTerm
        searchTerm = args[n+1]
    if (args[n] == "-n"):
        global imageCount
        imageCount = int(args[n+1])
    if (args[n] == "-h"):
        print(usage)
        sys.exit(2)

# processes the CLI arguments to set the global variables
def checkForArguments(args):                                                # processing CLI arguments
    if len(args) >1:                                                        # if only one argument is found use default globals
        setArgument(args,1)                                                 # set the first argument
        if (len(args) > 3):                                                 # there are more arguments
            setArgument(args,3)                                             # set the second argument
            if (len(args) > 5):                                             # if more than 3 arguments are provided something is wrong, warn the user and exit
                print("more arguments than expected \n {}".format(usage))
                sys.exit(2)

checkForArguments(sys.argv)
makeMainDir()
with open("api-key", 'r') as keyFile:                                       # for security reasons do not share your API key publicly ;) I placed it in a separate file called api-key with only that string in it
    apiKey = keyFile.readline().strip()
with open("stats-{}.csv".format(searchTerm), 'w', newline='') as csvfile:   # builds up the CSV file and processes all the queries
    fieldnames = ['criterium', 'model_count', 'samples']                    # names of the headers in the CSV
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    process(writer,fieldnames,"all-models",searchTerm,imageCount,0,0,0,0)
    process(writer,fieldnames,"hasMakes",searchTerm,imageCount,1,0,0,0)
    process(writer,fieldnames,"isRemix",searchTerm,imageCount,0,1,0,0)
    process(writer,fieldnames,"isRemix-and-hasMakes",searchTerm,imageCount,1,1,0,0)
    process(writer,fieldnames,"customizable",searchTerm,imageCount,0,0,1,0)
    process(writer,fieldnames,"customizable-and-hasMakes",searchTerm,imageCount,1,0,1,0)
