import csv

from quiz_exporter import export_to_csv, load_questions
from quiz_exporter.__main__ import main


def _read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f))


def test_csv_has_header_row(tmp_path):
    out = tmp_path / "out.csv"
    export_to_csv(load_questions("data/sample_quiz.json"), out)
    rows = _read_rows(out)
    assert rows[0] == ["題號", "題目", "選項A", "選項B", "選項C", "選項D", "答案"]


def test_csv_first_question_content(tmp_path):
    out = tmp_path / "out.csv"
    questions = load_questions("data/sample_quiz.json")
    export_to_csv(questions, out)
    rows = _read_rows(out)
    assert len(rows) == len(questions) + 1
    assert rows[1] == ["1", questions[0]["question"], *questions[0]["options"], questions[0]["answer"]]


def test_csv_is_utf8_with_bom(tmp_path):
    out = tmp_path / "out.csv"
    export_to_csv(load_questions("data/sample_quiz.json"), out)
    assert out.read_bytes().startswith(b"\xef\xbb\xbf")


def test_csv_lowercase_answer_unified_to_uppercase(tmp_path):
    out = tmp_path / "out.csv"
    export_to_csv([{"question": "題目一", "options": ["A", "B"], "answer": "c"}], out)
    assert _read_rows(out)[1] == ["1", "題目一", "A", "B", "", "", "C"]


def test_cli_picks_csv_by_extension(tmp_path):
    out = tmp_path / "out.csv"
    assert main(["data/sample_quiz.json", str(out)]) == 0
    assert out.read_bytes().startswith(b"\xef\xbb\xbf")
