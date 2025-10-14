from typing import List, Optional 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID  

from modules.posts.dto.postDto import * 
from modules.posts.entities.postEntity import PostEntity

import logging, uuid

class PostRepository: 

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__) 

    async def create_post(self,
        session: AsyncSession,
        body: CreatePostDto
    ) -> Optional[UUID]: 
        
        try: 
            
            entity = PostEntity(id=uuid.uuid4(),
                                name = body.Name,
                                tags = body.Tags,
                                owner_id = body.Owner,
                                image = body.Image) 
            session.add(entity)
            await session.commit()
            await session.refresh(entity) 

            return True 
        
        except SQLAlchemyError as sqle: 
            await self.logger.error(f"SQL Error: {sqle}")  
            session.rollback()
            return False 

        except Exception as e:
            self.logger.error(f"Error: {e}") 
            await session.rollback()
            return False 
        
    async def delete_post(self,
        session: AsyncSession,
        postId: UUID
    ) -> Optional[bool]: 
        
        entity = await session.get(PostEntity, id)

        if entity is None:
            return False

        try:
            await session.delete(entity)
            await session.flush()
            self.logger.info("post deleted successfully: %s", id)
            return True
        
        except SQLAlchemyError as e:
            self.logger.error("Failed to delete post: %s", e, exc_info=True)
            await session.rollback()
            return False 
        
    async def get_post_by_id(self,
        session: AsyncSession,
        postId: UUID
    ) -> Optional[PostDto]: 
        
        entity = await session.get(PostEntity, id) 
        
        if entity is None:
            return False

        try:
            await session.delete(entity)
            await session.flush()
            self.logger.info("Post get successfully: %s", id)
            return True
        
        except SQLAlchemyError as e:
            self.logger.error("Failed to get post: %s", e, exc_info=True)
            await session.rollback()
            return False  
        
    