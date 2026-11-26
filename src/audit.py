"""Первичный аудит датасета. Только расчёты, без ввода-вывода."""

import numpy as np
import pandas as pd


def load_data(path, nrows=None):
    return pd.read_csv(path, nrows=nrows, na_values=["nan", "NaN", ""], skipinitialspace=True)


def overview(df):
    items = [
        ("Количество строк", len(df)),
        ("Количество столбцов", df.shape[1]),
        ("Объём в памяти, МБ", round(df.memory_usage(deep=True).sum() / 1024**2, 1)),
        ("Полных дубликатов строк", int(df.duplicated().sum())),
        ("Дубликатов без учёта ID",
         int(df.drop(columns=["ID"], errors="ignore").duplicated().sum())),
        ("Всего пропущенных значений", int(df.isna().sum().sum())),
        ("Доля пропусков во всём датасете, %",
         round(df.isna().sum().sum() / df.size * 100, 2)),
    ]
    return pd.DataFrame(items, columns=["Показатель", "Значение"])


def target_distribution(df, target):
    counts = df[target].value_counts(dropna=False).sort_index()
    shares = counts / counts.sum()
    out = pd.DataFrame({
        "Класс": counts.index.astype(str),
        "Количество": counts.values,
        "Доля, %": (shares.values * 100).round(2),
    })
    baseline = pd.DataFrame({
        "Класс": ["BASELINE (мажоритарный класс)"],
        "Количество": [int(counts.max())],
        "Доля, %": [round(shares.max() * 100, 2)],
    })
    return pd.concat([out, baseline], ignore_index=True)


def column_profile(df):
    n = len(df)
    rows = []
    for col in df.columns:
        s = df[col]
        missing = int(s.isna().sum())
        nunique = int(s.nunique(dropna=True))
        row = {
            "Признак": col,
            "Тип": str(s.dtype),
            "Пропусков, шт": missing,
            "Пропусков, %": round(missing / n * 100, 2),
            "Уникальных значений": nunique,
            "Константа": nunique <= 1,
        }
        if pd.api.types.is_numeric_dtype(s):
            row.update({
                "Минимум": s.min(),
                "Медиана": s.median(),
                "Максимум": s.max(),
                "Среднее": round(s.mean(), 3) if nunique > 1 else np.nan,
                "Ст. отклонение": round(s.std(), 3) if nunique > 1 else np.nan,
            })
        elif nunique > 0:
            vc = s.value_counts()
            row["Самое частое значение"] = str(vc.index[0])[:40]
            row["Доля самого частого, %"] = round(vc.iloc[0] / n * 100, 2)
        rows.append(row)
    return (pd.DataFrame(rows)
            .sort_values("Пропусков, %", ascending=False)
            .reset_index(drop=True))


def category_cardinality(profile, categorical):
    return (profile[profile["Признак"].isin(categorical)]
            [["Признак", "Уникальных значений", "Пропусков, %"]]
            .sort_values("Уникальных значений", ascending=False)
            .reset_index(drop=True))


def category_levels(df, columns, top_n=15):
    frames = []
    for col in columns:
        if col not in df.columns:
            continue
        vc = df[col].value_counts(dropna=False).head(top_n)
        frames.append(pd.DataFrame({
            "Признак": col,
            "Значение": vc.index.astype(str),
            "Количество": vc.values,
            "Доля, %": (vc.values / len(df) * 100).round(3),
        }))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def flag_summary(df, bool_columns):
    rows = []
    for col in bool_columns:
        if col not in df.columns:
            continue
        s = df[col]
        rows.append({
            "Признак": col,
            "True, шт": int(s.sum()),
            "True, %": round(s.mean() * 100, 4),
        })
    return (pd.DataFrame(rows)
            .sort_values("True, %", ascending=False)
            .reset_index(drop=True))


def numeric_anomalies(df, rules):
    rows = []
    for col, (lo, hi) in rules.items():
        if col not in df.columns:
            continue
        s = df[col]
        bad = ((s < lo) | (s > hi)) & s.notna()
        rows.append({
            "Признак": col,
            "Границы": f"[{lo}; {hi}]",
            "Факт. минимум": s.min(),
            "Факт. максимум": s.max(),
            "Вне границ, шт": int(bad.sum()),
            "Вне границ, %": round(bad.mean() * 100, 4),
        })
    return pd.DataFrame(rows)


# ---------- сигнал: категориальные разрезы и хвосты распределений ----------

def class_mix_by_group(df, group_series, target, min_count=30):
    """Распределение классов внутри каждой группы + lift к базовой доле.
    lift > 1 означает, что класс встречается в группе чаще, чем в датасете."""
    tmp = pd.DataFrame({"group": group_series.astype(str), "y": df[target].values})
    counts = tmp.groupby(["group", "y"]).size().unstack(fill_value=0)
    counts = counts[counts.sum(axis=1) >= min_count]
    if counts.empty:
        return pd.DataFrame()

    base = df[target].value_counts(normalize=True).sort_index()
    shares = counts.div(counts.sum(axis=1), axis=0)

    out = pd.DataFrame({"Группа": counts.index, "Записей": counts.sum(axis=1).values})
    for cls in counts.columns:
        out[f"Доля {cls}, %"] = (shares[cls].values * 100).round(2)
    for cls in counts.columns:
        out[f"lift {cls}"] = (shares[cls].values / base[cls]).round(2)
    return out.sort_values("Записей", ascending=False).reset_index(drop=True)


def tail_signal(df, target, conditions):
    """Доля каждого класса внутри подмножества, заданного условием.
    conditions: {название: булева маска}"""
    base = df[target].value_counts(normalize=True).sort_index()
    rows = []
    for name, mask in conditions.items():
        mask = mask.fillna(False)
        sub = df.loc[mask, target]
        if len(sub) == 0:
            continue
        shares = sub.value_counts(normalize=True).reindex(base.index, fill_value=0)
        row = {"Условие": name, "Записей": int(len(sub)),
               "Доля выборки, %": round(len(sub) / len(df) * 100, 2)}
        for cls in base.index:
            row[f"Доля {cls}, %"] = round(shares[cls] * 100, 2)
        for cls in base.index:
            row[f"lift {cls}"] = round(shares[cls] / base[cls], 2)
        rows.append(row)
    return pd.DataFrame(rows)