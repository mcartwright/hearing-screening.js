# hearing-screening.js
A simple hearing screening in JavaScript

# Demo
To demo it, simply run `python -m SimpleHTTPServer`, and visit http://localhost:8000?inputCode=1 

# Inputs and outputs
The `inputCode` GET variable is an identifier that is used in a hash function to generate the output code which you can use to verify if they passed or not.

The passing output code is an md5 hash of "pass" + (inputCode * inputCode)
The failing output code is an md5 hash of "fail" + (inputCode * inputCode)

e.g. A passing output code with inputCode=2 is `md5("pass4")`, or rather `'fc2921d9057ac44e549efaf0048b2512'`.
