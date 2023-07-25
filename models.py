from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="words")


Category.words = relationship("Word", order_by=Word.id, back_populates="category")


class Translation(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    language = Column(String)
    translation = Column(String)

    word = relationship("Word", back_populates="translations")


Word.translations = relationship("Translation", order_by=Translation.id, back_populates="word")
