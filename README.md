# ai-intern-lab｜免費 AI 打工仔練習場

YouTube 系列《免費 AI 打工仔》的共用練習專案。
同一個小專案，交給不同的 AI Coding 工具（Jules、Antigravity、Copilot、Codex、Claude Code、OpenHands）處理，比較誰做得好。

## 這個專案做什麼
把題庫 JSON 匯出成 Excel 題目表。

```bash
pip install -r requirements.txt
python -m quiz_exporter data/sample_quiz.json out.xlsx
python -m pytest -q
```

## 給 AI 的規則
請看 [AGENTS.md](AGENTS.md)。

## 注意
這個專案**故意留了 bug**，用來測試 AI 能不能找到並修好。測試目前會通過，不代表程式沒問題。
