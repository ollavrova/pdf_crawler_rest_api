PDF crawler API
===============
Used technologies: python 2.7, Django 1.11.

Imagine a web application which is a web crawler that scans through web resources and documents to map the
network and find connections between document and the Internet.
This is a basic stage of the crawler - a module that collects Internet addresses
from PDF documents. Django application receives PDF documents and provides information about the Internet URLs that appear in
them.

Logic:
1. Receive a PDF file that is uploaded in an http request. Analyze the document to find
Internet URLs in the text, and then store them in the database (relational DB).
2. The PDF file/content itself is not expected to be stored.
3. The use of existing libraries for handling PDF documents is encouraged.
4. The server supports the following REST WS:
    - POST​ / FILE UPLOAD​ Uploading a PDF document, as described in part 1
    above
    - GET / JSON​ Returns a set of all the of documents that were uploaded: ids,
    names and number of URLs that were found for each document
    - GET / JSON​ Returns a set of URLs for a specific document
    - GET / JSON​ Returns a set of all URLs found, including the number of
documents that contained the URL
5. For every URL, hold an indication whether the URL is “alive”, that is, it will be false
6. Created an HTML single file that support the uploading of a PDF file. 

**Restrictions**: files with size more 5 Mb is not allowed to download.

Setup a project:
===============
- clone a project
- go to the project folder
- run next commands:
```bash
sudo apt install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

```

Testing:

```bash
python manage.py test
```

Endpoints:
=========
- GET /api/ - an HTML single file that support the uploading of a PDF file. 
- GET /api/documents/ - list of documents with sets of URLs 
- POST /api/documents/ - create a document by uploading a pdf file
- GET /api/documents/< id > - get one document and his set of URLs
- GET /api/urls/ - list of all URLs found, including the number of
documents that contained the URL


Example of usages:
-----------------
```bash
import requests
- get all documents:
requests.get('http://127.0.0.1:8000/api/documents')
<Response [200]>

[
    {
        "id": 1,
        "name": "test.pdf",
        "urls_number": 3
    }
]
- get all URLs for one document:
 r=requests.get('http://127.0.0.1:8000/api/documents/1')
>>> r.json
<bound method Response.json of <Response [200]>>
>>> r.text
{
    "id": 1,
    "name": "test.pdf",
    "urls": [
        {
            "id": 1,
            "url": "https://gist.github.com/gruber/",
            "alive": true
        },
        {
            "id": 2,
            "url": "https://gist.github.com/gruber/8891611",
            "alive": true
        },
        {
            "id": 3,
            "url": "http://daringfireball.net/2010/07/improved_regex_for_matching_urls",
            "alive": true
        }
    ]
}
 - get all URLs list
requests.get('http://127.0.0.1:8000/api/urls') 
 [
    {
        "id": 1,
        "url": "https://gist.github.com/gruber/",
        "alive": true,
        "num_docs": 1
    },
    {
        "id": 2,
        "url": "https://gist.github.com/gruber/8891611",
        "alive": true,
        "num_docs": 1
    },
    {
        "id": 3,
        "url": "http://daringfireball.net/2010/07/improved_regex_for_matching_urls",
        "alive": true,
        "num_docs": 1
    }
]

```
