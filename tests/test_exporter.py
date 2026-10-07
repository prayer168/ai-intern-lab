from openpyxl import load_workbook

from quiz_exporter import export_to_excel, load_questions


def test_export_creates_file_with_headers(tmp_path):
    out = tmp_path / "out.xlsx"
    export_to_excel(load_questions("data/sample_quiz.json"), out)
    ws = load_workbook(out).active
    assert ws.title == "題庫"
    assert ws.cell(row=1, column=1).value == "題號"
    assert ws.cell(row=1, column=7).value == "答案"


def test_export_contains_all_questions(tmp_path):
    out = tmp_path / "out.xlsx"
    questions = load_questions("data/sample_quiz.json")
    export_to_excel(questions, out)
    ws = load_workbook(out).active
    texts = [c.value for c in ws["B"] if c.value]
    for q in questions:
        assert q["question"] in texts


def test_export_first_question_on_row_2(tmp_path):
    out = tmp_path / "out.xlsx"
    questions = load_questions("data/sample_quiz.json")
    export_to_excel(questions, out)
    ws = load_workbook(out).active
    assert ws.cell(row=2, column=1).value == 1
    assert ws.cell(row=2, column=2).value == questions[0]["question"]


def test_export_lowercase_answer_unified_to_uppercase(tmp_path):
    out = tmp_path / "out.xlsx"
    questions = [{"question": "題目一", "options": ["A", "B", "C", "D"], "answer": "c"}]
    export_to_excel(questions, out)
    ws = load_workbook(out).active
    assert ws.cell(row=2, column=7).value == "C"


def test_export_fewer_options_pads_empty_cells(tmp_path):
    import json

    p = tmp_path / "q.json"
    p.write_text(
        json.dumps({"questions": [{"question": "Short", "options": ["One", "Two"], "answer": "A"}]}),
        encoding="utf-8",
    )
    out = tmp_path / "out.xlsx"
    export_to_excel(load_questions(p), out)
    ws = load_workbook(out).active
    assert [ws.cell(row=2, column=c).value for c in range(3, 7)] == ["One", "Two", None, None]
