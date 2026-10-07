import json

import pytest

from quiz_exporter import load_questions


def test_load_sample(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(json.dumps({"questions": [{"question": "1+1?", "answer": "A"}]}), encoding="utf-8")
    assert load_questions(p) == [{"question": "1+1?", "answer": "A"}]


def test_missing_answer_raises(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(json.dumps({"questions": [{"question": "沒有答案"}]}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_questions(p)


def test_invalid_answer_raises(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [{"question": "水在幾度會沸騰？", "answer": "E"}]}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="第 1 題"):
        load_questions(p)


def test_invalid_answer_second_question_raises(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps(
            {
                "questions": [
                    {"question": "第一題", "answer": "A"},
                    {"question": "第二題", "answer": "X"},
                ]
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="第 2 題"):
        load_questions(p)


def test_lowercase_answer_accepted_and_uppercased(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [{"question": "光合作用", "answer": "b"}]}),
        encoding="utf-8",
    )
    questions = load_questions(p)
    assert questions[0]["answer"] == "B"
