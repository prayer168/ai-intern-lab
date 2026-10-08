import sys

from . import export_to_csv, export_to_excel, load_questions


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 2:
        print("用法：python -m quiz_exporter <題庫.json> <輸出.xlsx|輸出.csv>")
        return 1
    questions = load_questions(argv[0])
    if argv[1].lower().endswith(".csv"):
        export_to_csv(questions, argv[1])
    else:
        export_to_excel(questions, argv[1])
    print(f"已匯出 {len(questions)} 題到 {argv[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
