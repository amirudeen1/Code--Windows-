class ComboSystem:
    def __init__(self):
        self.combo = 0
        self.combo_timer = 0
        self.combo_duration = 2000  # 2 seconds to maintain combo
        self.combo_multiplier = 1

    def hit(self, current_time):
        self.combo += 1
        self.combo_timer = current_time
        self.update_multiplier()

    def update(self, current_time):
        if current_time - self.combo_timer > self.combo_duration:
            self.combo = 0
            self.combo_multiplier = 1

    def update_multiplier(self):
        self.combo_multiplier = 1 + (self.combo // 5) * 0.5  # Increase multiplier every 5 hits

    def get_score_multiplier(self):
        return self.combo_multiplier

    def reset(self):
        self.combo = 0
        self.combo_timer = 0
        self.combo_multiplier = 1