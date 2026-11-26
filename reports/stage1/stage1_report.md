# Этап 1. Аудит датасета US Accidents

Дата: 2026-11-26 02:49  
Источник: `US_Accidents_Dec20_Updated.csv`  
Целевая переменная: `Severity`


## 1. Очистка и объём данных


### Удалённые записи

| Показатель | Значение |
| --- | --- |
| Строк в файле | 42768 |
| Удалено строк-артефактов | 1 |
| Удалено дубликатов без ID | 23 |
| Строк после очистки | 42744 |


### Состояние датасета после очистки

| Показатель | Значение |
| --- | --- |
| Количество строк | 42744 |
| Количество столбцов | 47 |
| Объём в памяти, МБ | 59.6 |
| Полных дубликатов строк | 0 |
| Дубликатов без учёта ID | 0 |
| Всего пропущенных значений | 84329 |
| Доля пропусков во всём датасете, % | 4.2 |


### Приведение булевых признаков

| Признак | Тип до | Тип после | Нераспознано, шт |
| --- | --- | --- | --- |
| Amenity | object | bool | 0 |
| Bump | object | bool | 0 |
| Crossing | object | bool | 0 |
| Give_Way | object | bool | 0 |
| Junction | object | bool | 0 |
| No_Exit | object | bool | 0 |
| Railway | object | bool | 0 |
| Roundabout | object | bool | 0 |
| Station | object | bool | 0 |
| Stop | object | bool | 0 |
| Traffic_Calming | object | bool | 0 |
| Traffic_Signal | object | bool | 0 |
| Turning_Loop | object | bool | 0 |


## 2. Целевая переменная


### Распределение классов

BASELINE — точность константного предсказания мажоритарного класса.

| Класс | Количество | Доля, % |
| --- | --- | --- |
| 1 | 433 | 1.01 |
| 2 | 31251 | 73.11 |
| 3 | 9302 | 21.76 |
| 4 | 1758 | 4.11 |
| BASELINE (мажоритарный класс) | 31251 | 73.11 |


## 3. Профиль признаков


### Все признаки

| Признак | Тип | Пропусков, шт | Пропусков, % | Уникальных значений | Константа | Самое частое значение | Доля самого частого, % | Минимум | Медиана | Максимум | Среднее | Ст. отклонение |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Number | float64 | 27865 | 65.19 | 6843 | False | — | — | 1 | 3014 | 851799 | 6684.3 | 14508.1 |
| Precipitation(in) | float64 | 19202 | 44.92 | 80 | False | — | — | 0 | 0 | 9.99 | 0.011 | 0.139 |
| Wind_Chill(F) | float64 | 17595 | 41.16 | 586 | False | — | — | -41.6 | 58 | 110 | 55.01 | 22.216 |
| Wind_Speed(mph) | float64 | 4517 | 10.57 | 67 | False | — | — | 0 | 7 | 232 | 7.856 | 5.268 |
| End_Lng | float64 | 4205 | 9.84 | 36022 | False | — | — | -124.486 | -91.06 | -68.3654 | -96.129 | 17.633 |
| End_Lat | float64 | 4205 | 9.84 | 35968 | False | — | — | 24.5714 | 36.0174 | 48.9976 | 36.475 | 4.995 |
| Weather_Condition | str | 1056 | 2.47 | 68 | False | Fair | 23.67 | — | — | — | — | — |
| Visibility(mi) | float64 | 1049 | 2.45 | 44 | False | — | — | 0 | 10 | 80 | 9.133 | 2.819 |
| Humidity(%) | float64 | 1039 | 2.43 | 99 | False | — | — | 2 | 68 | 100 | 65.183 | 22.868 |
| Temperature(F) | float64 | 982 | 2.3 | 563 | False | — | — | -23.8 | 63 | 117 | 61.053 | 18.414 |
| Wind_Direction | str | 924 | 2.16 | 24 | False | CALM | 9.77 | — | — | — | — | — |
| Pressure(in) | float64 | 839 | 1.96 | 737 | False | — | — | 20.27 | 29.92 | 31.12 | 29.658 | 0.908 |
| Weather_Timestamp | str | 681 | 1.59 | 35566 | False | 2020-10-30 13:53:00 | 0.02 | — | — | — | — | — |
| Airport_Code | str | 92 | 0.22 | 1366 | False | KCQT | 1.7 | — | — | — | — | — |
| Timezone | str | 45 | 0.11 | 4 | False | US/Eastern | 41.72 | — | — | — | — | — |
| Zipcode | str | 13 | 0.03 | 17771 | False | 91706 | 0.19 | — | — | — | — | — |
| Nautical_Twilight | str | 4 | 0.01 | 2 | False | Day | 76.52 | — | — | — | — | — |
| Civil_Twilight | str | 4 | 0.01 | 2 | False | Day | 71.69 | — | — | — | — | — |
| City | str | 4 | 0.01 | 4501 | False | Houston | 2.57 | — | — | — | — | — |
| Astronomical_Twilight | str | 4 | 0.01 | 2 | False | Day | 80.36 | — | — | — | — | — |
| Sunrise_Sunset | str | 4 | 0.01 | 2 | False | Day | 67.12 | — | — | — | — | — |
| Street | str | 0 | 0 | 14474 | False | I-5 N | 1.38 | — | — | — | — | — |
| Side | str | 0 | 0 | 2 | False | R | 82.75 | — | — | — | — | — |
| ID | str | 0 | 0 | 42744 | False | A-1 | 0 | — | — | — | — | — |
| Severity | int64 | 0 | 0 | 4 | False | — | — | 1 | 2 | 4 | 2.29 | 0.555 |
| Start_Time | str | 0 | 0 | 42541 | False | 2020-10-08 10:53:30 | 0.01 | — | — | — | — | — |
| Description | str | 0 | 0 | 38777 | False | A crash has occurred causing no to minim | 0.07 | — | — | — | — | — |
| Distance(mi) | float64 | 0 | 0 | 3418 | False | — | — | 0 | 0 | 148.36 | 0.396 | 1.609 |
| End_Time | str | 0 | 0 | 42638 | False | 2016-10-17 13:44:53 | 0.01 | — | — | — | — | — |
| Start_Lat | float64 | 0 | 0 | 39614 | False | — | — | 24.5748 | 36.0691 | 48.9976 | 36.496 | 4.997 |
| Start_Lng | float64 | 0 | 0 | 39639 | False | — | — | -124.486 | -91.1912 | -68.366 | -96.398 | 17.744 |
| County | str | 0 | 0 | 1020 | False | Los Angeles | 8.07 | — | — | — | — | — |
| Amenity | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.011 | 0.104 |
| Country | str | 0 | 0 | 1 | True | US | 100 | — | — | — | — | — |
| State | str | 0 | 0 | 49 | False | CA | 25.23 | — | — | — | — | — |
| Bump | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0 | 0.008 |
| Crossing | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.077 | 0.266 |
| Give_Way | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.003 | 0.055 |
| Junction | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.098 | 0.297 |
| Station | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.02 | 0.139 |
| Roundabout | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0 | 0.008 |
| Railway | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.008 | 0.092 |
| No_Exit | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.001 | 0.039 |
| Turning_Loop | bool | 0 | 0 | 1 | True | — | — | False | 0 | False | — | — |
| Traffic_Signal | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.157 | 0.364 |
| Traffic_Calming | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0 | 0.019 |
| Stop | bool | 0 | 0 | 2 | False | — | — | False | 0 | True | 0.015 | 0.123 |


## 4. Категориальные признаки


### Кардинальность

| Признак | Уникальных значений | Пропусков, % |
| --- | --- | --- |
| Street | 14474 | 0 |
| City | 4501 | 0.01 |
| Airport_Code | 1366 | 0.22 |
| County | 1020 | 0 |
| Weather_Condition | 68 | 2.47 |
| State | 49 | 0 |
| Wind_Direction | 24 | 2.16 |
| Timezone | 4 | 0.11 |
| Nautical_Twilight | 2 | 0.01 |
| Sunrise_Sunset | 2 | 0.01 |
| Astronomical_Twilight | 2 | 0.01 |
| Civil_Twilight | 2 | 0.01 |
| Side | 2 | 0 |


### Частые значения

| Признак | Значение | Количество | Доля, % |
| --- | --- | --- | --- |
| State | CA | 10785 | 25.232 |
| State | FL | 3839 | 8.981 |
| State | TX | 3456 | 8.085 |
| State | NY | 1907 | 4.461 |
| State | NC | 1853 | 4.335 |
| State | SC | 1673 | 3.914 |
| State | OR | 1401 | 3.278 |
| State | VA | 1354 | 3.168 |
| State | PA | 1314 | 3.074 |
| State | MN | 1152 | 2.695 |
| State | IL | 1152 | 2.695 |
| State | GA | 984 | 2.302 |
| State | MI | 948 | 2.218 |
| State | AZ | 944 | 2.208 |
| State | TN | 808 | 1.89 |
| City | Houston | 1097 | 2.566 |
| City | Los Angeles | 971 | 2.272 |
| City | Charlotte | 848 | 1.984 |
| City | Dallas | 748 | 1.75 |
| City | Miami | 731 | 1.71 |
| City | Austin | 509 | 1.191 |
| City | Raleigh | 468 | 1.095 |
| City | Orlando | 460 | 1.076 |
| City | Atlanta | 423 | 0.99 |
| City | Sacramento | 382 | 0.894 |
| City | Baton Rouge | 374 | 0.875 |
| City | Nashville | 351 | 0.821 |
| City | San Diego | 344 | 0.805 |
| City | Minneapolis | 317 | 0.742 |
| City | Phoenix | 304 | 0.711 |
| County | Los Angeles | 3450 | 8.071 |
| County | Orange | 1241 | 2.903 |
| County | Harris | 1159 | 2.711 |
| County | Miami-Dade | 942 | 2.204 |
| County | Mecklenburg | 907 | 2.122 |
| County | Dallas | 893 | 2.089 |
| County | Montgomery | 722 | 1.689 |
| County | San Diego | 700 | 1.638 |
| County | Alameda | 650 | 1.521 |
| County | San Bernardino | 642 | 1.502 |
| County | Wake | 642 | 1.502 |
| County | Maricopa | 617 | 1.443 |
| County | Riverside | 561 | 1.312 |
| County | Travis | 560 | 1.31 |
| County | Sacramento | 550 | 1.287 |
| Street | I-5 N | 589 | 1.378 |
| Street | I-95 N | 523 | 1.224 |
| Street | I-95 S | 423 | 0.99 |
| Street | I-10 E | 379 | 0.887 |
| Street | I-5 S | 322 | 0.753 |
| Street | I-10 W | 317 | 0.742 |
| Street | I-80 W | 292 | 0.683 |
| Street | I-80 E | 251 | 0.587 |
| Street | I-405 N | 240 | 0.561 |
| Street | I-15 N | 196 | 0.459 |
| Street | I-75 S | 193 | 0.452 |
| Street | I-75 N | 173 | 0.405 |
| Street | I-94 W | 170 | 0.398 |
| Street | US-101 N | 153 | 0.358 |
| Street | CA-99 N | 145 | 0.339 |
| Side | R | 35372 | 82.753 |
| Side | L | 7372 | 17.247 |
| Timezone | US/Eastern | 17834 | 41.723 |
| Timezone | US/Pacific | 13051 | 30.533 |
| Timezone | US/Central | 9346 | 21.865 |
| Timezone | US/Mountain | 2468 | 5.774 |
| Timezone | — | 45 | 0.105 |
| Airport_Code | KCQT | 728 | 1.703 |
| Airport_Code | KMCJ | 623 | 1.458 |
| Airport_Code | KRDU | 591 | 1.383 |
| Airport_Code | KCLT | 562 | 1.315 |
| Airport_Code | KBNA | 502 | 1.174 |
| Airport_Code | KEMT | 453 | 1.06 |
| Airport_Code | KFUL | 423 | 0.99 |
| Airport_Code | KBTR | 396 | 0.926 |
| Airport_Code | KLGA | 388 | 0.908 |
| Airport_Code | KHHR | 387 | 0.905 |
| Airport_Code | KORL | 385 | 0.901 |
| Airport_Code | KDAL | 380 | 0.889 |
| Airport_Code | KSNA | 371 | 0.868 |
| Airport_Code | KATT | 366 | 0.856 |
| Airport_Code | KCCR | 320 | 0.749 |
| Wind_Direction | CALM | 4177 | 9.772 |
| Wind_Direction | Calm | 3313 | 7.751 |
| Wind_Direction | WNW | 2168 | 5.072 |
| Wind_Direction | SSW | 2033 | 4.756 |
| Wind_Direction | NW | 1994 | 4.665 |
| Wind_Direction | WSW | 1963 | 4.592 |
| Wind_Direction | SW | 1953 | 4.569 |
| Wind_Direction | SSE | 1899 | 4.443 |
| Wind_Direction | NNW | 1868 | 4.37 |
| Wind_Direction | S | 1665 | 3.895 |
| Wind_Direction | South | 1556 | 3.64 |
| Wind_Direction | W | 1541 | 3.605 |
| Wind_Direction | North | 1540 | 3.603 |
| Wind_Direction | West | 1517 | 3.549 |
| Wind_Direction | SE | 1511 | 3.535 |
| Weather_Condition | Fair | 10117 | 23.669 |
| Weather_Condition | Clear | 7404 | 17.322 |
| Weather_Condition | Mostly Cloudy | 5788 | 13.541 |
| Weather_Condition | Partly Cloudy | 4033 | 9.435 |
| Weather_Condition | Cloudy | 3454 | 8.081 |
| Weather_Condition | Overcast | 3451 | 8.074 |
| Weather_Condition | Light Rain | 2096 | 4.904 |
| Weather_Condition | Scattered Clouds | 1896 | 4.436 |
| Weather_Condition | — | 1056 | 2.471 |
| Weather_Condition | Light Snow | 609 | 1.425 |
| Weather_Condition | Fog | 488 | 1.142 |
| Weather_Condition | Rain | 481 | 1.125 |
| Weather_Condition | Haze | 463 | 1.083 |
| Weather_Condition | Heavy Rain | 176 | 0.412 |
| Weather_Condition | Light Drizzle | 131 | 0.306 |
| Sunrise_Sunset | Day | 28691 | 67.123 |
| Sunrise_Sunset | Night | 14049 | 32.868 |
| Sunrise_Sunset | — | 4 | 0.009 |
| Civil_Twilight | Day | 30645 | 71.694 |
| Civil_Twilight | Night | 12095 | 28.296 |
| Civil_Twilight | — | 4 | 0.009 |
| Nautical_Twilight | Day | 32707 | 76.518 |
| Nautical_Twilight | Night | 10033 | 23.472 |
| Nautical_Twilight | — | 4 | 0.009 |
| Astronomical_Twilight | Day | 34351 | 80.364 |
| Astronomical_Twilight | Night | 8389 | 19.626 |
| Astronomical_Twilight | — | 4 | 0.009 |


## 5. Булевы признаки


### Доля True

| Признак | True, шт | True, % |
| --- | --- | --- |
| Traffic_Signal | 6719 | 15.7192 |
| Junction | 4184 | 9.7885 |
| Crossing | 3273 | 7.6572 |
| Station | 842 | 1.9699 |
| Stop | 658 | 1.5394 |
| Amenity | 466 | 1.0902 |
| Railway | 361 | 0.8446 |
| Give_Way | 128 | 0.2995 |
| No_Exit | 64 | 0.1497 |
| Traffic_Calming | 15 | 0.0351 |
| Bump | 3 | 0.007 |
| Roundabout | 3 | 0.007 |
| Turning_Loop | 0 | 0 |


## 6. Физические границы


### Выходы за диапазоны

| Признак | Границы | Факт. минимум | Факт. максимум | Вне границ, шт | Вне границ, % |
| --- | --- | --- | --- | --- | --- |
| Temperature(F) | [-60; 140] | -23.8 | 117 | 0 | 0 |
| Humidity(%) | [0; 100] | 2 | 100 | 0 | 0 |
| Pressure(in) | [20; 35] | 20.27 | 31.12 | 0 | 0 |
| Visibility(mi) | [0; 20] | 0 | 80 | 98 | 0.2293 |
| Wind_Speed(mph) | [0; 120] | 0 | 232 | 1 | 0.0023 |
| Precipitation(in) | [0; 10] | 0 | 9.99 | 0 | 0 |
| Start_Lat | [24; 50] | 24.5748 | 48.9976 | 0 | 0 |
| Start_Lng | [-125; -66] | -124.486 | -68.366 | 0 | 0 |


## 7. Утечка данных в Description


### Показатели по массовым суффиксам

Учитываются суффиксы, встречающиеся не менее 20 раз. Единичные суффиксы исключены: их чистота равна 100% по построению.

| Показатель | Значение |
| --- | --- |
| Порог массовости суффикса, записей | 20 |
| Уникальных суффиксов всего | 16900 |
| Массовых суффиксов | 123 |
| Записей под массовыми суффиксами | 17833 |
| Покрытие датасета массовыми суффиксами, % | 41.72 |
| Массовых суффиксов с чистотой >= 95% | 20 |
| Записей под ними | 3958 |
| Доля датасета под ними, % | 9.26 |


### Массовые суффиксы и распределение классов

lift — отношение доли класса внутри суффикса к его доле в датасете.

| Последние 3 слова | Записей | Мажоритарный класс | Чистота, % | Severity 1 | Severity 2 | Severity 3 | Severity 4 | lift мажоритарного |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| due to accident | 3110 | 2 | 50.29 | 0 | 1564 | 196 | 1350 | 0.69 |
| drive with caution | 2668 | 2 | 100 | 0 | 2668 | 0 | 0 | 1.37 |
| rd - accident | 1647 | 2 | 85 | 60 | 1400 | 184 | 3 | 1.16 |
| ave - accident | 987 | 2 | 83.79 | 59 | 827 | 99 | 2 | 1.15 |
| st - accident | 818 | 2 | 84.11 | 26 | 688 | 101 | 3 | 1.15 |
| left lane blocked | 811 | 2 | 82.86 | 7 | 672 | 124 | 8 | 1.13 |
| right lane blocked | 673 | 2 | 75.19 | 17 | 506 | 141 | 9 | 1.03 |
| blvd - accident | 661 | 2 | 87.29 | 28 | 577 | 56 | 0 | 1.19 |
| accident. lane blocked | 407 | 2 | 80.59 | 0 | 328 | 71 | 8 | 1.1 |
| dr - accident | 320 | 2 | 85 | 19 | 272 | 28 | 1 | 1.16 |
| hard shoulder blocked | 277 | 2 | 54.15 | 78 | 150 | 40 | 9 | 0.74 |
| expect long delays | 273 | 2 | 100 | 0 | 273 | 0 | 0 | 1.37 |
| fwy - accident | 260 | 2 | 91.92 | 4 | 239 | 15 | 2 | 1.26 |
| take alternate route | 248 | 2 | 70.16 | 0 | 174 | 0 | 74 | 0.96 |
| blocked. expect delays | 207 | 2 | 100 | 0 | 207 | 0 | 0 | 1.37 |
| hwy - accident | 206 | 2 | 85.92 | 9 | 177 | 19 | 1 | 1.18 |
| two lanes blocked | 185 | 3 | 73.51 | 2 | 31 | 136 | 16 | 3.38 |
| rd expect delays | 135 | 2 | 100 | 0 | 135 | 0 | 0 | 1.37 |
| right shoulder closed | 122 | 2 | 100 | 0 | 122 | 0 | 0 | 1.37 |
| center lane blocked | 96 | 2 | 65.62 | 2 | 63 | 30 | 1 | 0.9 |
| ln - accident | 93 | 2 | 86.02 | 4 | 80 | 9 | 0 | 1.18 |
| on the median | 84 | 2 | 52.38 | 0 | 44 | 40 | 0 | 0.72 |
| pky - accident | 83 | 2 | 81.93 | 2 | 68 | 13 | 0 | 1.12 |
| ave expect delays | 82 | 2 | 100 | 0 | 82 | 0 | 0 | 1.37 |
| no recent updates | 82 | 2 | 91.46 | 0 | 75 | 7 | 0 | 1.25 |


## 8. Нормализация категорий


### Группы Weather_Condition

| Группа | Записей | Доля, % |
| --- | --- | --- |
| cloudy | 18824 | 44.04 |
| clear | 17646 | 41.28 |
| rain | 2980 | 6.97 |
| low_visibility | 1119 | 2.62 |
| unknown | 1079 | 2.52 |
| snow | 773 | 1.81 |
| storm | 323 | 0.76 |


### Соответствие значений группам

| Группа | Исходное значение | Записей |
| --- | --- | --- |
| clear | Fair | 10117 |
| clear | Clear | 7404 |
| clear | Fair / Windy | 125 |
| cloudy | Mostly Cloudy | 5788 |
| cloudy | Partly Cloudy | 4033 |
| cloudy | Cloudy | 3454 |
| cloudy | Overcast | 3451 |
| cloudy | Scattered Clouds | 1896 |
| cloudy | Cloudy / Windy | 77 |
| cloudy | Mostly Cloudy / Windy | 71 |
| cloudy | Partly Cloudy / Windy | 54 |
| low_visibility | Fog | 488 |
| low_visibility | Haze | 463 |
| low_visibility | Smoke | 82 |
| low_visibility | Patches of Fog | 36 |
| low_visibility | Mist | 20 |
| low_visibility | Shallow Fog | 14 |
| low_visibility | Haze / Windy | 9 |
| low_visibility | Fog / Windy | 2 |
| low_visibility | Widespread Dust | 2 |
| low_visibility | Blowing Dust / Windy | 1 |
| low_visibility | Partial Fog | 1 |
| low_visibility | Smoke / Windy | 1 |
| rain | Light Rain | 2096 |
| rain | Rain | 481 |
| rain | Heavy Rain | 176 |
| rain | Light Drizzle | 131 |
| rain | Light Rain / Windy | 36 |
| rain | Drizzle | 32 |
| rain | Rain / Windy | 9 |
| rain | Heavy Rain / Windy | 8 |
| rain | Showers in the Vicinity | 4 |
| rain | Light Rain Shower | 3 |
| rain | Heavy Drizzle | 2 |
| rain | Drizzle and Fog | 1 |
| rain | Light Drizzle / Windy | 1 |
| snow | Light Snow | 609 |
| snow | Snow | 66 |
| snow | Heavy Snow | 25 |
| snow | Light Freezing Rain | 23 |
| snow | Light Snow / Windy | 18 |
| snow | Light Freezing Fog | 8 |
| snow | Snow / Windy | 5 |
| snow | Blowing Snow | 4 |
| snow | Light Freezing Drizzle | 4 |
| snow | Light Ice Pellets | 3 |
| snow | Sleet | 2 |
| snow | Heavy Ice Pellets | 1 |
| snow | Ice Pellets | 1 |
| snow | Light Blowing Snow | 1 |
| snow | Low Drifting Snow | 1 |
| snow | Small Hail | 1 |
| snow | Snow and Sleet | 1 |
| storm | Light Thunderstorms and Rain | 51 |
| storm | T-Storm | 43 |
| storm | Thunder in the Vicinity | 40 |
| storm | Light Rain with Thunder | 39 |
| storm | Thunderstorm | 37 |
| storm | Thunder | 34 |
| storm | Heavy T-Storm | 29 |
| storm | Heavy Thunderstorms and Rain | 24 |
| storm | Thunderstorms and Rain | 21 |
| storm | Heavy T-Storm / Windy | 2 |
| storm | Heavy Thunderstorms and Snow | 1 |
| storm | Squalls / Windy | 1 |
| storm | T-Storm / Windy | 1 |
| unknown | (пропуск) | 1056 |
| unknown | Wintry Mix | 22 |
| unknown | N/A Precipitation | 1 |


### Wind_Direction после нормализации

| Значение | Записей | Доля, % |
| --- | --- | --- |
| CALM | 7490 | 17.52 |
| S | 3221 | 7.54 |
| W | 3058 | 7.15 |
| N | 2775 | 6.49 |
| WNW | 2168 | 5.07 |
| E | 2124 | 4.97 |
| VAR | 2042 | 4.78 |
| SSW | 2033 | 4.76 |
| NW | 1994 | 4.66 |
| WSW | 1963 | 4.59 |
| SW | 1953 | 4.57 |
| SSE | 1899 | 4.44 |
| NNW | 1868 | 4.37 |
| SE | 1511 | 3.53 |
| ENE | 1458 | 3.41 |
| ESE | 1434 | 3.35 |
| NNE | 1424 | 3.33 |
| NE | 1405 | 3.29 |
| UNKNOWN | 924 | 2.16 |


## 9. Различимость классов


### Медианы числовых признаков по классам

| Severity | Temperature(F) | Visibility(mi) | Wind_Speed(mph) |
| --- | --- | --- | --- |
| 1 | 72.5 | 10 | 8 |
| 2 | 62.1 | 10 | 7 |
| 3 | 64 | 10 | 8 |
| 4 | 61 | 10 | 7 |


### Хвосты распределений

Доля класса внутри подмножества и lift к базовой доле.

| Условие | Записей | Доля выборки, % | Доля 1, % | Доля 2, % | Доля 3, % | Доля 4, % | lift 1 | lift 2 | lift 3 | lift 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Visibility < 5 | 3287 | 7.69 | 0.46 | 71.68 | 23.36 | 4.5 | 0.45 | 0.98 | 1.07 | 1.09 |
| Visibility < 1 | 562 | 1.31 | 0.53 | 74.91 | 17.97 | 6.58 | 0.53 | 1.02 | 0.83 | 1.6 |
| Temperature < 32 | 2833 | 6.63 | 0.07 | 71.34 | 22.77 | 5.82 | 0.07 | 0.98 | 1.05 | 1.42 |
| Wind_Speed > 20 | 794 | 1.86 | 0.88 | 73.3 | 21.66 | 4.16 | 0.87 | 1 | 1 | 1.01 |
| Humidity > 90 | 5861 | 13.71 | 0.58 | 73.11 | 21.26 | 5.05 | 0.57 | 1 | 0.98 | 1.23 |


### Группы погоды

| Группа | Записей | Доля 1, % | Доля 2, % | Доля 3, % | Доля 4, % | lift 1 | lift 2 | lift 3 | lift 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cloudy | 18824 | 0.84 | 71.61 | 23.54 | 4.01 | 0.83 | 0.98 | 1.08 | 0.98 |
| clear | 17646 | 1.31 | 75.56 | 19.01 | 4.11 | 1.29 | 1.03 | 0.87 | 1 |
| rain | 2980 | 1.04 | 70.5 | 24.8 | 3.66 | 1.03 | 0.96 | 1.14 | 0.89 |
| low_visibility | 1119 | 0.54 | 78.19 | 17.96 | 3.31 | 0.53 | 1.07 | 0.83 | 0.8 |
| unknown | 1079 | 0.28 | 71.83 | 22.06 | 5.84 | 0.27 | 0.98 | 1.01 | 1.42 |
| snow | 773 | 0.39 | 63 | 29.5 | 7.12 | 0.38 | 0.86 | 1.36 | 1.73 |
| storm | 323 | 0.31 | 61.61 | 34.06 | 4.02 | 0.31 | 0.84 | 1.56 | 0.98 |


### Интервалы суток

| Группа | Записей | Доля 1, % | Доля 2, % | Доля 3, % | Доля 4, % | lift 1 | lift 2 | lift 3 | lift 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3_day | 12686 | 1.15 | 72.81 | 22.13 | 3.9 | 1.14 | 1 | 1.02 | 0.95 |
| 1_rush_morning | 8554 | 0.62 | 74.47 | 21.95 | 2.96 | 0.61 | 1.02 | 1.01 | 0.72 |
| 2_rush_evening | 8475 | 1.59 | 70.03 | 24.67 | 3.71 | 1.57 | 0.96 | 1.13 | 0.9 |
| 5_night | 7540 | 0.61 | 75.12 | 18.63 | 5.64 | 0.6 | 1.03 | 0.86 | 1.37 |
| 4_evening | 4946 | 1.07 | 71.15 | 22.62 | 5.16 | 1.06 | 0.97 | 1.04 | 1.25 |
| unknown | 543 | 0 | 96.87 | 0.18 | 2.95 | 0 | 1.32 | 0.01 | 0.72 |


### Время суток (Sunrise_Sunset)

| Группа | Записей | Доля 1, % | Доля 2, % | Доля 3, % | Доля 4, % | lift 1 | lift 2 | lift 3 | lift 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Day | 28691 | 1.24 | 72.17 | 22.97 | 3.62 | 1.22 | 0.99 | 1.06 | 0.88 |
| Night | 14049 | 0.55 | 75.02 | 19.31 | 5.12 | 0.54 | 1.03 | 0.89 | 1.24 |


### Штаты

| Группа | Записей | Доля 1, % | Доля 2, % | Доля 3, % | Доля 4, % | lift 1 | lift 2 | lift 3 | lift 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA | 10785 | 0.75 | 79.11 | 19.01 | 1.13 | 0.74 | 1.08 | 0.87 | 0.28 |
| FL | 3839 | 1.17 | 77.47 | 17.82 | 3.54 | 1.16 | 1.06 | 0.82 | 0.86 |
| TX | 3456 | 0.46 | 71.24 | 25.95 | 2.34 | 0.46 | 0.97 | 1.19 | 0.57 |
| NY | 1907 | 0.79 | 65.44 | 28.16 | 5.61 | 0.78 | 0.9 | 1.29 | 1.36 |
| NC | 1853 | 1.3 | 83.54 | 11.98 | 3.18 | 1.28 | 1.14 | 0.55 | 0.77 |
| SC | 1673 | 0.18 | 83.68 | 15.12 | 1.02 | 0.18 | 1.14 | 0.69 | 0.25 |
| OR | 1401 | 1.36 | 88.37 | 6.07 | 4.21 | 1.34 | 1.21 | 0.28 | 1.02 |
| VA | 1354 | 1.62 | 64.92 | 25.7 | 7.75 | 1.6 | 0.89 | 1.18 | 1.89 |
| PA | 1314 | 0.08 | 76.94 | 16.36 | 6.62 | 0.08 | 1.05 | 0.75 | 1.61 |
| MN | 1152 | 0.09 | 78.3 | 20.75 | 0.87 | 0.09 | 1.07 | 0.95 | 0.21 |
| IL | 1152 | 0.17 | 56.94 | 38.89 | 3.99 | 0.17 | 0.78 | 1.79 | 0.97 |
| GA | 984 | 0.41 | 48.58 | 40.04 | 10.98 | 0.4 | 0.66 | 1.84 | 2.67 |
| MI | 948 | 0.21 | 62.55 | 29.22 | 8.02 | 0.21 | 0.86 | 1.34 | 1.95 |
| AZ | 944 | 11.12 | 68.64 | 13.77 | 6.46 | 10.98 | 0.94 | 0.63 | 1.57 |
| TN | 808 | 2.6 | 72.52 | 22.03 | 2.85 | 2.57 | 0.99 | 1.01 | 0.69 |
| NJ | 756 | 0.26 | 67.59 | 22.62 | 9.52 | 0.26 | 0.92 | 1.04 | 2.32 |
| LA | 756 | 3.44 | 78.17 | 16.4 | 1.98 | 3.39 | 1.07 | 0.75 | 0.48 |
| MD | 754 | 0.66 | 59.68 | 25.2 | 14.46 | 0.65 | 0.82 | 1.16 | 3.51 |
| WA | 691 | 1.16 | 62.95 | 31.69 | 4.2 | 1.14 | 0.86 | 1.46 | 1.02 |
| OH | 669 | 1.05 | 61.29 | 25.86 | 11.81 | 1.03 | 0.84 | 1.19 | 2.87 |
| UT | 633 | 1.11 | 80.25 | 15.8 | 2.84 | 1.09 | 1.1 | 0.73 | 0.69 |
| CO | 552 | 1.81 | 46.2 | 43.12 | 8.88 | 1.79 | 0.63 | 1.98 | 2.16 |
| OK | 483 | 0 | 87.16 | 11.8 | 1.04 | 0 | 1.19 | 0.54 | 0.25 |
| AL | 473 | 0.21 | 73.15 | 25.16 | 1.48 | 0.21 | 1 | 1.16 | 0.36 |
| MO | 444 | 0 | 54.28 | 38.74 | 6.98 | 0 | 0.74 | 1.78 | 1.7 |
| CT | 390 | 0.26 | 62.31 | 27.69 | 9.74 | 0.25 | 0.85 | 1.27 | 2.37 |
| MA | 385 | 0.26 | 64.94 | 33.77 | 1.04 | 0.26 | 0.89 | 1.55 | 0.25 |
| IN | 355 | 0 | 60.28 | 28.45 | 11.27 | 0 | 0.82 | 1.31 | 2.74 |
| KY | 222 | 0.45 | 54.05 | 39.19 | 6.31 | 0.44 | 0.74 | 1.8 | 1.53 |
| WI | 206 | 0.49 | 40.29 | 36.41 | 22.82 | 0.48 | 0.55 | 1.67 | 5.55 |
| NE | 201 | 0 | 80.1 | 17.91 | 1.99 | 0 | 1.1 | 0.82 | 0.48 |
| IA | 147 | 0 | 59.86 | 30.61 | 9.52 | 0 | 0.82 | 1.41 | 2.32 |
| NV | 128 | 0 | 74.22 | 23.44 | 2.34 | 0 | 1.02 | 1.08 | 0.57 |
| RI | 110 | 0.91 | 48.18 | 49.09 | 1.82 | 0.9 | 0.66 | 2.26 | 0.44 |
| KS | 106 | 0 | 64.15 | 27.36 | 8.49 | 0 | 0.88 | 1.26 | 2.06 |
| DC | 104 | 0.96 | 75 | 10.58 | 13.46 | 0.95 | 1.03 | 0.49 | 3.27 |
| NH | 88 | 0 | 84.09 | 14.77 | 1.14 | 0 | 1.15 | 0.68 | 0.28 |
| AR | 80 | 0 | 80 | 6.25 | 13.75 | 0 | 1.09 | 0.29 | 3.34 |
| MS | 80 | 0 | 58.75 | 32.5 | 8.75 | 0 | 0.8 | 1.49 | 2.13 |
| DE | 69 | 0 | 60.87 | 13.04 | 26.09 | 0 | 0.83 | 0.6 | 6.34 |
| ID | 66 | 0 | 92.42 | 1.52 | 6.06 | 0 | 1.26 | 0.07 | 1.47 |
| NM | 63 | 0 | 77.78 | 17.46 | 4.76 | 0 | 1.06 | 0.8 | 1.16 |
| MT | 54 | 0 | 94.44 | 3.7 | 1.85 | 0 | 1.29 | 0.17 | 0.45 |
| WV | 49 | 0 | 75.51 | 14.29 | 10.2 | 0 | 1.03 | 0.66 | 2.48 |
| ME | 38 | 0 | 92.11 | 0 | 7.89 | 0 | 1.26 | 0 | 1.92 |
