import json

from quiz_exporter.__main__ import main


def test_missing_file_prints_friendly_message(tmp_path, capsys):
    missing = tmp_path / "sampel_quiz.json"
    assert main([str(missing), str(tmp_path / "out.xlsx")]) == 1
    captured = capsys.readouterr()
    assert captured.out.strip() == f"找不到題庫檔：{missing}"
    assert "Traceback" not in captured.out + captured.err


def test_invalid_json_prints_friendly_message(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text('{"questions": [', encoding="utf-8")
    assert main([str(bad), str(tmp_path / "out.xlsx")]) == 1
    captured = capsys.readouterr()
    assert captured.out.strip() == f"題庫檔不是正確的 JSON：{bad}"
    assert "Traceback" not in captured.out + captured.err


def test_invalid_question_prints_loader_message(tmp_path, capsys):
    bad = tmp_path / "q.json"
    bad.write_text(
        json.dumps({"questions": [{"question": "水在幾度會沸騰？", "answer": "E"}]}),
        encoding="utf-8",
    )
    out = tmp_path / "out.xlsx"
    assert main([str(bad), str(out)]) == 1
    captured = capsys.readouterr()
    assert captured.out.strip().startswith("第 1 題答案必須是 A–D")
    assert "Traceback" not in captured.out + captured.err
    assert not out.exists()
