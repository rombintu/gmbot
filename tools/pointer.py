class Pointer:
    def __init__(self, size_a):
        self.size_a = size_a

    def to_center(self, size_b = (0, 0), plus_w = 0, plus_h = 0):
        return (
            (self.size_a[0] - size_b[0]) // 2 + plus_w,
            (self.size_a[1] - size_b[1]) // 2 + plus_h
        )

    def to_right(self, size_b = (0, 0), plus_w = 0, plus_h = 0):
        return (
            self.size_a[0] - size_b[0] - 10 + plus_w,
            (self.size_a[1] - size_b[1]) // 2 + plus_h
        )

    def to_left(self, size_b = (0, 0), plus_w = 0, plus_h = 0):
        return (
            10 + plus_w,
            (self.size_a[1] - size_b[1]) // 2 + plus_h
        )
    def to_top(self, size_b = (0, 0), plus_w = 0, plus_h = 0):
        return (
            (self.size_a[0] - size_b[0]) // 2 + plus_w,
            10 + plus_h
        )
    
    def to_bottom(self, size_b = (0, 0), plus_w = 0, plus_h = 0):
        return (
            (self.size_a[0] - size_b[0]) // 2 + plus_w,
            self.size_a[1] - size_b[1] - 10 - 25 + plus_h
        )
