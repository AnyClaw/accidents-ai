from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT_DIR / "data" / "US_Accidents_Dec20_Updated.csv"
REPORT_DIR = ROOT_DIR / "reports" / "stage1"

# имена итоговых файлов отчёта
REPORT_MD = REPORT_DIR / "stage1_report.md"
PROFILE_CSV = REPORT_DIR / "column_profile.csv"

TARGET = "Severity"

NROWS = None          # None = весь файл; число = быстрый прогон на подвыборке
RANDOM_STATE = 42