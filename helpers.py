class Trade:
    def __init__(self, entry = 0.0, tp = 0.0, sl = 0.0, on = False):
        # Private variables
        self._on = on
        self._entry = entry
        self._tp = tp
        self._sl = sl

    @property
    def entry(self):
        """Getter for entry."""
        return self._entry

    @property
    def tp(self):
        """Getter for tp."""
        return self._tp

    @property
    def sl(self):
        """Getter for sl."""
        return self._sl
    
    @property
    def on(self):
        """Getter for on."""
        return self._on
    
    # Computed properties
    @property
    def is_buy(self):
        return self._tp > self._sl
    
    @property
    def is_sell(self):
        return self._tp < self._sl

    @entry.setter
    def entry(self, value):
        if isinstance(value, float) or isinstance(value, int) :
            if self._on:
                self._entry = value
        else:
            raise ValueError("Entry must be a floating number")

    @tp.setter
    def tp(self, value):
        if isinstance(value, float) or isinstance(value, int) :
            if self._on:
                self._tp = value
        else:
            raise ValueError("TP must be a floating number")

    @sl.setter
    def sl(self, value):
        if isinstance(value, float) or isinstance(value, int) :
            if self._on:
                self._sl = value
        else:
            raise ValueError("SL must be a floating number")
        
    @on.setter
    def on(self, value):
        if isinstance(value, bool):
            if not value: 
                self._entry = 0
                self._tp = 0
                self._sl = 0

            self._on = value
        else:
            raise ValueError("On must be a boolean")