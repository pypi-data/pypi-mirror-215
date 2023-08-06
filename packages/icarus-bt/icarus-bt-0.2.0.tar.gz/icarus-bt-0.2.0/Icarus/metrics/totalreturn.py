class TotalReturn:
    """
    Calculates the total return of a stock
    
    Attributes
        initial_value (float): The initial value of the stock
        final_value (float): The final value of the stock"""
    def __init__(self, initial_value, final_value):
        self.initial_value = initial_value
        self.final_value = final_value

    def calculate(self):
        """
        Calculates the total return of a stock
        """
        total_return = ((self.final_value - self.initial_value) / self.initial_value)*100
        return total_return
