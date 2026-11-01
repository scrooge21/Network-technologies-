from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from routes.users import user_router
from routes.events import event_router
import uvicorn

tags_metadata = [
    {"name": "User", "description": "Регистрация, вход и выход пользователей."},
    {"name": "Events", "description": "Создание, просмотр и удаление событий."},
]

app = FastAPI(
    title="Планировщик событий",
    description=(
        ""
    ),
    openapi_tags=tags_metadata,
    docs_url=None,  # отключаем стандартную страницу, ниже своя
)


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    page = get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title)
    css = "<style>.swagger-ui .info .title small { display: none; }</style>"
    html = page.body.decode().replace("</head>", css + "</head>")
    return HTMLResponse(html)


app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)