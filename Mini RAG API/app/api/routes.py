from fastapi import APIRouter, UploadFile, HTTPException, File
from app.core.rag_chain import build_rag, ragchain
from app.schema.request import AskQuestion
from app.schema.response import GiveResponse
import os

router = APIRouter()

UPLOAD_DIR = "upload"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/")
def home_page():
    return {"message": "welcome to our Mini RAG API application"}


@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    build_rag(file_path)

    return {"message": "Doc processed successfully"}


@router.post("/ask", response_model=GiveResponse)
def ask_question(data: AskQuestion):
    if ragchain is None:
        raise HTTPException(
            status_code=400,
            detail="No document uploaded yet"
        )

    try:
        answer = ragchain.invoke(data.question)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
