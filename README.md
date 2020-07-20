## Qauntum API

Django Rest API backend for [Quantum Coasters](https://github.com/MattCrook/quantum-front-end-capstone). For more information and details regarding this project, please see the github page for the front-end application.

### Project Set Up to Run Locally
1. Clone it:
   * `git@github.com:MattCrook/quantumapp-api.git`
2. Set up your virtual environment:
   * python -m venv `QuantumEnv`
3. Activate virtual environment:
   * `source ./QuantumEnv/bin/activate`
4. Install dependencies:
   * `pip install -r requirements.txt`
5. Run migrations:
   * `python manage.py makemigrations`
   * `python manage.py migrate`
6. Load fixtures:
   * `python manage.py loaddata */fixtures/*.json`
7. Start the API server:
   * `python manage.py runserver` 
