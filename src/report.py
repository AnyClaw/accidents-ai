"""Сборка единого отчёта: markdown-файл со всеми таблицами."""

import pandas as pd


def df_to_md(df, index=False, max_rows=None):
    """DataFrame -> markdown-таблица. Без внешних зависимостей."""
    if df.empty:
        return "_Таблица пуста._\n"

    data = df.reset_index() if index else df
    truncated = False
    if max_rows is not None and len(data) > max_rows:
        data = data.head(max_rows)
        truncated = True

    headers = [str(c) for c in data.columns]

    def fmt(v):
        if pd.isna(v):
            return "—"
        if isinstance(v, float):
            return f"{v:g}"
        # '|' ломает markdown-таблицу, переносы строк тоже
        return str(v).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in data.iterrows():
        lines.append("| " + " | ".join(fmt(v) for v in row) + " |")

    if truncated:
        lines.append("")
        lines.append(f"_Показаны первые {max_rows} строк из {len(df)}. Полная таблица — в CSV._")

    return "\n".join(lines) + "\n"


class Report:
    """Накапливает разделы и пишет их в один .md файл."""

    def __init__(self, title):
        self.parts = [f"# {title}\n"]

    def text(self, txt):
        self.parts.append(txt.strip() + "\n")

    def section(self, title, level=2):
        self.parts.append(f"\n{'#' * level} {title}\n")

    def table(self, title, df, note=None, index=False, max_rows=None):
        self.section(title, level=3)
        if note:
            self.text(note)
        self.parts.append(df_to_md(df, index=index, max_rows=max_rows))

    def save(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.parts), encoding="utf-8")
        return path