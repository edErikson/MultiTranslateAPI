# MultiTranslateAPI

A FastAPI application that serves as a multilingual translation database. 

## Overview

MultiTranslateAPI is a RESTful API built with FastAPI and SQLAlchemy. The application provides endpoints to query and manage a database of words and their translations into multiple languages.

The data model consists of three main entities:

- Categories: Represents a category of words.
- Words: Represents a word in English and its associated category.
- Translations: Represents a translation of a word into another language.

## Setting Up

The application uses SQLite for the database and SQLAlchemy for the ORM. You can set up the database connection by updating the `SQLALCHEMY_DATABASE_URL` in `database.py`.

## Running the App

To run the application, use the command:

```bash
uvicorn main:app --reload


API Endpoints
GET /word/{word_id}: Returns the details of a word, given its ID.
GET /word/{word}/translations: Returns all translations of a specific English word.
GET /category/{category_id}/words: Returns all words from a specific category, given its ID.
GET /translation/{translation_id}: Returns the details of a translation, given its ID.
