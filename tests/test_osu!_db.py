print(__name__)

import pytest
import db
import io
import datetime

def test_read_bool():
    assert db.read_bool(io.BytesIO(b'\x00')) == False
    assert db.read_bool(io.BytesIO(b'\x01')) == True

def test_read_byte():
    assert db.read_byte(io.BytesIO(b'\x00')) == 0
    assert db.read_byte(io.BytesIO(b'\x01')) == 1
    assert db.read_byte(io.BytesIO(b'\x7f')) == 127

def test_read_short():
    assert db.read_short(io.BytesIO(b'\x00\x00')) == 0
    assert db.read_short(io.BytesIO(b'\x01\x00')) == 1
    assert db.read_short(io.BytesIO(b'\x00\x01')) == 2**8

def test_read_int():
    assert db.read_int(io.BytesIO(b'\x00\x00\x00\x00')) == 0
    assert db.read_int(io.BytesIO(b'\x01\x00\x00\x00')) == 1
    assert db.read_int(io.BytesIO(b'\x00\x00\x00\x01')) == 2**24

def test_read_long():
    assert db.read_long(io.BytesIO(b'\x00\x00\x00\x00\x00\x00\x00\x00')) == 0
    assert db.read_long(io.BytesIO(b'\x01\x00\x00\x00\x00\x00\x00\x00')) == 1
    assert db.read_long(io.BytesIO(b'\x00\x00\x00\x00\x00\x00\x00\x01')) == 2**56

def test_read_single():
    assert db.read_single(io.BytesIO(b'\x00\x00\x00\x00')) == 0
    assert db.read_single(io.BytesIO(b'\x01\x00\x00\x00')) == 1.401298464324817e-45
    assert db.read_single(io.BytesIO(b'\x00\x00\x00\x01')) == 2.350988701644575e-38

def test_read_double():
    assert db.read_double(io.BytesIO(b'\x00\x00\x00\x00\x00\x00\x00\x00')) == 0
    assert db.read_double(io.BytesIO(b'\x01\x00\x00\x00\x00\x00\x00\x00')) == 5e-324
    assert db.read_double(io.BytesIO(b'\x00\x00\x00\x00\x00\x00\x00\x01')) == 7.291122019556398e-304

def test_read_datetime():
    assert db.read_datetime(io.BytesIO(b'\x00\x00\x00\x00\x00\x00\x00\x00')) == datetime.datetime(1, 1, 1)
    assert db.read_datetime(io.BytesIO(b'\x00\x00\x00\x00\x00\x00\x00\x01')) == datetime.datetime(229, 5, 5, 23, 50, 3, 792794)

def test_read_string():
    assert db.read_string(io.BytesIO(b'\x00')) == ''
    assert db.read_string(io.BytesIO(b'\x0b\x00')) == ''
    assert db.read_string(io.BytesIO(b'\x0b\x02ab')) == 'ab'
