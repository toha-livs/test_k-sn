# -*- coding: utf-8 -*-
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



# @pytest.fixture(scope='session')
# def database(request):
#     '''
#     Create a Postgres database for the tests, and drop it when the tests are done.
#     '''
#     pg_host = DB_OPTS.get("host")
#     pg_port = DB_OPTS.get("port")
#     pg_user = DB_OPTS.get("username")
#     pg_db = DB_OPTS["database"]
#
#     init_postgresql_database(pg_user, pg_host, pg_port, pg_db)
#
#     @request.addfinalizer
#     def drop_database():
#         drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6)
import myapp


@pytest.fixture(scope='session')
def app():
    '''
    Create a Flask app context for the tests.
    '''
    app = myapp.app
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/anton_test'
    return app


@pytest.fixture(scope='session')
def _db(app):
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    return myapp.db

@pytest.fixture
def client(app):
    """client app"""
    return app.test_client()


__author__ = 'manitou'
