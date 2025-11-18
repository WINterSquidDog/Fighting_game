class BattleManager:
    """Контроль боя двух персонажей"""
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def update(self, dt):
        self.p1.update(dt)
        self.p2.update(dt)
    
    def check_hit(self, a, d):
        """
        a - атакующий
        d - защищающийся
        """
        if a.rect.colliderect(d.rect):
            print(f"{a.name} hit {d.name}")