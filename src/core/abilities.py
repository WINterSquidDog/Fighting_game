import abc

class Ability(abc.ABC):
    """
    Абстракция способности
    """
    def __init__(self, meter_cost=1):
        self.meter_cost = meter_cost
    
    def activate(self, user, target):
        """
        Использование способности
        """
        pass