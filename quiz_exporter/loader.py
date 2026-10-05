import json
from pathlib import Path


def load_questions(path):
    """讀取題庫 JSON，回傳題目清單（list of dict）。"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    for i, q in enumerate(questions, start=1):
        if "question" not in q or "answer" not in q:
            raise ValueError(f"第 {i} 題缺少 question 或 answer 欄位")
    return questions
