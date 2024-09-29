> **We can play with Strategy settings like the ticker and constants to see if we get better results**

- **Strategy (TF = 1h, WINDOW = 7)**
```
if(CMP > MA(High) + 2STD(High)) 
    sell with SL == TP == 1STD(High)
if(CMP < MA(LOW) - 2STD(LOW)) 
    buy with SL == TP == 1STD(LOW)
```

> **strategy written in pinescript should not be taken into consideration**

> **Python gives more flexibility and can be relied on when backtesting or implementing strategies (better than pine script)**