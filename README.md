## Hedgehog Image Listing APP (Django Rest APIs )

This is a Django rest framework app for performing curd operations on Image data.

## Project Structure

The `hedgehog` directory holds the application settings.

- `applications/api/views.py` Where all the APIs defined.
- `applications/api/tests.py`  Where all the unit test defined

The main directory holds the following files:
- `manage.py` Where the Django application is initialize and the config is loaded
- `requirments.txt` Where the dependencies this project needs to run are located.


### Project setup
```
#Clone the project repository
git clone git@github.com:savad/hedgehog.git
 
# navigate to the yousician directory
cd hedgehog

# create a virtual environment for hedgehog
python3 -m venv hedgehog-venv

# activate the virtual environment
source hedgehog-venv/bin/activate
```

Install dependencies
```
pip install -r requirments.txt
```


### Configure Database
 To simplify development you can use default sqlite database.



### List of APIs
* Swagger is configured in this project.
* Navigate to home page (/) for accessing swagger.
* For downloading swagger JSON file, access http://{domain}/swagger.json


### API user Authorization
```commandline
Request a token using /api/v1/login/ endpoint

Use the token in the request header as
Authorization: Token xxxxxxxxxxxxxxxxx
```
### Start the application
```
python manage.py runserver

```

### Execute tests
```
python manage.py test
```



