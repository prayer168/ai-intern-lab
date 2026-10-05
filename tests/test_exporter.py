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
