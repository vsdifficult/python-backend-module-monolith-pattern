from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import logging

from modules.posts.repository.postRepository import PostRepository
from modules.posts.dto.postDto import CreatePostDto, PostDto


class PostService:
    def __init__(self, logger: logging.Logger = None):

        self.logger = logger or logging.getLogger(__name__)
        self.post_repository = PostRepository(logger=self.logger)

    async def create_new_post(self, session: AsyncSession, post_data: CreatePostDto) -> bool:

        try:

            self.logger.info(f"Creating a new post: {post_data.Name}")

            success = await self.post_repository.create_post(session, post_data)

            return success

        except Exception as e:
            self.logger.error(f"Error in PostService while creating post: {e}", exc_info=True)

            return False

    async def delete_post_by_id(self, session: AsyncSession, post_id: UUID) -> bool:

        try:

            self.logger.info(f"Deleting post with ID: {post_id}")
            
            return await self.post_repository.delete_post(session, post_id)

        except Exception as e:
            self.logger.error(f"Error in PostService while deleting post: {e}", exc_info=True)

            return False

    async def get_post_by_id(self, session: AsyncSession, post_id: UUID) -> PostDto | None:

        try:

            self.logger.info(f"Fetching post with ID: {post_id}")

            return await self.post_repository.get_post_by_id(session, post_id)

        except Exception as e:
            self.logger.error(f"Error in PostService while fetching post: {e}", exc_info=True)

            return None
