import json

import pytest

from quiz_exporter import load_questions


def test_load_sample(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(json.dumps({"questions": [{"question": "1+1?", "answer": "2"}]}), encoding="utf-8")
    assert load_questions(p) == [{"question": "1+1?", "answer": "2"}]


def test_missing_answer_raises(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(json.dumps({"questions": [{"question": "沒有答案"}]}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_questions(p)
