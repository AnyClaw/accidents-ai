"""Этап 1: аудит датасета US Accidents. Отчёт — только данные и выводы."""

from datetime import datetime

import numpy as np
import pandas as pd

import config as cfg
import audit
from report import Report


BOOL_FLAGS = [
    "Amenity", "Bump", "Crossing", "Give_Way", "Junction", "No_Exit",
    "Railway", "Roundabout", "Station", "Stop", "Traffic_Calming",
    "Traffic_Signal", "Turning_Loop",
]

CATEGORICAL = [
    "State", "City", "County", "Street", "Side", "Timezone",
    "Airport_Code", "Wind_Direction", "Weather_Condition",
    "Sunrise_Sunset", "Civil_Twilight", "Nautical_Twilight", "Astronomical_Twilight",
]

ANOMALY_RULES = {
    "Temperature(F)":    (-60, 140),
    "Humidity(%)":       (0, 100),
    "Pressure(in)":      (20, 35),
    "Visibility(mi)":    (0, 20),
    "Wind_Speed(mph)":   (0, 120),
    "Precipitation(in)": (0, 10),
    "Start_Lat":         (24, 50),
    "Start_Lng":         (-125, -66),
}

TRUE_STRINGS = {"true", "1", "1.0", "yes", "t"}
FALSE_STRINGS = {"false", "0", "0.0", "no", "f"}

MIN_SUFFIX_COUNT = 20      # порог массовости суффикса для проверки утечки
MIN_GROUP_COUNT = 30       # порог массовости группы при анализе сигнала


# =====================================================================
# Очистка
# =====================================================================

def find_broken_rows(df):
    mask = pd.Series(False, index=df.index)
    if "ID" in df.columns:
        mask |= df["ID"].isna()
    for col in BOOL_FLAGS:
        if col in df.columns:
            mask |= df[col].isna()
    return df[mask]


def fix_boolean_flags(df):
    rows = []
    for col in BOOL_FLAGS:
        if col not in df.columns:
            continue
        before = str(df[col].dtype)
        s = df[col].astype(str).str.strip().str.lower()
        unknown = int((~(s.isin(TRUE_STRINGS) | s.isin(FALSE_STRINGS))).sum())
        df[col] = s.isin(TRUE_STRINGS)
        rows.append({"Признак": col, "Тип до": before,
                     "Тип после": str(df[col].dtype), "Нераспознано, шт": unknown})
    return df, pd.DataFrame(rows)


# =====================================================================
# Нормализация категорий (детерминированная, без статистики выборки)
# =====================================================================

WIND_SYNONYMS = {
    "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W",
    "NORTHEAST": "NE", "NORTHWEST": "NW",
    "SOUTHEAST": "SE", "SOUTHWEST": "SW",
    "VARIABLE": "VAR", "VRB": "VAR",
    "CALM": "CALM",
}


def normalize_wind(series):
    s = series.astype(str).str.strip().str.upper()
    s = s.replace(WIND_SYNONYMS)
    s = s.where(~series.isna(), "UNKNOWN")
    s = s.where(s != "NAN", "UNKNOWN")
    return s


# порядок важен: сначала опасные явления, затем нейтральные
WEATHER_RULES = [
    ("storm",          ["thunder", "t-storm", "squall"]),
    ("snow",           ["snow", "sleet", "blizzard", "ice", "hail", "freezing"]),
    ("rain",           ["rain", "drizzle", "shower"]),
    ("low_visibility", ["fog", "haze", "mist", "smoke", "dust", "sand"]),
    ("cloudy",         ["cloud", "overcast"]),
    ("clear",          ["clear", "fair"]),
]


def group_weather(series):
    s = series.fillna("").astype(str).str.lower()
    result = pd.Series("unknown", index=series.index)
    assigned = pd.Series(False, index=series.index)
    for name, keys in WEATHER_RULES:
        hit = s.apply(lambda v: any(k in v for k in keys)) & ~assigned
        result[hit] = name
        assigned |= hit
    return result


def hour_bucket(hour):
    if 7 <= hour <= 9:
        return "1_rush_morning"
    if 16 <= hour <= 18:
        return "2_rush_evening"
    if 10 <= hour <= 15:
        return "3_day"
    if 19 <= hour <= 22:
        return "4_evening"
    return "5_night"


# =====================================================================
# Утечка в Description
# =====================================================================

def description_leakage(df, target, tail_words=3, min_count=MIN_SUFFIX_COUNT, top_n=25):
    if "Description" not in df.columns:
        return pd.DataFrame(), pd.DataFrame()

    desc = df["Description"].fillna("").astype(str)
    cleaned = (desc.str.replace(r"\[Shared\]", "", regex=True)
                   .str.replace(r"\[Appended[^\]]*\]", "", regex=True)
                   .str.replace(r"[.\s]+$", "", regex=True)
                   .str.strip())
    tail = cleaned.str.split().str[-tail_words:].str.join(" ").str.lower()

    tmp = pd.DataFrame({"suffix": tail, "y": df[target].values})
    counts = tmp.groupby(["suffix", "y"]).size().unstack(fill_value=0)
    totals = counts.sum(axis=1)
    base = df[target].value_counts(normalize=True).sort_index()

    mass = counts[totals >= min_count]
    mass_totals = totals[totals >= min_count]
    purity = mass.max(axis=1) / mass_totals

    summary = pd.DataFrame({
        f"Последние {tail_words} слова": mass.index,
        "Записей": mass_totals.values,
        "Мажоритарный класс": mass.idxmax(axis=1).values,
        "Чистота, %": (purity.values * 100).round(2),
    })
    for cls in mass.columns:
        summary[f"Severity {cls}"] = mass[cls].values
    summary["lift мажоритарного"] = [
        round((mass.loc[s, c] / mass_totals[s]) / base[c], 2)
        for s, c in zip(mass.index, mass.idxmax(axis=1))
    ]
    summary = summary.sort_values("Записей", ascending=False).head(top_n).reset_index(drop=True)

    pure_mask = purity >= 0.95
    verdict = pd.DataFrame([
        ("Порог массовости суффикса, записей", min_count),
        ("Уникальных суффиксов всего", len(totals)),
        ("Массовых суффиксов", len(mass)),
        ("Записей под массовыми суффиксами", int(mass_totals.sum())),
        ("Покрытие датасета массовыми суффиксами, %",
         round(mass_totals.sum() / len(df) * 100, 2)),
        ("Массовых суффиксов с чистотой >= 95%", int(pure_mask.sum())),
        ("Записей под ними", int(mass_totals[pure_mask].sum())),
        ("Доля датасета под ними, %",
         round(mass_totals[pure_mask].sum() / len(df) * 100, 2)),
    ], columns=["Показатель", "Значение"])

    return summary, verdict


# =====================================================================
# Рабочие константы для этапа 2 (в отчёт не выводятся)
# =====================================================================

FEATURE_PLAN = [
    ("Temperature(F)",    "числовой",  "аномалии->NaN; клиппинг [-60;140]; медиана train; стандартизация"),
    ("Humidity(%)",       "числовой",  "аномалии->NaN; клиппинг [0;100]; медиана train; стандартизация"),
    ("Pressure(in)",      "числовой",  "аномалии->NaN; медиана train; стандартизация"),
    ("Visibility(mi)",    "числовой",  "аномалии->NaN; медиана train; обрезка сверху до 10; стандартизация"),
    ("Wind_Speed(mph)",   "числовой",  ">120->NaN; медиана train; флаг пропуска; стандартизация"),
    ("Start_Lat",         "числовой",  "медиана train; стандартизация"),
    ("Start_Lng",         "числовой",  "медиана train; стандартизация"),
    ("low_visibility",    "производный","1 если Visibility < 5, иначе 0"),
    ("is_freezing",       "производный","1 если Temperature < 32, иначе 0"),
    ("Weather_Condition", "категория", "группировка по WEATHER_RULES -> OHE"),
    ("Wind_Direction",    "категория", "normalize_wind -> OHE"),
    ("Sunrise_Sunset",    "категория", "NaN->Unknown -> OHE"),
    ("State",             "категория", "NaN->Unknown -> OHE"),
    ("Side",              "категория", "NaN->Unknown -> OHE"),
    ("Start_Time",        "дата",      "hour, day_of_week, month, is_weekend, is_rush_hour"),
    ("Amenity",           "булев",     "0/1"),
    ("Crossing",          "булев",     "0/1"),
    ("Junction",          "булев",     "0/1"),
    ("Railway",           "булев",     "0/1"),
    ("Station",           "булев",     "0/1"),
    ("Stop",              "булев",     "0/1"),
    ("Traffic_Signal",    "булев",     "0/1"),
    ("Severity",          "ЦЕЛЕВАЯ",   "4 класса"),
]

DROP_PLAN = [
    ("ID", "идентификатор"), ("Number", "номер дома; 65% пропусков"),
    ("Country", "константа"), ("Description", "текст + утечка"),
    ("Street", "14474 категории"), ("City", "4501 категория"),
    ("County", "1020 категорий"), ("Zipcode", "17771 значение"),
    ("Airport_Code", "код метеостанции"), ("Timezone", "дублирует долготу"),
    ("Wind_Chill(F)", "производная; 41% пропусков"),
    ("Precipitation(in)", "45% пропусков; сигнал в Weather_Condition"),
    ("Weather_Timestamp", "время замера погоды"),
    ("Civil_Twilight", "избыточен"), ("Nautical_Twilight", "избыточен"),
    ("Astronomical_Twilight", "избыточен"),
    ("End_Time", "утечка"), ("End_Lat", "утечка"), ("End_Lng", "утечка"),
    ("Distance(mi)", "утечка"),
    ("Bump", "3 True"), ("No_Exit", "64 True"), ("Give_Way", "128 True"),
    ("Traffic_Calming", "15 True"), ("Roundabout", "3 True"),
    ("Turning_Loop", "константа"),
]


# =====================================================================
# MAIN
# =====================================================================

def main():
    pd.set_option("display.width", 220)

    print("Загрузка данных...")
    df = audit.load_data(cfg.DATA_PATH, nrows=cfg.NROWS)
    rows_raw = len(df)

    # --- очистка ---
    broken = find_broken_rows(df)
    df = df.drop(index=broken.index).reset_index(drop=True)
    rows_after_broken = len(df)

    dup_mask = df.drop(columns=["ID"], errors="ignore").duplicated()
    df = df.loc[~dup_mask].reset_index(drop=True)
    rows_final = len(df)

    df, bool_fix = fix_boolean_flags(df)

    cleaning = pd.DataFrame([
        ("Строк в файле", rows_raw),
        ("Удалено строк-артефактов", rows_raw - rows_after_broken),
        ("Удалено дубликатов без ID", rows_after_broken - rows_final),
        ("Строк после очистки", rows_final),
    ], columns=["Показатель", "Значение"])

    # --- нормализация категорий ---
    weather_group = group_weather(df["Weather_Condition"])
    wind_norm = normalize_wind(df["Wind_Direction"])
    start_dt = pd.to_datetime(df["Start_Time"], errors="coerce")
    hours = start_dt.dt.hour
    buckets = hours.map(lambda h: hour_bucket(int(h)) if pd.notna(h) else "unknown")

    weather_map = pd.DataFrame({
        "Исходное значение": df["Weather_Condition"].fillna("(пропуск)").astype(str),
        "Группа": weather_group,
    }).groupby(["Группа", "Исходное значение"]).size().reset_index(name="Записей")
    weather_map = weather_map.sort_values(["Группа", "Записей"],
                                          ascending=[True, False]).reset_index(drop=True)

    weather_stat = (pd.DataFrame({"Группа": weather_group})
                    .value_counts().rename_axis("Группа").reset_index(name="Записей"))
    weather_stat["Доля, %"] = (weather_stat["Записей"] / len(df) * 100).round(2)

    wind_stat = (wind_norm.value_counts().rename_axis("Значение")
                 .reset_index(name="Записей"))
    wind_stat["Доля, %"] = (wind_stat["Записей"] / len(df) * 100).round(2)

    # --- базовые таблицы ---
    ov = audit.overview(df)
    dist = audit.target_distribution(df, cfg.TARGET)
    profile = audit.column_profile(df)
    card = audit.category_cardinality(profile, CATEGORICAL)
    levels = audit.category_levels(df, CATEGORICAL, top_n=15)
    flags = audit.flag_summary(df, BOOL_FLAGS)
    anomalies = audit.numeric_anomalies(df, ANOMALY_RULES)

    # --- утечка ---
    leak_table, leak_verdict = description_leakage(df, cfg.TARGET)

    # --- сигнал ---
    num_cols = ["Temperature(F)", "Visibility(mi)", "Wind_Speed(mph)"]
    signal_num = df.groupby(cfg.TARGET)[num_cols].median().round(2).reset_index()

    tails = audit.tail_signal(df, cfg.TARGET, {
        "Visibility < 5": df["Visibility(mi)"] < 5,
        "Visibility < 1": df["Visibility(mi)"] < 1,
        "Temperature < 32": df["Temperature(F)"] < 32,
        "Wind_Speed > 20": df["Wind_Speed(mph)"] > 20,
        "Humidity > 90": df["Humidity(%)"] > 90,
    })
    sig_weather = audit.class_mix_by_group(df, weather_group, cfg.TARGET, MIN_GROUP_COUNT)
    sig_hours = audit.class_mix_by_group(df, buckets, cfg.TARGET, MIN_GROUP_COUNT)
    sig_night = audit.class_mix_by_group(df, df["Sunrise_Sunset"], cfg.TARGET, MIN_GROUP_COUNT)
    sig_state = audit.class_mix_by_group(df, df["State"], cfg.TARGET, MIN_GROUP_COUNT)

    # --- консоль ---
    print("\n=== ОЧИСТКА ===")
    print(cleaning.to_string(index=False))
    print("\n=== РАСПРЕДЕЛЕНИЕ Severity ===")
    print(dist.to_string(index=False))
    print("\n=== УТЕЧКА (массовые суффиксы) ===")
    print(leak_verdict.to_string(index=False))
    print("\n=== СИГНАЛ: хвосты распределений ===")
    print(tails.to_string(index=False))
    print("\n=== СИГНАЛ: группы погоды ===")
    print(sig_weather.to_string(index=False))

    # --- отчёт ---
    rep = Report("Этап 1. Аудит датасета US Accidents")
    rep.text(f"Дата: {datetime.now():%Y-%m-%d %H:%M}  \n"
             f"Источник: `{cfg.DATA_PATH.name}`  \n"
             f"Целевая переменная: `{cfg.TARGET}`")

    rep.section("1. Очистка и объём данных")
    rep.table("Удалённые записи", cleaning)
    rep.table("Состояние датасета после очистки", ov)
    rep.table("Приведение булевых признаков", bool_fix)

    rep.section("2. Целевая переменная")
    rep.table("Распределение классов", dist,
              note="BASELINE — точность константного предсказания мажоритарного класса.")

    rep.section("3. Профиль признаков")
    rep.table("Все признаки", profile, max_rows=60)

    rep.section("4. Категориальные признаки")
    rep.table("Кардинальность", card)
    rep.table("Частые значения", levels, max_rows=200)

    rep.section("5. Булевы признаки")
    rep.table("Доля True", flags)

    rep.section("6. Физические границы")
    rep.table("Выходы за диапазоны", anomalies)

    rep.section("7. Утечка данных в Description")
    rep.table("Показатели по массовым суффиксам", leak_verdict,
              note=f"Учитываются суффиксы, встречающиеся не менее {MIN_SUFFIX_COUNT} раз. "
                   "Единичные суффиксы исключены: их чистота равна 100% по построению.")
    rep.table("Массовые суффиксы и распределение классов", leak_table,
              note="lift — отношение доли класса внутри суффикса к его доле в датасете.",
              max_rows=30)

    rep.section("8. Нормализация категорий")
    rep.table("Группы Weather_Condition", weather_stat)
    rep.table("Соответствие значений группам", weather_map, max_rows=120)
    rep.table("Wind_Direction после нормализации", wind_stat)

    rep.section("9. Различимость классов")
    rep.table("Медианы числовых признаков по классам", signal_num)
    rep.table("Хвосты распределений", tails, note="Доля класса внутри подмножества и lift к базовой доле.")
    rep.table("Группы погоды", sig_weather)
    rep.table("Интервалы суток", sig_hours)
    rep.table("Время суток (Sunrise_Sunset)", sig_night)
    rep.table("Штаты", sig_state, max_rows=50)

    path = rep.save(cfg.REPORT_MD)
    cfg.PROFILE_CSV.parent.mkdir(parents=True, exist_ok=True)
    profile.to_csv(cfg.PROFILE_CSV, sep=";", decimal=",", index=False, encoding="utf-8-sig")

    print(f"\nОтчёт: {path}")
    print(f"CSV:   {cfg.PROFILE_CSV}")


if __name__ == "__main__":
    main()