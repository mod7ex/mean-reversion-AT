### We can play with Strategy settings like the ticker and constants to see if we get better results

> **Till now the best Params found for `ticker=GC=F` are the following**

```py
STD_FACTORS = {
    'ENTRY': 2,
    'SL': 1, # is calculated from entry
    'TP': 1 # is calculated from entry
}
```

### Strategy 
```
// TF = 1h, WINDOW = 7
if(CMP > MA(High) + 2STD(High)) 
    sell with SL == TP == 1STD(High)
if(CMP < MA(LOW) - 2STD(LOW)) 
    buy with SL == TP == 1STD(LOW)
```

> **strategy written in pinescript should not be taken into consideration**

- [TODO] try also EMA
- [TODO] gather constants in a separate file
- [TODO] work on precision (CFD, Futures) prices, pips ...

### **Python gives more flexibility and can be relied on when backtesting or implementing strategies (better than pine script)**