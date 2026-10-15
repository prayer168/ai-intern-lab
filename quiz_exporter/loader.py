import json
from pathlib import Path


VALID_ANSWERS = {"A", "B", "C", "D"}


def load_questions(path):
    """讀取題庫 JSON，回傳題目清單（list of dict）。"""
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError('題庫檔最外層必須是物件，例如 {"questions": [...]}')
    questions = data.get("questions", [])
    if not questions:
        raise ValueError('題庫裡沒有任何題目，請確認有 "questions" 清單且至少一題')
    for i, q in enumerate(questions, start=1):
        if not isinstance(q, dict):
            raise ValueError(f'第 {i} 題格式不正確，每一題都要寫成 {{"question": ..., "answer": ...}}')
        if "question" not in q or "answer" not in q:
            raise ValueError(f"第 {i} 題缺少 question 或 answer 欄位")
        opts = q.get("options", [])
        for letter, opt in zip("ABCD", opts if isinstance(opts, list) else []):
            if isinstance(opt, bool) or not isinstance(opt, (str, int, float, type(None))):
                raise ValueError(f"第 {i} 題的選項{letter}必須是文字或數字")
        text = q["question"].strip() if isinstance(q["question"], str) else ""
        if not text:
            raise ValueError(f"第 {i} 題的題目是空白的")
        q["question"] = text
        opts = q.get("options", [])
        if isinstance(opts, list):
            seen = []
            for opt in opts:
                key = opt.strip() if isinstance(opt, str) else opt
                if key in seen and key not in ("", None):
                    raise ValueError(f"第 {i} 題有重複的選項：{key}")
                seen.append(key)
        ans = q["answer"].strip().upper() if isinstance(q["answer"], str) else None
        if not ans or ans not in VALID_ANSWERS:
            raise ValueError(f"第 {i} 題答案必須是 A–D（目前為 {q['answer']!r}）")
        if not isinstance(q.get("options", []), list):
            raise ValueError(f'第 {i} 題的 options 必須是清單，例如 ["甲", "乙", "丙", "丁"]')
        option_count = len(q.get("options", []))
        if isinstance(q.get("options"), list):
            q["options"] = [o.strip() if isinstance(o, str) else o for o in q["options"]]
        if option_count > 4:
            raise ValueError(f"第 {i} 題有 {option_count} 個選項，最多允許 4 個選項")
        if option_count and "ABCD".index(ans) >= option_count:
            raise ValueError(f"第 {i} 題答案是 {ans}，但只有 {option_count} 個選項")
        q["answer"] = ans
        for letter, opt in zip("ABCD", q.get("options", [])):
            if opt is None or (isinstance(opt, str) and not opt.strip()):
                raise ValueError(f"第 {i} 題的選項{letter}是空白的")
    return questions
