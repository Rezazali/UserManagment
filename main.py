from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username: str


class FollowBase(BaseModel):
    follower_id: int
    followee_id: int


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Depends(get_db)


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = db_dependency):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.put("/follow/", status_code=status.HTTP_200_OK)
async def follow_user(follow: FollowBase, db: Session = db_dependency):
    follower = db.query(models.User).filter(models.User.id == follow.follower_id).first()
    print(follower)
    followee = db.query(models.User).filter(models.User.id == follow.followee_id).first()
    print(followee)
    if not follower or not followee:
        raise HTTPException(status_code=404, detail="User not found")
    follower.following.append(followee)
    db.commit()
    return {"message": "Successfully followed"}


@app.delete("/unfollow/", status_code=status.HTTP_200_OK)
async def unfollow_user(follow: FollowBase, db: Session = db_dependency):
    follower = db.query(models.User).filter(models.User.id == follow.follower_id).first()
    followee = db.query(models.User).filter(models.User.id == follow.followee_id).first()
    if not follower or not followee:
        raise HTTPException(status_code=404, detail="User not found")
    follower.following.remove(followee)
    db.commit()
    return {"message": "Successfully unfollowed"}


@app.get("/followers/{user_id}")
async def get_followers(user_id: int, db: Session = db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"followers": [follower.username for follower in user.followers]}


@app.get("/common-followers/{user1_id}/{user2_id}")
async def get_common_followers(user1_id: int, user2_id: int, db: Session = db_dependency):
    user1 = db.query(models.User).filter(models.User.id == user1_id).first()
    user2 = db.query(models.User).filter(models.User.id == user2_id).first()
    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="User not found")
    common_followers = set(user1.followers).intersection(user2.followers)
    return {"common_followers": [follower.username for follower in common_followers]}
