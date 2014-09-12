UMAurora.py
===========

Checks for class University of Manitoba availability every minute.

Requirements
------------

1. Requests Python library
2. OSX
3. Desired course identifier, code, CRN, and SESSID cookie valie

Finding SESSID Cookie
---------------------

1. Visit http://aurora.umanitoba.ca
2. Sign in
3. Inspect the page and copy the SESSID cookie valie

Usage
-----

    python umaurora.py COURSE_IDENTIFIER COURSE_CODE COURSE_CRN SESSID

Example:
    
    python umaurora.py MKT 2210 10009 abcde12345