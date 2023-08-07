from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import List

import models
from database import SessionLocal

app = FastAPI(debug=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class WordBase(BaseModel):
    word: str


class WordInDB(WordBase):
    id: int
    category_name: str

    class Config:
        orm_mode = True


class TranslationBase(BaseModel):
    language: str
    translation: str


class TranslationInDB(TranslationBase):
    id: int
    word: str
    category_name: str

    class Config:
        orm_mode = True


class TranslationOut(BaseModel):
    language: str
    translation: str

    class Config:
        orm_mode = True


@app.get("/word/{word_id}", tags=['English words'])
def read_word(word_id: int, db: Session = Depends(get_db)):
    #db_word = db.query(models.Word).filter(models.Word.id == word_id).first()
    db_word = db.query(models.Word).options(joinedload(models.Word.category)).filter(models.Word.id == word_id).first()
    if db_word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    return {
        "id": db_word.id,
        "word": db_word.word,
        "category_name": db_word.category.name,
    }


@app.get("/translation/{translation_id}")
def read_translation(translation_id: int, db: Session = Depends(get_db)):
    #db_translation = db.query(models.Translation).filter(models.Translation.id == translation_id).first()
    db_translation = db.query(models.Translation).options(
        joinedload(models.Translation.word).joinedload(models.Word.category)).filter(
        models.Translation.id == translation_id).first()
    if db_translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")

    return {
        "id": db_translation.id,
        "language": db_translation.language,
        "translation": db_translation.translation,
        "word": db_translation.word.word,
        "category_name": db_translation.word.category.name,
    }


@app.get("/category/{category_id}/words", response_model=List[WordInDB])
def read_category_words(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).options(joinedload(models.Category.words)).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    words = []
    for word in db_category.words:
        word_data = {"id": word.id, "word": word.word, "category_name": db_category.name}
        words.append(word_data)
    return words


@app.get("/word/{word}/translations", response_model=List[TranslationOut], tags=['Translations'])
def get_translations(word: str, db: Session = Depends(get_db)):
    db_word = db.query(models.Word).options(joinedload(models.Word.translations)).filter(models.Word.word == word).first()
    if db_word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return db_word.translations
