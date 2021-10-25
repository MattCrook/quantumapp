## Qauntum API

Django Rest API backend for [Quantum Coasters](https://github.com/MattCrook/quantum-front-end-capstone). For more information and details regarding this project, please see the github page for the front-end application.

### Project Set Up to Run Locally

##### The setup commands can be run by using the Makefile targets as follows:

```
- pip3 install virtualenv
- make venv_create
- make venv_init
- make migrate
- make run_local
```

##### Or, follow step by step:
1. Clone it:
   * `git@github.com:MattCrook/quantumapp-api.git`
2. Set up your virtual environment:
   * python -m venv `venv`
   * Or `sudo pip3 install virtualenv` / `pip3 install virtualenv`
3. Activate virtual environment:
   * `source ./venv/bin/activate`
4. Install dependencies:
   * `pip3 install -r requirements.txt` / `pip3 install -r requirements.txt --no-cache-dir`
5. Run migrations:
   * You can use SQLite3 or PostgreSQL as the database. Just be sure whichever you choose to use it set to the default in `settings.py`.
   * Run:
   * `python3 manage.py makemigrations`
   * `python3 manage.py migrate`
6. Load fixtures:
   * `python3 manage.py loaddata */fixtures/*.json`
7. Start the API server:
   * `python3 manage.py runserver`
* Note: You may have to change the default database in `settings.py` depending on which database you want to use.
  * Currently it is running with a PostgreSQL image.
  * If you want to just run locally for testing purposes, before you run `makemigrations` and `migrate`:
    * Change the default database to be sqlite, instead of postgres.
    * Then run `makemigrations` and `migrate`.
    * This will create a local DB for you to run the app with.

#### Docker

Can also run with Docker

```
make docker_build_local
make docker_run
```

#### Or run with Docker-Compose

```
make docker_compose
```
## Deployed Application

#### Production Environment

###### The production environment is currently deployed using App Engine hosted on GCP, and can be found at the below link. Login is currently dissabled as it is being re-worked. You can still see the landing page, and login through Auth0, however you will not be able to do anything in the application, as the Database is currently dissconnected and offline.

* https://api-dot-quantum-coasters.uc.r.appspot.com/

#### Development Environment

###### To clone this repo and run locally, (as of right now, this has plans to change in the future) you will need to have an Auth0 account and create an application in your Auth0 account.

###### You will then need to configure that application with the applicable Login URL, allowed callback URI's, allowed Logout URL, Allowed Web Origins, and Allowed CORS Origins. These should also be saved as env variables in your .env file locally in the root of this project. An example is provided for what variables are needed.

###### Follow instructions above to either run locally using localhost:8000, Docker, or Docker-Compose.

<!-- ## Deploy

Building image with the URI and URL of frontend and back end because dynamic.

These get injected into Dockerfile as ARGS and then set in the environment as ENV variables.

They are the IP of the load balancer, which is the backend

Then the URI of the front end. (Deployed in App Engine)

```
docker_build_deploy
```
* Frontend and backend URLs get passed to Dockerfile as build ARGS
* Image is built then pushed to Dockerhub
* They get used to create ENV variables
* When VM is provisioning it pulls the Image and starts the container, using the `env.deploy` env file, and alreasy has the ENV vars from the ARGs.
* The `settings.py` file then uses those variables in the application.

ToDo: make more dynamic so the values are not hard coded.

Make separate Settings.py files to use for different envs -->
