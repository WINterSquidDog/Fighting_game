class Cameo:
    """Персонаж-камео."""
    def __init__(self, name: str, unique_ability, breaker_ability):
        self.name = name
        self.unique_ability = unique_ability
        self.breaker_ability = breaker_ability
    
    def use_unique(self, user, target):
        """
        Использование уникальной атаки камео
        """
        return self.unique_ability.activate(user, target)

    def use_breaker(self, user, target, stats):
        """
        Использование брейкера
        """
        if stats.spend_meter(3):
            return self.breaker_ability.activate(user, target)
        return False