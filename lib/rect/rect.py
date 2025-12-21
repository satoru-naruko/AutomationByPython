class Rect:
    """
    画面上の矩形領域を表すクラス
    """
    def __init__(self, start_x=100, start_y=100, end_x=200, end_y=200):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    @property
    def width(self):
        """矩形の幅を返す"""
        return self.end_x - self.start_x

    @property
    def height(self):
        """矩形の高さを返す"""
        return self.end_y - self.start_y

    @classmethod
    def from_dict(cls, data):
        """
        辞書からRectインスタンスを作成

        :param data: start_x, start_y, end_x, end_y を含む辞書
        :return: Rectインスタンス
        """
        if data is None:
            return cls()

        return cls(
            start_x=data.get("start_x", 100),
            start_y=data.get("start_y", 100),
            end_x=data.get("end_x", 200),
            end_y=data.get("end_y", 200)
        )

    def to_region_tuple(self):
        """
        ScreenComparatorで使用する形式 (x, y, width, height) のタプルを返す

        :return: (start_x, start_y, width, height) のタプル
        """
        return (self.start_x, self.start_y, self.width, self.height)
