from fastapi import APIRouter

from src.modules.auth.controller import router as auth_router
from src.modules.group.controller import router as group_router
from src.modules.tag.controller import router as tag_router
from src.modules.title.controller import router as title_router
from src.modules.user.controller import router as user_router

router = APIRouter()

router.include_router(auth_router)
# Auth should always be first

router.include_router(user_router)
router.include_router(title_router)
router.include_router(tag_router)
router.include_router(group_router)
