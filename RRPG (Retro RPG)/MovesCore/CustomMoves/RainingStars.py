import MovesCore.Moves as M

class RainingStars(M.Moves):
    def __init__(self):
        super().__init__()
        super().__init_subclass__()
        self.MoveId = "magic:raining_stars"
        self.MoveName = "Raining Stars"
        self.Description = "Calls down a shower of magical stars to strike all enemies."
        self.MoveBaseDamage = 15
        self.MoveBaseStaminaCost = 5
        self.MoveCooldown = 3
        self.MoveType = "Stellar"
        # Additional effects can be added here, such as status effects or area damage.