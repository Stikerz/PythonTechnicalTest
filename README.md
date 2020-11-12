# Origin Markets Backend Test


This project was written using python3.7. A requirements
 folder is
 included to install the dependencies

## Running with Docker
- A Docker Compose file is provided that will run the application in an
 isolated environment

- Make sure you have `docker & docker-compose` installed and that the Docker
 daemon is running
 
- Build & Run the image: `docker-compose up --build`

- Start using web app: `http://localhost:4200/`

- Check Django backend server `http://localhost:8000/`

## Running with a virtual environment 

#### Run Django Server

- To run the application in a virtual Python environment, follow these instructions. This example will create a virtual Python environment

- Check you have the pynv version you need:
pyenv versions

- You should see 3.7.6

- If you do not have the correct version of Python, install it like this:
pyenv install 3.7.6

- On command line do this:
~/.pyenv/versions/3.7.6/bin/python -m venv env

- This creates a folder called env. Then do this to activate the virtual environment:
source env/bin/activate

- Lastly do this to check that you are now on the correct Python version:
python --version

To check we are on the right Python version

- You can install the dependencies with `pip install -r requirements/all.txt`

- You can then run the migrations commands with `python manage.py
 makemigrations
` then
 `python manage.py
 makemigrations
` in the origin directory

- You can then run the server command with `python manage.py runserver`

## Project Structure Notes

- The Backend Django Rest Framework  are stored in the `origin/bonds
` folder
- User authentication is implemented using drf tokens.
- Project uses sensitive info hardcoded  in `origin/settings` for
 dev purposes only ( store sensitive data are either with environment
  variables or via a json file in production)
- Django server 'runserver' for dev purposes only, server such a gunicorn for
 prod
 
## API Endpoints using DRF
- Get/Post Bonds : origin/bonds/?legal_name=
- Get/Post User : origins/users/

## Testing
- Run python manage.py test origin.bonds.tests # Run test


## Coverage 

```

Module	                                  Statements Missing Exclude Coverage
-----------------------------------------------------------------------------
bonds/__init__.py	                       0	0	0	100%
bonds/admin.py	                               3	0	0	100%
bonds/helpers/currencies.py	               1	0	0	100%
bonds/models.py	                               17	0	0	100%
bonds/serializers.py	                       57	0	0	100%
bonds/tests/support/assertions.py	       11	0	0	100%
bonds/tests/support/helpers/sample_data.py     2	0	0	100%
bonds/tests/test_bond_views.py	               91	0	0	100%
bonds/tests/test_user_views.py	               57	0	0	100%
bonds/urls.py	                               3	0	0	100%
bonds/utils/services.py	                       16	0	2	100%
bonds/views.py	                               25	0	7	100%
origin/__init__.py	                       0	0	0	100%
origin/settings.py	                       19	0	0	100%
origin/urls.py	                               4	0	0	100%
-----------------------------------------------------------------------------
Total	                                       303	0	9	100%
```


## Assesment Spec

We would like you to implement an api to: ingest some data representing bonds, query an external api for some additional data, store the result, and make the resulting data queryable via api.
- Fork this hello world repo leveraging Django & Django Rest Framework. (If you wish to use something else like flask that's fine too.)
- Please pick and use a form of authentication, so that each user will only see their own data. ([DRF Auth Options](https://www.django-rest-framework.org/api-guide/authentication/#api-reference))
- We are missing some data! Each bond will have a `lei` field (Legal Entity Identifier). Please use the [GLEIF API](https://www.gleif.org/en/lei-data/gleif-lei-look-up-api/access-the-api) to find the corresponding `Legal Name` of the entity which issued the bond.
- If you are using a database, SQLite is sufficient.
- Please test any additional logic you add.

We should be able to send a request to:

`POST /bonds/`

to create a "bond" with data that looks like:
~~~
{
    "isin": "FR0000131104",
    "size": 100000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}
~~~
---
We should be able to send a request to:

`GET /bonds/`

to see something like:
~~~
[
    {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNPPARIBAS"
    },
    ...
]
~~~
We would also like to be able to add a filter such as:
`GET /bonds/?legal_name=BNPPARIBAS`

to reduce down the results.
