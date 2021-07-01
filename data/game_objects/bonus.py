from data.game_objects.collectable import Collectable


class Bonus(Collectable):
    """
    A bonus is a collectable object that can be picked up by an entity.\n
    It adds a certain value of health points to the entity when picked up.\n
    """

    def __init__(self, pos: tuple[int, int], sprite: str, value: int) -> None:
        super(Bonus, self).__init__(pos, sprite, auto_grab=True)
        self.__value: int = value  # health to add to an entity when taken

    @property
    def value(self) -> int:
        return self.__value
