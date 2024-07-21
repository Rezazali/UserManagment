# Back-End

This template should help get you started developing with Fast Api.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/).

## Project Setup

1. First, install the APK on your phone.
```sh
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment

```sh
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

3. Install the dependencies

```sh
pip install fastapi sqlalchemy uvicorn pymysql
```
## Running the Application
### Start the FastAPI Server for Development

```sh
uvicorn main:app --reload
```
### Tip
 You must have installed SQL Server and SQL Work Manager
 and enter your username and password in the database section of the project so that you can see the saved data.
 
```sh
URL_DATABASE = 'mysql+pymysql://root:RezA8595***@localhost:3306/usermanagment'
```
