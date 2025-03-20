from fastapi import FastAPI, HTTPException, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Orígenes permitidos


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)



from app.routes import problem1, problem2, problem3, problem4

# Agregar todas las rutas
app.include_router(problem1.router, prefix="/api")
app.include_router(problem2.router, prefix="/api")
app.include_router(problem3.router, prefix="/api")
app.include_router(problem4.router, prefix="/api")




@app.get("/")
def home():
    return {"message": "API funcionando correctamente 🚀"}


