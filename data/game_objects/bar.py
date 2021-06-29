from data.game_objects.displayable import Displayable
from data.constants import TILE_SCALE


class Bar(Displayable):

    def __init__(self, pos: tuple[int, int], color: tuple[int, int, int]) -> None:
        self.__total_width: float = TILE_SCALE * 2 / 3
        super(Bar, self).__init__(pos, (0, TILE_SCALE // 10), color)
        self.rect.center = pos  # centers the bar at pos immediately
        self.__progress: float = 0.  # varies from 0 to 1, 0 is an empty bar, 1 is a full bar
        self.visible = False

    @property
    def progress(self) -> float:
        return self.__progress

    @progress.setter
    def progress(self, progress: float) -> None:
        # the bar is displayed only if it's not full or empty
        if progress <= 0.:
            self.__progress = 0.
            self.visible = False
        elif progress >= 1.:
            self.__progress = 1.
            self.visible = False
        else:
            self.__progress = progress
            self.rect.width = int(self.__progress * self.__total_width)
            self.visible = True
