class Trade:
    def __init__(self, entry = 0.0, tp = 0.0, sl = 0.0, on = False):
        # Private variables
        self.__on = on
        self.__entry = entry
        self.__tp = tp
        self.__sl = sl

    @property
    def entry(self):
        """Getter for entry."""
        return self.__entry

    @property
    def tp(self):
        """Getter for tp."""
        return self.__tp

    @property
    def sl(self):
        """Getter for sl."""
        return self.__sl
    
    @property
    def on(self):
        """Getter for on."""
        return self.__on
    
    # Computed properties
    @property
    def is_buy(self):
        return self.__tp > self.__sl
    
    @property
    def is_sell(self):
        return self.__tp < self.__sl

    @entry.setter
    def entry(self, value):
        if isinstance(value, float | int):
            if self.__on:
                self.__entry = value
        else:
            raise ValueError("Entry is invalid")

    @tp.setter
    def tp(self, value):
        if isinstance(value, float | int):
            if self.__on:
                self.__tp = value
        else:
            raise ValueError("TP is invalid")

    @sl.setter
    def sl(self, value):
        if isinstance(value, float | int):
            if self.__on:
                self.__sl = value
        else:
            raise ValueError("SL is invalid")
        
    def On(self):
        self.__on = True
    
    def Off(self):
        self.__entry = 0
        self.__tp = 0
        self.__sl = 0
        self.__on = False