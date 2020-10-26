# CS7330-Project NoSQL Databases

## Requirements

- [python version 3.8](https://www.python.org/downloads/release/python-386/) (I can change my version if both of you are using the same different version, e.g. 3.7)

- [MongoDB version 4.4 Community Edition](https://www.mongodb.com/try/download/community)

all requirements for python are in requirements.txt

## Using Cloud Mongodb

Make sure to have an account on cloud.mongodb.com The invite to Austin was to your yahoo email, so register using that email

- Accept invite in email
- Register
- Log in
- On left side
  - Database Access - add yourself
  - Network Access - add your IP
    1. Click ADD IP ADDRESS
    2. Click ADD CURRENT IP ADDRESS
    3. Put your name in Comment
- The database is under
  - Clusters - Cluster0 - Collections
- To connect to the database
  - see cloud_db_example.py
  - this uses `test_user` to connect to the DB, `test_user` **does not have write access**
  - if you cannot connect make sure you have your IP added in above steps
- How to add your user to the project
  - In `local_config.py`
  - `CLOUD_URI`
    - replace `user:password` with your user and password, this is the user/password you created in Database Access 
  - **Do not commit local_config.py to git as your password is stored here** This will be added to .gitignore once everyone has their `local_config.py` configured.

## Using MongoDB Locally

- Optional - Install MongoDB Compass - This allows you to visually inspect your local DB
- run `local_db_example.py`

## Other

You can create a folder called local under the root dir of the project and put things you want git to ignore

