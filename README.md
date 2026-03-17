Imports:

This project requires these installations:
python -m pip install --upgrade pip
pip install mysql-connector-python python-dotenv

Tabulate
https://pypi.org/project/tabulate/
installed via: pip install tabulate

The user will need to set up their own mysql connection,
and create a .env file.
Example can be found in .env.example

The seed data is located in csv files.
Bootstrapping the database is taken care of by the app.

You can change the user in the menu. The user id 1 is reserved for the seeded user.
You can use another id if you would like to start with an empty user.