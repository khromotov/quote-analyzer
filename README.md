Конечно! Вот версия `README.md` без смайликов — чисто деловая и академичная:

```markdown
# Quote Analyzer

**Quote Analyzer** — это программное средство для анализа котировок акций и генерации торговых сигналов на основе технического и математического анализа.

---

## Возможности
- Загрузка исторических котировок через [Yahoo Finance](https://finance.yahoo.com)
- Расчёт индикаторов: SMA, EMA, MACD, Ichimoku, Z-score, волатильность, Parabolic SAR
- Генерация сигналов BUY / SELL по приоритетной системе
- Оценка доходности стратегии (backtest)
- Визуализация цен и алертов
- Экспорт отчёта в Excel

---

## Установка и запуск

### 1. Клонирование проекта
```bash
git clone https://github.com/khromotov/quote-analyzer.git
cd quote-analyzer
```

### 2. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

> Примечание: если файла `requirements.txt` нет, установите вручную:
```bash
pip install yfinance pandas matplotlib openpyxl
```

### 4. Запуск программы по умолчанию
```bash
python src/run_strategy.py
```

Это выполнит стратегию для тикеров `AAPL`, `MSFT`, `TSLA`, `GOOGL`, `NVDA` с периодом `2023-01-01` по `2024-01-01`.

### 5. Результаты
- В консоли появится информация о доходности
- В папке `reports/` появятся файлы вида `alerts_report_<тикер>.xlsx`
- Отобразится график с точками входа и выхода

---

## Тестирование

```bash
python -m unittest tests/test_pipeline.py
```

Тест проверит работу стратегии на нескольких тикерах, рассчитает доходность и экспортирует тестовые отчёты в `reports/`.

---

## Зависимости
- Python 3.9+
- pandas
- yfinance
- matplotlib
- openpyxl

---

## Обратная связь

Проект разработан студентом БПМИ239 Андреем Хромотовым.  
Буду рад замечаниям и предложениям через [Issues](https://github.com/khromotov/quote-analyzer/issues) или pull requests.
```
