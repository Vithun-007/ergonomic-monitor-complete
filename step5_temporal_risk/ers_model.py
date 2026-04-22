class ERSModel:
    def __init__(self):
        self.current_score = 5.0
        self.decay = 0.92

    def update(self, rula):
        if rula <= 2:
            self.current_score *= self.decay
        else:
            self.current_score += (rula - 2) * 0.3

        self.current_score = max(0.0, min(20.0, self.current_score))
        return self.current_score