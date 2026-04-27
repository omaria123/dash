# Отчет: Интерактивный финансовый дашборд в Metabase

## 1. Общий вид дашборда
<img width="1389" height="851" alt="image" src="https://github.com/user-attachments/assets/b9ed094c-8c07-4bf9-8e96-b1cd29ab424c" />
<img width="1498" height="762" alt="image" src="https://github.com/user-attachments/assets/796246e3-63e8-4d7c-8c36-335ce0e8f4fa" />
<img width="1458" height="842" alt="image" src="https://github.com/user-attachments/assets/2aff74ea-67c4-4d51-a63c-2680f2b7e9d1" />

---

## 2. SQL-запросы и визуализации

### 2.1. Анализ кэшбека (1% от суммы)
```sql
SELECT 
    category, 
    SUM(CONVERT(amount, DECIMAL(10, 2)) * 0.01) AS simulated_cashback
FROM bank_transaction
WHERE type = 'Списание'
  [[AND {{category_filter}}]]
  [[AND STR_TO_DATE(transactiondate, '%d.%m.%Y') BETWEEN {{start_date}} AND {{end_date}}]]
GROUP BY category
ORDER BY simulated_cashback DESC;
```
<img width="1419" height="784" alt="image" src="https://github.com/user-attachments/assets/f4aced34-052d-4be1-961e-070df1db994e" />

### 2.2. Суммарный приход/расход по месяцам
```sql
SELECT 
    DATE_FORMAT(STR_TO_DATE(transactiondate, '%d.%m.%Y'), '%Y-%m') as month,
    SUM(CASE WHEN type = 'Списание' THEN CAST(amount AS DECIMAL(10,2)) ELSE 0 END) as outcome,
    SUM(CASE WHEN type != 'Списание' THEN CAST(amount AS DECIMAL(10,2)) ELSE 0 END) as income
FROM bank_transaction
WHERE 1=1 
  [[AND {{category_filter}}]]
  [[AND STR_TO_DATE(transactiondate, '%d.%m.%Y') BETWEEN {{start_date}} AND {{end_date}}]]
GROUP BY month
ORDER BY month;
```
<img width="1400" height="627" alt="image" src="https://github.com/user-attachments/assets/4cfb682b-d818-4b0f-938c-d6668f720049" />

### 2.3. Движение средств
```sql
WITH daily_data AS (
    SELECT 
        STR_TO_DATE(transactiondate, '%d.%m.%Y') AS DT,
        SUM(IF(type = 'Списание', 
               CONVERT(amount, DECIMAL(10, 2)) * -1, 
               CONVERT(amount, DECIMAL(10, 2)))) AS net_amount
    FROM bank_transaction
    WHERE 1=1
      [[AND {{category_filter}}]]
      [[AND STR_TO_DATE(transactiondate, '%d.%m.%Y') BETWEEN {{start_date}} AND {{end_date}}]]
    GROUP BY DT
)
SELECT DT, SUM(net_amount) OVER (ORDER BY DT) AS cumulative_balance
FROM daily_data;
```
<img width="1422" height="640" alt="image" src="https://github.com/user-attachments/assets/2573e913-97de-4d6c-8c73-bc4053af22e4" />

### 2.4. Индикатор среднемесячных трат
```sql
SELECT AVG(monthly_sum) FROM (
    SELECT 
        SUM(CONVERT(amount, DECIMAL(10, 2))) as monthly_sum
    FROM bank_transaction
    WHERE type = 'Списание'
      [[AND {{category_filter}}]]
      [[AND STR_TO_DATE(transactiondate, '%d.%m.%Y') BETWEEN {{start_date}} AND {{end_date}}]]
    GROUP BY DATE_FORMAT(STR_TO_DATE(transactiondate, '%d.%m.%Y'), '%Y-%m')
) AS sub;
```
<img width="965" height="652" alt="image" src="https://github.com/user-attachments/assets/c1f08dfe-3c6d-4913-a30c-8733170031a8" />

### 2.5. Траты по категориям
```sql
SELECT 
    category, 
    SUM(CONVERT(amount, DECIMAL(10, 2)) * 0.01) as total_spent
FROM bank_transaction
WHERE type = 'Списание'
  [[AND {{category_filter}}]]
  [[AND STR_TO_DATE(transactiondate, '%d.%m.%Y') BETWEEN {{start_date}} AND {{end_date}}]]
GROUP BY category;
```
<img width="1267" height="630" alt="image" src="https://github.com/user-attachments/assets/67f757be-3b82-4cab-911c-0b340ef48039" />

### 2.6. Траты по категориям и месяцам
```sql
SELECT 
    DATE_FORMAT(STR_TO_DATE(transactiondate, '%d.%m.%Y'), '%M %Y') as month,
    category,
    SUM(CONVERT(amount, DECIMAL(10, 2))) as total
FROM bank_transaction
WHERE type = 'Списание'
  [[AND {{category_filter}}]]
  [[AND STR_TO_DATE(transactiondate, '%d.%m.%Y') BETWEEN {{start_date}} AND {{end_date}}]]
GROUP BY month, category;
```
<img width="1247" height="627" alt="image" src="https://github.com/user-attachments/assets/b5cd7005-cb70-4ec6-9f37-a55885c5575e" />

---

## 3. Кросс-фильтры
<img width="1846" height="746" alt="image" src="https://github.com/user-attachments/assets/99d996f4-0401-4afb-a4e1-d77910cbcf42" />
<img width="1838" height="741" alt="image" src="https://github.com/user-attachments/assets/ebee4a98-b574-4a7f-a9d3-64babc2d9a38" />

## 4. Фильтры
<img width="1845" height="724" alt="image" src="https://github.com/user-attachments/assets/3babc1a3-23d2-4056-85e9-41bc5cb59a08" />
<img width="1839" height="731" alt="image" src="https://github.com/user-attachments/assets/f3c2a4b4-07fc-4892-9ba6-47abb6916d31" />
<img width="1822" height="803" alt="image" src="https://github.com/user-attachments/assets/b3255460-b359-4e8e-a44a-5af3856c754a" />



