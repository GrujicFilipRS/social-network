from datetime import datetime, timezone

from sqlalchemy.orm import Session

from uuid import UUID

from models import User
from models.users import UserOptions
from schemas import UserGetResponse, DTO

from ..service_models import UserServiceModel


class UserServiceSqlal(UserServiceModel):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    async def get_user(self, id: UUID) -> UserGetResponse:
        user = self.db_session.get(User, id)
        return UserGetResponse.ok(user) if user else UserGetResponse.error('User not found')
    
    async def get_user_by_username(self, username: str) -> UserGetResponse:
        user = self.db_session.query(User).filter_by(username=username).first()
        return UserGetResponse.ok(user) if user else UserGetResponse.error('User not found') 
    
    async def register(self, username: str, password: str, name: str | None) -> UserGetResponse:
        user_exists = self.db_session.query(User).filter_by(username=username).first() is not None
        
        if user_exists:
            return UserGetResponse.error('User with such username already exists')
        
        user = User(
            username = username,
            name = name,
            last_username_edit = datetime.now(timezone.utc),
            created_at = datetime.now(timezone.utc)
        )
        
        user.set_password(password)
        
        self.db_session.add(user)
        self.db_session.commit()
        
        return UserGetResponse.ok(user)

    async def log_in(self, username: str, password: str) -> UserGetResponse:
        user = self.db_session.query(User).filter_by(username=username).first()
        if not user:
            return UserGetResponse.error('Invalid credentials')

        if not user.check_password(password):
            return UserGetResponse.error('Invalid credentials')
        
        return UserGetResponse.ok(user)
    
    async def set_name(self, id: UUID, name: str) -> DTO:
        user = self.db_session.get(User, id)
        if not user:
            return DTO.error('User not found')
        
        user.set_name(name)
        self.db_session.add(user)
        self.db_session.commit()
        
        return DTO.ok()
    
    async def change_username(self, id: UUID, username: str) -> DTO:
        user = self.db_session.get(User, id)
        if not user:
            return DTO.error('User not found')
        
        if user.username == username:
            return DTO.error('That action did not change the username')
        
        exists = self.db_session.query(User).filter_by(username=username).first() is not None
        if exists:
            return DTO.error('That username is already taken')
        
        able_to_change = user.able_to_change_username()
        
        if not able_to_change:
            return DTO.error(
                f'You can only update your username once every {UserOptions.USERNAME_UPDATE_LIMIT_HOURS} hours'
            )
        
        user.username = username
        self.db_session.add(user)
        self.db_session.commit()
        
        return DTO.ok()
    
    async def change_password(self, id: UUID, old_password: str, new_password: str) -> DTO:
        user = self.db_session.get(User, id)
        if not user:
            return DTO.error('User not found')
        
        if not user.check_password(old_password):
            return DTO.error('Credentials incorrect')
        
        user.set_password(new_password)
        self.db_session.add(user)
        self.db_session.commit()
        
        return DTO.ok()