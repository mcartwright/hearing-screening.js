# hearing-screening.js
A very, simple, lightweight hearing screening in JavaScript to ensure that a participant's playback device can reproduce and the participant themselves can perceive a specified range of frequencies.

# Demo without backend
To demo it without the backend (output code is given to user to copy and paste into another application), simply run `python -m SimpleHTTPServer` from the static directory (i.e., `hearing-screening.js/hearing_screening/static`), and visit <http://localhost:8000>

# Inputs and outputs
When a user opens the page, a dialog box will appear asking for their username. If you want to automatically populate this variable, then pass and `inputCode` GET variable (e.g., `inputCode=1`). This identifier is used in a hash function to generate the output code which you can use to verify if they passed or not.

The passing output code is an md5 hash of `"pass" + inputCode + inputCode`.
The failing output code is an md5 hash of `"fail" + inputCode + inputCode`.

e.g. A passing output code with inputCode="hello" is `md5("passhellohello")`, or rather `'afa8ed14c3237993406a436a92e17b1d'`.

# Backend
If you want to run a simple backend in which the responses are saved to a sqlite (or any database supported by sqlalchemy), we provide a very simple Flask backend.

1. Install the backend locally: `pip install -e .`
1. Create the database: `python create_db.py`
1. Run the backend locally: `FLASK_APP=hearing_screening flask run`
1. Open your browser and visit <http://127.0.0.1:5000/?backend=1>

The GET variable `backend=1` in the URL tells the application to save the output code to the database rather than return it in the modal dialog.

For more information on Flask and how to deploy on server, see <http://flask.pocoo.org/docs/0.12/deploying/>
