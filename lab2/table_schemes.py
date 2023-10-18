Catalog: str = '''CREATE TABLE IF NOT EXISTS "Catalog" (
                "CatalogID" SERIAL PRIMARY KEY,
                "Name" varchar NOT NULL,
                "Description" varchar NOT NULL
            )'''

Article: str = '''CREATE TABLE IF NOT EXISTS "Article" (
                "ArticleID" SERIAL PRIMARY KEY,
                "CatalogID" integer REFERENCES "Catalog" ("CatalogID"),
                "Title" varchar NOT NULL,
                "Publication Date" DATE NOT NULL,
                "Content" varchar NOT NULL
            )'''

Author: str = '''CREATE TABLE IF NOT EXISTS "Author" (
                "AuthorID" SERIAL PRIMARY KEY,
                "First Name" varchar NOT NULL,
                "Last Name" varchar NOT NULL,
                "Email" varchar NOT NULL
            )'''

Author_Article: str = '''CREATE TABLE IF NOT EXISTS "Author_Article" (
                "Article_ArticleID" integer REFERENCES "Article" ("ArticleID"),
                "Author_AuthorID" integer REFERENCES "Author" ("AuthorID")
            )'''

Comment: str = '''CREATE TABLE IF NOT EXISTS "Comment" (
                "CommentID" SERIAL PRIMARY KEY,
                "ArticleID" integer REFERENCES "Article" ("ArticleID"),
                "AuthorID" integer REFERENCES "Author" ("AuthorID"),
                "Text" varchar NOT NULL,
                "Timestamp" DATE NOT NULL
            )'''