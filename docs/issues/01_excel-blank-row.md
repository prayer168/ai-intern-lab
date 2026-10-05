# Issue 草稿 01（EP2 拍攝時才建立，請勿提前開）

**標題：** 匯出 Excel 時，第一題前面多一列空白

**內容：**
執行 `python -m quiz_exporter data/sample_quiz.json out.xlsx` 後打開 Excel：

- 第 1 列是標題（正常）
- 第 2 列是空白（不正常）
- 第 3 列才是第一題

期望：第一題應該在第 2 列，緊接在標題下面。

請：
1. 先補一個能抓到這個問題的測試
2. 修正程式
3. 確認 `python -m pytest -q` 全部通過
4. 開 PR，不要直接合併
