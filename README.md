## Qauntum API

Django Rest API backend for [Quantum Coasters](https://github.com/MattCrook/quantum-front-end-capstone). For more information and details regarding this project, please see the github page for the front-end application.

### Project Set Up to Run Locally
1. Clone it:
   * `git@github.com:MattCrook/quantumapp-api.git`
2. Set up your virtual environment:
   * python -m venv `venv`
3. Activate virtual environment:
   * `source ./venv/bin/activate`
4. Install dependencies:
   * `pip install -r requirements.txt`
5. Run migrations:
   * You can use SQLite3 or PostgreSQL as the database. Just be sure whichever you choose to use it set to the default in `settings.py`.
   * Run:
   * `python manage.py makemigrations`
   * `python manage.py migrate`
6. Load fixtures:
   * `python manage.py loaddata */fixtures/*.json`
7. Start the API server:
   * `python manage.py runserver`
* Note: You may have to change the default database in `settings.py` depending on which database you want to use.
  * Currently it is running with a PostgreSQL image.
  * If you want to just run locally for testing purposes, before you run `makemigrations` and `migrate`:
    * Change the default database to be sqlite, instead of postgres.
    * Then run `makemigrations` and `migrate`.
    * This will create a local DB for you to run the app with.
