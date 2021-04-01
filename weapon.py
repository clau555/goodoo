from collectable import Collectable


class Weapon(Collectable):

    MELEE = 0
    RANGE = 1

    def __init__(self, pos: tuple[int, int], sprite: str, weapon_type: int, recoil: int = 0) -> None:
        super(Weapon, self).__init__(pos, sprite)
        self.type: int = weapon_type
        self.recoil: int = recoil

    def action(self) -> None:
        # TODO weapon action
        print("weapon action")
