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
