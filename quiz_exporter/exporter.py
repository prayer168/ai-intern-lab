from openpyxl import Workbook

HEADERS = ["題號", "題目", "選項A", "選項B", "選項C", "選項D", "答案"]


def export_to_excel(questions, out_path):
    """把題目清單匯出成 Excel，第一列是標題。"""
    wb = Workbook()
    ws = wb.active
    ws.title = "題庫"
    ws.append(HEADERS)

    for i, q in enumerate(questions, start=1):
        options = list(q.get("options", [])) + [""] * 4
        row = i + 1
        ws.cell(row=row, column=1, value=i)
        ws.cell(row=row, column=2, value=q["question"])
        for col, opt in enumerate(options[:4], start=3):
            ws.cell(row=row, column=col, value=opt)
        ans = q.get("answer", "")
        ws.cell(row=row, column=7, value=ans.upper() if isinstance(ans, str) else ans)

    wb.save(out_path)
    return out_path
