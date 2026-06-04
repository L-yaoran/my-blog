# -*- coding: utf-8 -*-
from app import app
with app.test_client() as c:
    r = c.get('/practice/001/')
    print('Status:', r.status_code)
    print('Contains section:', b'\xe4\xb8\x80\xe3\x80\x81\xe9\x80\x89\xe6\x8b\xa9\xe9\xa2\x98' in r.data)
    print('Contains CodeMirror:', b'codemirror' in r.data)
    print('Contains quiz id:', b'001' in r.data)
    r2 = c.get('/practice/999/')
    print('404 for unknown:', r2.status_code)