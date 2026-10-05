# AGENTS.md — 給所有 AI 打工仔的工作守則

這份檔案寫給 Jules、Antigravity、Copilot、Codex、Claude Code、OpenHands 等 AI 開發助手。
（Antigravity CLI 也會讀 GEMINI.md，內容與本檔相同，以本檔為準。）

## 專案在做什麼
把題庫 JSON（`data/*.json`）匯出成 Excel。程式在 `quiz_exporter/`，測試在 `tests/`。

## 怎麼跑
```bash
pip install -r requirements.txt
python -m pytest -q
python -m quiz_exporter data/sample_quiz.json out.xlsx
```

## 工作規則
1. **一個任務一個分支**，分支名稱用 `ai/<工具名>/<簡短描述>`，例如 `ai/jules/fix-blank-row`。
2. **不准直接推到 `main`，也不准自己 merge。** 一律開 Pull Request，等人工審核。
3. **改完一定要跑 `python -m pytest -q`**，修 bug 時要先補一個會失敗的測試，再修到通過。
4. PR 說明要寫：改了什麼、為什麼、怎麼驗證。
5. 只改任務需要的檔案，不要順手重構或改格式。

## 絕對不要做
- 不要提交任何密碼、API Key、Token、`.env` 檔。
- 不要修改 `.github/workflows/`、`AGENTS.md`、`GEMINI.md`、`LICENSE`。
- 不要刪除 `data/sample_quiz.json` 或任何既有測試。
- 不要新增需要付費服務或外部網路的相依套件。
