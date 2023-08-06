# Importing NumPy as "np"
import numpy as np

class Multiplication:

    def __init__(self, multiplier):
        self.multiplier = multiplier

    def multiply(self, number):
        
        # Using NumPy .dot() to multiply the numbers
        return np.dot(number, self.multiplier)
    
class Addition:
    def __init__(self, add_by):
        self.add_by = add_by
    
    def add(self, number):
        return number + self.add_by
