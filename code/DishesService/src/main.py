from fastapi import FastAPI
from app.endpoints import router
from app.database_postgres import Base, engine
from app.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DishesService")

Base.metadata.create_all(bind=engine)
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Updated CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://0.0.0.0", "http://127.0.0.1", "http://frontend:3000"],  # Explicitly allow your frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],  # Explicitly list allowed methods
#     allow_headers=["*"],
#     expose_headers=["*"],
#     max_age=600,  # Cache preflight requests for 10 minutes
# )

app.include_router(router=router, prefix='/dish')

@app.get('/')
def get_root():
    return f'Hello, from {app.title}'


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)