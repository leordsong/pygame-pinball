from objects.Circle import Circle


class Ball(Circle):
    bounciness = 0.8

    def __init__(self, x, y, r, color, img=None, name="ball"):
        super().__init__(x, y, r, color, [0, 0], name)
        self.img = img

    def draw(self, ctx):
        if self.img is not None:
            ctx.blit(self.img, (int(self.x) - self.r, int(self.y) - self.r))
        else:
            super().draw(ctx)
