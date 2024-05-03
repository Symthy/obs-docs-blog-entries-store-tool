from __future__ import annotations

from typing import List

from entries.values.category_path import CategoryPath


class CategoryGroup:
    """
    直下のカテゴリまでを保持するクラス
    - 末端のカテゴリは children が空
    """

    def __init__(self, category_path: CategoryPath, category_children: List[CategoryGroup] = None):
        self.__category_name = category_path.end
        self.__category_path = category_path
        self.__children: List[CategoryGroup] = [] if category_children is None else category_children

    @property
    def category_name(self) -> str:
        return self.__category_name

    @property
    def sub_categories(self) -> List[str]:
        return [child.category_name for child in self.__children]

    def find_category_path(self, category_path: CategoryPath) -> bool:
        if self.__category_path == category_path:
            return True
        if not self.__category_path.starts_with(category_path):
            return False
        for sub_category_group in self.__children:
            if sub_category_group.find_category_path(category_path):
                return True
        return False

    def category_paths(self, parent_category_path: CategoryPath = None) -> List[CategoryPath]:
        """
        フルパスの category_path のみ取得。途中階層のパスは含めない
        """
        current_category_path = parent_category_path.join(self.category_name) \
            if parent_category_path is not None else CategoryPath(self.category_name)
        if len(self.sub_categories) == 0:
            return [current_category_path]
        category_paths = []
        for child in self.__children:
            category_paths += child.category_paths(current_category_path)
        return category_paths
