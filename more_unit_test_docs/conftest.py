# content of conftest.py

import pytest
from pytest import fixture


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "marker_name : marker test written into conftest.py for a better understanding"
    )
    config.addinivalue_line(
        "markers", "marker_name1 : marker test written into conftest.py for a better understanding"
    )
    config.addinivalue_line(
        "markers", "marker_name2 : marker test written into conftest.py for a better understanding"
    )
    config.addinivalue_line(
        "markers", "marker_name3 : marker test written into conftest.py for a better understanding"
    )
    config.addinivalue_line(
        "markers", "marker_name4 : marker test written into conftest.py for a better understanding"
    )


@fixture(scope='session')
def I_handle_DB_URL_FILE_in_class():
    print(" --> connect to DB/URL/FILE in class", end=' ')
    yield
    print(" --> disconnect from DB/URL/FILE in class", end=' ')


@fixture(scope='function', params=[10, 20])
def different_values_tested_in_param(request):      # param and request are keywords
    print(f" --> fixture opened with {request.param}", end=' ')
    return request.param

@fixture(scope="class")
def value_given_by_fixture(request):
    request.cls.input = [10,20]

