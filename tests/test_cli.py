import json

import pytest

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


def test_input_is_directory_prints_friendly_message(tmp_path, capsys):
    out = tmp_path / "out.xlsx"
    assert main([str(tmp_path), str(out)]) == 1
    captured = capsys.readouterr()
    assert captured.out.strip() == f"題庫路徑是資料夾，不是檔案：{tmp_path}"
    assert "Traceback" not in captured.out + captured.err
    assert not out.exists()


def test_big5_file_prints_friendly_encoding_message(tmp_path, capsys):
    bad = tmp_path / "big5.json"
    bad.write_bytes(
        json.dumps({"questions": [{"question": "水在幾度會沸騰？", "answer": "C"}]}, ensure_ascii=False).encode("cp950")
    )
    out = tmp_path / "out.xlsx"
    assert main([str(bad), str(out)]) == 1
    captured = capsys.readouterr()
    assert captured.out.strip().startswith(f"題庫檔不是 UTF-8 編碼：{bad}")
    assert "codec" not in captured.out
    assert not out.exists()


@pytest.mark.parametrize("name", ["out.xls", "out.txt", "out"])
def test_unsupported_output_extension_prints_friendly_message(tmp_path, capsys, name):
    out = tmp_path / name
    assert main(["data/sample_quiz.json", str(out)]) == 1
    captured = capsys.readouterr()
    assert captured.out.strip() == f"輸出檔名必須是 .xlsx 或 .csv 結尾：{out}"
    assert not out.exists()


def test_uppercase_xlsx_extension_still_accepted(tmp_path):
    out = tmp_path / "OUT.XLSX"
    assert main(["data/sample_quiz.json", str(out)]) == 0
    assert out.exists()


def test_missing_output_folder_prints_friendly_message(tmp_path, capsys):
    out = tmp_path / "no_such_folder" / "out.xlsx"
    assert main(["data/sample_quiz.json", str(out)]) == 1
    captured = capsys.readouterr()
    assert captured.out.strip().startswith(f"無法寫入輸出檔：{out}")
    assert "Traceback" not in captured.out + captured.err


def test_output_file_locked_prints_friendly_message(tmp_path, capsys, monkeypatch):
    import quiz_exporter.__main__ as cli

    def locked(questions, out_path):
        raise PermissionError(13, "Permission denied", str(out_path))

    monkeypatch.setattr(cli, "export_to_excel", locked)
    out = tmp_path / "out.xlsx"
    assert main(["data/sample_quiz.json", str(out)]) == 1
    captured = capsys.readouterr()
    assert captured.out.strip().startswith(f"無法寫入輸出檔：{out}")
    assert "Traceback" not in captured.out + captured.err


def test_top_level_array_prints_friendly_message(tmp_path, capsys):
    bad = tmp_path / "list.json"
    bad.write_text(json.dumps([{"question": "水在幾度會沸騰？", "answer": "C"}]), encoding="utf-8")
    out = tmp_path / "out.xlsx"
    assert main([str(bad), str(out)]) == 1
    captured = capsys.readouterr()
    assert "最外層必須是物件" in captured.out
    assert "Traceback" not in captured.out + captured.err
    assert not out.exists()
