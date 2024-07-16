from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

association_table = Table('followers', Base.metadata,
                          Column('follower_id', Integer, ForeignKey('users.id')),
                          Column('followee_id', Integer, ForeignKey('users.id'))
                          )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

    following = relationship(
        "User",
        secondary=association_table,
        primaryjoin=id == association_table.c.follower_id,
        secondaryjoin=id == association_table.c.followee_id,
        backref="followers"
    )


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref="posts")

