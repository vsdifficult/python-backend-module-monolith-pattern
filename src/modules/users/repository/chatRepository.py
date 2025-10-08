from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from uuid import UUID, uuid4
import logging

from src.modules.users.dto.chatDto import ChatDto, MessageDto
from src.modules.users.entities.chatEntity import Chat, Message

class ChatRepository:
    """
    Production-ready repository for Chats and Messages
    """

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)


    async def create_chat(
        self,
        session: AsyncSession,
        title: str,
        sender_id: UUID,
        recipient_id: UUID
    ) -> Optional[Chat]:
        try:
            chat = Chat(
                id=uuid4(),
                title=title,
                sender_id=sender_id,
                recipient_id=recipient_id
            )
            session.add(chat)
            await session.commit()
            await session.refresh(chat)
            return chat
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Failed to create chat: {e}", exc_info=True)
            return None

    async def get_chat_by_id(
        self,
        session: AsyncSession,
        chat_id: UUID
    ) -> Optional[Chat]:
        try:
            result = await session.execute(select(Chat).where(Chat.id == chat_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to fetch chat {chat_id}: {e}", exc_info=True)
            return None

    async def get_chats_for_user(
        self,
        session: AsyncSession,
        user_id: UUID
    ) -> List[Chat]:
        try:
            result = await session.execute(
                select(Chat).where(
                    (Chat.sender_id == user_id) | (Chat.recipient_id == user_id)
                )
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to fetch chats for user {user_id}: {e}", exc_info=True)
            return []

    async def delete_chat(
        self,
        session: AsyncSession,
        chat_id: UUID
    ) -> bool:
        try:
            result = await session.execute(delete(Chat).where(Chat.id == chat_id))
            await session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Failed to delete chat {chat_id}: {e}", exc_info=True)
            return False

    # ----------------- Messages -----------------

    async def add_message(
        self,
        session: AsyncSession,
        chat_id: UUID,
        sender_id: UUID,
        content: str
    ) -> Optional[Message]:
        try:
            message = Message(
                id=uuid4(),
                chat_id=chat_id,
                sender_id=sender_id,
                content=content
            )
            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Failed to add message to chat {chat_id}: {e}", exc_info=True)
            return None

    async def delete_message(
        self,
        session: AsyncSession,
        message_id: UUID 
    ) -> Optional[bool]: 
        try: 
            entity = await session.execute(
                select(Message).filter(Message.id == message_id)
            )  
            await session.delete(entity)
            await session.flush() 
            return True 
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Failed to delete message {entity.id}: {e}", exc_info=True)
            return False

    async def get_messages(
        self,
        session: AsyncSession,
        chat_id: UUID,
        limit: int = 50
    ) -> List[Message]:
        try:
            result = await session.execute(
                select(Message)
                .where(Message.chat_id == chat_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to fetch messages for chat {chat_id}: {e}", exc_info=True)
            return []