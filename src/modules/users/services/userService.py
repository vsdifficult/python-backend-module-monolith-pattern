from src.modules.users.repository.userRepository import UserRepository
from src.modules.users.repository.chatRepository import ChatRepository
from src.modules.users.dto.userDto import UserDto
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
import logging


class UserService:
    """User Service"""

    def __init__(self,
        logger: logging.Logger, 
        user_repo: UserRepository,
        chat_repo: ChatRepository):

        self._logger = logger
        self._user_repo = user_repo
        self._chat_repo = chat_repo


    async def get_user_by_id(self, session: AsyncSession, user_id: UUID) -> Optional[UserDto]:
        """Get user by id"""
        user = await self._user_repo.get_by_id(session, user_id)
        if user:
            return UserDto.from_orm(user)
        return None

    async def update_user(
        self, session: AsyncSession, user_id: UUID, data: dict
    ) -> Optional[UserDto]:
        """Update user"""
        user = await self._user_repo.update_user(session, user_id, data)
        if user:
            return UserDto.from_orm(user)
        return None

    async def delete_user(self, session: AsyncSession, user_id: UUID) -> bool:
        """Delete user"""
        return await self._user_repo.delete_user(session, user_id)

    async def create_chat(self, 
        session: AsyncSession, 
        title: str,
        senderId: UUID, 
        recipient_id: UUID
    ) -> Optional[UUID]: 
    
        try: 
            chat_entity = await self._chat_repo.create_chat(session, 
                                                            title, 
                                                            senderId, 
                                                            recipient_id) 
            if chat_entity is None: 
                self._logger.error("Error create chat") 
                return None 
            self._logger.info(f"Create chat: {chat_entity.id}")
            return chat_entity.id 
        except Exception as e: 
            self._logger.error(f"Error: {e}") 
            return None  
        
    async def send_message(self,
        session: AsyncSession,
        chatId: UUID,
        senderId: UUID,
        content: str
    ) -> Optional[UUID]: 
        
        try: 
            message_entity = await self._chat_repo.add_message(session, 
                                                               chatId, 
                                                               senderId, 
                                                               content) 
            if message_entity is None: 
                self._logger.error(f"Error create message in chat {message_entity.chat_id}") 
                return None 
            self._logger.info(f"Successfull create message in chat {message_entity.chat_id}")  
            return message_entity 
        
        except Exception as e: 
            self._logger.error(f"Error: {e}") 
            return None  

    async def delete_message(self,
        session: AsyncSession,
        messageId: UUID,
    ) -> Optional[bool]: 
        
        try: 
            await self._chat_repo.delete_message(session, messageId)  
            self._logger.info(f"Message {messageId} deleted")
            return True 
        except Exception as e: 
            self._logger.error(f"Error: {e}") 
            return None  

            