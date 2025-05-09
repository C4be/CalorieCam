from fastapi import FastAPI
from app.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NeuralNetworkService")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/nn")


@app.get("/")
def get_root():
    return f"Hello, from {app.title}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
