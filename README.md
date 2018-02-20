# hearing-screening.js
A simple hearing screening in JavaScript

# Demo
To demo it, simply run `python -m SimpleHTTPServer`, and visit <http://localhost:8000>

# Inputs and outputs
When a user opens the page, a dialog box will appear asking for their username. If you want to automatically populate this variable, then pass and `inputCode` GET variable (e.g., `inputCode=1`). This identifier is used in a hash function to generate the output code which you can use to verify if they passed or not.

The passing output code is an md5 hash of `"pass" + inputCode + inputCode`.
The failing output code is an md5 hash of `"fail" + inputCode + inputCode`.

e.g. A passing output code with inputCode="hello" is `md5("passhellohello")`, or rather `'afa8ed14c3237993406a436a92e17b1d'`.

# Backend
If you want to run a simple backend in which the responses are saved to a sqlite (or any database supported by sqlalchemy), we provide a very simple Flask backend. To save to the backend add in the GET variable `backend=1` to the URL.

http://flask.pocoo.org/docs/0.12/deploying/
