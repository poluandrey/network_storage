from src.models.user import User
from src.depends import SessionDep
from src.auth import verify_password


def authenticate_user(session: SessionDep, username: str, password: str) -> User | bool:
    user = session.get(User, {'username': username})

    if not user:
        return False

    if not verify_password(password, user.userpassword):
        return False

    return user
