# Coding Exercise for ORNL Software Engineer Job (6694)

## Table of Contents

- [Coding Exercise for ORNL Software Engineer Job (6694)](#coding-exercise-for-ornl-software-engineer-job-6694)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
  - [API Response Example:](#api-response-example)
  - [Ways to test it](#ways-to-test-it)
  - [What can be improved](#what-can-be-improved)

## Background

For this coding exercise, I decided to go with a Python based approach using [Flask](https://flask.palletsprojects.com/en/2.0.x/). There are 2 programs in this project. One is the main application called main.py that should be executed first. The other is a testing application called tester.py that runs different test cases containing requests with different parameters against the API and prints the API's JSON response. 

## Install

1. Install Python (I used version 3.10 for Windows)
2. While in the project directory, start a virtual Python environment.

    ```bash
    # Create virtual Python environment
    $ py -m venv venv
    ``` 
    On Windows, activate the virtual environment by doing:
    ```bash
    $ . venv/Scripts/activate.bat
    ``` 
    On MacOS, activate the virtual environment by doing:
    ```bash
    $ . venv/bin/activate
    ``` 
    **After activating it, open up a fresh new terminal within the project directory to ensure you're in the activated virtual environment**

3. Install the project dependencies using the provided `requirements.txt` file
   ```bash
   $ pip install -r requirements.txt
   ``` 



## Usage

1. While in the root project directory, open up a terminal, run the main application:
   ```bash
   $ py main.py
   ``` 
2. To run the test cases(be sure that the application is running in the background), open up a seperate terminal, navigate to the root project directory and run the following command:
   ```bash
   $ py tester.py
   ``` 

## API Response Example:

Performing a GET request to the following URL:

`http://127.0.0.1:5000/batch_jobs?filter[submitted_after]='2018-03-04T18:57:37+00:00'&filter[submitted_before]='2018-03-04T20:24:01+00:00'&filter[min_nodes]=100&filter[max_nodes]=1900`

should output something like:

```
{
    "links": {
        "self": "http://127.0.0.1:5000/batch_jobs?filter[submitted_after]=%272018-03-04T18:57:37+00:00%27&filter[submitted_before]=%272018-03-04T20:24:01+00:00%27&filter[min_nodes]=100&filter[max_nodes]=1900"
    },
    "data": [
        {
            "type": "batch_jobs",
            "id": "1",
            "attributes": {
                "batch_number": 970,
                "submitted_at": "2018-03-04T20:16:49",
                "nodes_used": 741
            }
        }
    ]
}

```
## Ways to test it
You can test the API by running my tester program as I explained above. You can also use API testing software (such as Postman) to test it as well as pasting the request into the browser.

Here are some URL's you can test out to see different results. Assuming main.py is running, you can click on the URL's below to view the API's JSON response within the web browser:

http://127.0.0.1:5000/batch_jobs

http://127.0.0.1:5000/batch_jobs?filter[max_nodes]=20

http://127.0.0.1:5000/batch_jobs?filter[min_nodes]=19000

http://127.0.0.1:5000/batch_jobs?filter[submitted_before]='2018-02-28T00:14:25+00:00'

http://127.0.0.1:5000/batch_jobs?filter[submitted_after]='2018-03-04T23:45:37+00:00'

http://127.0.0.1:5000/batch_jobs?filter[submitted_after]='2018-03-04T18:57:37+00:00'&filter[submitted_before]='2018-03-04T20:24:01+00:00'&filter[min_nodes]=100&filter[max_nodes]=1900

## What can be improved
* While Flask request object make it easy to retrieve GET parameters, it's not doing any data validation. The better way is to use a Object Data Mapper like marshmallow to do data validation and filtering to ensure app security.  

* Formatting the "submitted_at" value to also include the "+00:00" format at the end and consider it when creating & querying the database. This program doesn't consider the "+00:00" portion since all dateTime values from the csv file seems to have the same "+00:00" portion at the end of all of them.

* Handling scenarios when http status errors occurs 


