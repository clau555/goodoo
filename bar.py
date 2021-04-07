from config import TILE_SCALE
from displayable import Displayable


class Bar(Displayable):

    def __init__(self, pos: tuple[int, int], color: tuple[int, int, int]) -> None:
        self.__total_width: float = TILE_SCALE * 2 / 3
        super(Bar, self).__init__(pos, (0, TILE_SCALE // 10), color)
        self.rect.center = pos  # centers the bar at pos immediately
        self.__progress: float = 0.
        self.set_display(False)

    def set_progress(self, progress: float) -> None:
        # the bar is displayed only if it's not full or empty
        if progress <= 0.:
            self.__progress = 0.
            self.set_display(False)
        elif progress >= 1.:
            self.__progress = 1.
            self.set_display(False)
        else:
            self.__progress = progress
            self.rect.width = int(self.__progress * self.__total_width)
            self.set_display(True)
