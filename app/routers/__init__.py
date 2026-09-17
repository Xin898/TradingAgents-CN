"""
Routers package: expose API routers.

The platform integration router is composed into the API root router here so
app.main can keep its existing /api mount while downstream contracts remain
isolated in the platform_integration package.
"""

from app.routers import health
from platform_integration.router import router as platform_integration_router

health.router.include_router(platform_integration_router)
