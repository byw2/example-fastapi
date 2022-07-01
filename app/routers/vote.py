from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
import app.schemas as schemas
import app.database as database
import app.models as models
import app.oauth2 as oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

# post request because we are sending some information to the server
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    if db.query(models.Post).filter(vote.post_id == models.Post.id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {vote.post_id} does not exist")
    # check if the vote for current user of post exists
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    # if the vote direction is 1, this means that this user liked a post
    if (vote.dir == 1): 
        print("Vote dir is 1.")
        if found_vote: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        # db.refresh(new_vote)
        return new_vote
    # if the vote direction is 0, this means that this user unliked a post
    elif (vote.dir == 0):
        print("Vote dir is 0.")
        if found_vote is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)


