from constants import TILE_SCALE
from displayable import Displayable


class Bar(Displayable):

    def __init__(self, pos: tuple[int, int]) -> None:
        self.__total_width: float = TILE_SCALE * 2 / 3
        super(Bar, self).__init__(pos, (0, TILE_SCALE / 10), (255, 255, 255))
        self.__progress: float = 0
        self.set_display(False)

    def set_progress(self, progress: float) -> None:
        if progress < 0:
            self.__progress = 0
            self.set_display(False)
        elif progress > 1:
            self.__progress = 1
            self.set_display(False)
        else:
            self.__progress = progress
            self.rect.width = int(self.__progress * self.__total_width)
            self.set_display(True)
