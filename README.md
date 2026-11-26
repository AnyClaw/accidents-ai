# Предсказание тяжести ДТП (US Accidents)

Курсовой проект по дисциплине «Основы ИИ». Задача: обучить модель многоклассовой классификации для предсказания степени тяжести дорожно-транспортного происшествия (`Severity`) по погодным условиям, времени суток и характеристикам дорожной инфраструктуры.

## Особенности реализации

- **Модель:** Multinomial Logistic Regression с Softmax на выходе.
- **Без ML-библиотек:** Все алгоритмы обучения (градиентный спуск, cross-entropy, softmax, метрики) реализованы самостоятельно на `NumPy`.
- **Датасет:** [US Accidents (Dec20 Updated)] — ~42 тыс. записей после очистки.

## Архитектура проекта

```text
├── data/                  # Исходный CSV-файл датасета
├── reports/
│   └── stage1/            # Отчёты аудита (markdown + csv)
├── src/
│   ├── config.py          # Пути, константы, настройки
│   ├── audit.py           # Функции расчёта статистик и таблиц
│   ├── report.py          # Генерация единого markdown-отчёта
│   ├── preprocessing.py   # [Этап 2] Imputer, Scaler, OneHotEncoder на NumPy
│   ├── model.py           # [Этап 3] Softmax, CrossEntropy, GradientDescent
│   ├── metrics.py         # [Этап 3] Accuracy, F1, Confusion Matrix
│   └── stage1_audit.py    # Точка входа этапа 1
└── README.md
```

## Зависимости

- numpy
- pandas
- tabulate