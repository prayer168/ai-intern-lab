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


@pytest.mark.parametrize("option_count", [5, 6])
def test_excess_options_raise_with_question_number_and_count(tmp_path, option_count):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [
            {"question": "First", "options": ["A", "B"], "answer": "A"},
            {"question": "Second", "options": [str(i) for i in range(option_count)], "answer": "A"},
        ]}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=f"第 2 題.*{option_count} 個選項"):
        load_questions(p)


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_question_raises_with_question_number(tmp_path, blank):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [
            {"question": "第一題", "answer": "A"},
            {"question": blank, "options": ["甲", "乙", "丙", "丁"], "answer": "A"},
        ]}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="第 2 題的題目是空白的"):
        load_questions(p)


def test_question_whitespace_is_stripped(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [{"question": "  水在幾度會沸騰？ ", "answer": "A"}]}),
        encoding="utf-8",
    )
    assert load_questions(p)[0]["question"] == "水在幾度會沸騰？"


def test_utf8_bom_file_is_accepted(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [{"question": "水在幾度會沸騰？", "answer": "C"}]}, ensure_ascii=False),
        encoding="utf-8-sig",
    )
    assert load_questions(p) == [{"question": "水在幾度會沸騰？", "answer": "C"}]


@pytest.mark.parametrize("options", [["甲", "乙", "甲", "丁"], ["甲", " 甲 "]])
def test_duplicate_options_raise_with_question_number(tmp_path, options):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [
            {"question": "第一題", "options": ["甲", "乙"], "answer": "A"},
            {"question": "第二題", "options": options, "answer": "A"},
        ]}, ensure_ascii=False),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="第 2 題有重複的選項：甲"):
        load_questions(p)


@pytest.mark.parametrize("blank", ["", "   ", None])
def test_blank_option_raises_with_question_and_option_number(tmp_path, blank):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [
            {"question": "第一題", "options": ["甲", "乙"], "answer": "A"},
            {"question": "第二題", "options": ["甲", blank, "丙", "丁"], "answer": "B"},
        ]}, ensure_ascii=False),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="第 2 題的選項B是空白的"):
        load_questions(p)


@pytest.mark.parametrize("options", ["水,火", "甲乙丙丁", {"A": "水"}])
def test_non_list_options_raises_with_question_number(tmp_path, options):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [
            {"question": "第一題", "options": ["甲", "乙"], "answer": "A"},
            {"question": "第二題", "options": options, "answer": "A"},
        ]}, ensure_ascii=False),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="第 2 題的 options 必須是清單"):
        load_questions(p)


@pytest.mark.parametrize("item", [123, None, ["水在幾度會沸騰？", "C"]])
def test_non_object_question_raises_with_question_number(tmp_path, item):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [{"question": "第一題", "answer": "A"}, item]}, ensure_ascii=False),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="第 2 題格式不正確"):
        load_questions(p)


@pytest.mark.parametrize("data", [{"question": [{"question": "打錯欄位名稱", "answer": "A"}]}, {"questions": []}])
def test_no_questions_raises(tmp_path, data):
    p = tmp_path / "q.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="題庫裡沒有任何題目"):
        load_questions(p)


def test_top_level_array_raises_friendly_error(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(json.dumps([{"question": "水在幾度會沸騰？", "answer": "C"}]), encoding="utf-8")
    with pytest.raises(ValueError, match="最外層必須是物件"):
        load_questions(p)


def test_answer_beyond_given_options_raises(tmp_path):
    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [
            {"question": "第一題", "options": ["甲", "乙", "丙", "丁"], "answer": "D"},
            {"question": "第二題", "options": ["對", "錯"], "answer": "D"},
        ]}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="第 2 題答案是 D，但只有 2 個選項"):
        load_questions(p)
