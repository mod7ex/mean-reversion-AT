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
````
// TF = 1h, WINDOW = 7
if(CMP > MA(High) + 2STD) 
    sell with SL == TP == 1STD
if(CMP < MA(High) - 2STD) 
    buy with SL == TP == 1STD
```