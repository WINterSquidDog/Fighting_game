# src/core/stats.py
class Stats:
    """Хранение характеристик персонажа"""
    def __init__(self, hp=1000, meter_max=300):
        self.hp = hp
        self.meter = 0
        self.meter_max = meter_max
    
    def add_meter(self, value):
        """Добавляет энергию, не превышая максимум"""
        self.meter = min(self.meter + value, self.meter_max)
    
    def spend_meter(self, value):
        """Тратит энергию. 
        Возвращает True если энергии хватает.
        Для удобства value - количество делений, в расчетах умножается на meter_max/3.
        """
        segment_cost = value * (self.meter_max // 3)
        if self.meter >= segment_cost:
            self.meter -= segment_cost
            return True
        return False

    def get_segments(self):
        """
        ✅ ИСПРАВЛЕНО: правильная логика определения сегментов
        """
        segment_size = self.meter_max // 3
        if self.meter >= 2 * segment_size:
            return 3
        elif self.meter >= segment_size:
            return 2
        elif self.meter > 0:
            return 1
        else:
            return 0