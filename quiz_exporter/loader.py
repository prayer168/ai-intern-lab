import json
from pathlib import Path


VALID_ANSWERS = {"A", "B", "C", "D"}


def load_questions(path):
    """讀取題庫 JSON，回傳題目清單（list of dict）。"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    for i, q in enumerate(questions, start=1):
        if "question" not in q or "answer" not in q:
            raise ValueError(f"第 {i} 題缺少 question 或 answer 欄位")
        ans = q["answer"].strip().upper() if isinstance(q["answer"], str) else None
        if not ans or ans not in VALID_ANSWERS:
            raise ValueError(f"第 {i} 題答案必須是 A–D（目前為 {q['answer']!r}）")
        q["answer"] = ans
    return questions
