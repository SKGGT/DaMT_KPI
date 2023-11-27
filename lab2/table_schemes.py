from __future__ import annotations
from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy import String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Catalog(Base):
    __tablename__ = "Catalog"

    CatalogID: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String)
    Description: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"Catalog(ID={self.CatalogID!r}, Name={self.Name!r}, Description={self.Description!r})"

    def __init__(self, name, description, **kw: any):
        super().__init__(**kw)
        self.Name = name
        self.Description = description


class Author_Article(Base):
    __tablename__ = "Author_Article"

    Article_ArticleID: Mapped[int] = mapped_column(ForeignKey("Article.ArticleID"), primary_key=True)
    Author_AuthorID: Mapped[int] = mapped_column(ForeignKey("Author.AuthorID"), primary_key=True)

    Article: Mapped["Article"] = relationship(back_populates="Authors")
    Author: Mapped["Author"] = relationship(back_populates="Articles")

    def __init__(self, article_ArticleID, author_AuthorID, **kw: any):
        super().__init__(**kw)
        self.Article_ArticleID = article_ArticleID
        self.Author_AuthorID = author_AuthorID


class Article(Base):
    __tablename__ = "Article"

    ArticleID: Mapped[int] = mapped_column(primary_key=True)
    CatalogID: Mapped[int] = mapped_column(ForeignKey("Catalog.CatalogID"))
    Title: Mapped[str] = mapped_column(String)
    PublicationDate: Mapped[Date] = mapped_column(Date)
    Content: Mapped[str] = mapped_column(String)

    Authors: Mapped[List["Author_Article"]] = relationship(back_populates="Article")

    def __repr__(self):
        return f"Article(ID={self.ArticleID!r}, CatalogID={self.CatalogID!r}, Title={self.Title!r}, Publication Date={self.PublicationDate!r}, Content={self.Content!r})"

    def __init__(self, catalogID, title, publicationDate, content, **kw: any):
        super().__init__(**kw)
        self.CatalogID = catalogID
        self.Title = title
        self.PublicationDate = publicationDate
        self.Content = content


class Author(Base):
    __tablename__ = "Author"

    AuthorID: Mapped[int] = mapped_column(primary_key=True)
    FirstName: Mapped[str] = mapped_column(String)
    LastName: Mapped[str] = mapped_column(String)
    Email: Mapped[str] = mapped_column(String)

    Articles: Mapped[List["Author_Article"]] = relationship(back_populates="Author")

    def __repr__(self):
        return f"Author(ID={self.AuthorID!r}, FirstName={self.FirstName!r}, LastName={self.LastName!r}, Email={self.Email!r})"

    def __init__(self, firstName, lastName, email, **kw: any):
        super().__init__(**kw)
        self.FirstName = firstName
        self.LastName = lastName
        self.Email = email


class Comment(Base):
    __tablename__ = "Comment"

    CommentID: Mapped[int] = mapped_column(primary_key=True)
    ArticleID: Mapped[int] = mapped_column(ForeignKey("Article.ArticleID"))
    AuthorID: Mapped[int] = mapped_column(ForeignKey("Author.AuthorID"))
    Text: Mapped[str] = mapped_column(String)
    Timestamp: Mapped[Date] = mapped_column(Date)

    def __repr__(self):
        return f"Comment(ID={self.CommentID!r}, ArticleID={self.ArticleID!r}, AuthorID={self.AuthorID!r}, Text={self.Text!r}, Timestamp={self.Timestamp!r})"

    def __init__(self, articleID, authorID, text, timestamp, **kw: any):
        super().__init__(**kw)
        self.ArticleID = articleID
        self.AuthorID = authorID
        self.Text = text
        self.Timestamp = timestamp
