from sqlalchemy import Integer, Column, String
from database import Base

class DBArticles(Base):
    __tablename__ = "articles"  # SQLのテーブル名

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)