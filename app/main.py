from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth
from app.api import auth, portfolio_routes, history_routes

app = FastAPI()

# Register auth routes
app.include_router(auth.router)
app.include_router(portfolio_routes.router)
app.include_router(history_routes.router)

# Optional: CORS setup (for frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route (required for health check or browser test)
@app.get("/")
def root():
    return {"msg": "StackUp API is running"}

# ✅ Swagger Authorize button with JWT support
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="StackUp Portfolio API",
        version="1.0.0",
        description="API for login, upload, and trend analysis",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for route in app.routes:
        if hasattr(route.endpoint, "openapi_extra"):
            route.openapi_extra.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi