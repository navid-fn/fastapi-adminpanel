from sqlmodel import Session, select

from app.models import Post
from app.models.posts import PostCreate, PostUpdate


def create_post(session: Session, post_create: PostCreate) -> Post:
    post_db = Post.model_validate(post_create)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db


def update_post(session: Session, post_id: int, post_update: PostUpdate):
    post_db = session.get(Post, post_id)
    if not post_db:
        return None
    update_data = post_update.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(update_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db


def get_post_by_owner(session: Session, user_id: int):
    return session.exec(select(Post).where(Post.owner_id == user_id)).all()
