from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QStyle,
    QWidget,
)
from PyQt6.QtCore import pyqtSignal
from karoto.flow_layout import FlowLayout


class Tag(QPushButton):
    deleted = pyqtSignal()

    def __init__(self, name: str, count: int = None, cross=True) -> None:
        super().__init__()

        self.name = name
        self.setText(name if count is None else f"{name} ({count})")

        if cross:
            pixmapi = QStyle.StandardPixmap.SP_DialogCloseButton
            icon = self.style().standardIcon(pixmapi)
            self.setIcon(icon)

        self.clicked.connect(self.deleted)


class TagWizzard(QWidget):
    created_tag = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        self.plus_button = QPushButton("+")
        self.plus_button.clicked.connect(self.toggle)
        self.plus_button.setProperty("class", "single_char_button")

        self.name_edit = QLineEdit()
        self.name_edit.returnPressed.connect(self.ready)
        self.name_edit.setHidden(True)

        self.confirm_button = QPushButton(">")
        self.confirm_button.clicked.connect(self.ready)
        self.confirm_button.setHidden(True)
        self.confirm_button.setProperty("class", "single_char_button")

        self.layout_ = QHBoxLayout()
        self.layout_.addWidget(self.plus_button)
        self.layout_.addWidget(self.name_edit)
        self.layout_.addWidget(self.confirm_button)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_)

    def toggle(self) -> None:
        self.plus_button.setHidden(not self.plus_button.isHidden())
        self.name_edit.setHidden(not self.name_edit.isHidden())
        self.confirm_button.setHidden(not self.confirm_button.isHidden())

        self.name_edit.setFocus()

    def ready(self) -> None:
        name = self.name_edit.text()
        if name == "":
            self.toggle()
            return
        self.created_tag.emit(name)


class Tags(QWidget):
    deleted_tag = pyqtSignal(str)
    created_tag = pyqtSignal(str)

    def __init__(self, tags: list[str]) -> None:
        super().__init__()
        self.tags = tags
        self.init_ui()

    def init_ui(self) -> None:
        self.layout_ = FlowLayout()
        for name in self.tags:
            t = Tag(name=name)
            t.deleted.connect(
                    lambda x=name: self.deleted_tag.emit(x)
            )
            self.layout_.addWidget(t)
        self.wizzard = TagWizzard()
        self.wizzard.created_tag.connect(self.created_tag)
        self.layout_.addWidget(self.wizzard)

        self.setLayout(self.layout_)


class TagFilter(QWidget):
    changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.all_tags = []
        self.filter_tags = []

        self.init_ui()

    def init_ui(self) -> None:
        self.layout_ = FlowLayout()
        self.setLayout(self.layout_)

    def show_tags(self, add_another=False) -> None:
        self.clear_layout()

        for filter_tag in self.filter_tags:
            t = Tag(name=filter_tag)
            t.deleted.connect(lambda x=filter_tag: self.remove_filter(x))
            self.layout_.addWidget(t)

        if self.filter_tags != [] and not add_another:
            add_button = QPushButton("+")
            add_button.setProperty("class", "single_char_button")
            add_button.clicked.connect(
                lambda: self.show_tags(add_another=True)
            )
            self.layout_.addWidget(add_button)
            return

        for name, count in self.all_tags:
            if name in self.filter_tags:
                continue

            t = Tag(name=name, count=count, cross=False)
            t.deleted.connect(lambda x=name: self.add_filter(x))
            self.layout_.addWidget(t)

    def clear_layout(self) -> None:
        while not self.layout_.isEmpty():
            del_item = self.layout_.itemAt(0)
            self.layout_.removeItem(del_item)
            del_item.widget().deleteLater()

    def update_all_tags(self, all_tags: list[tuple[str, int]]) -> None:
        self.all_tags = all_tags
        self.show_tags()

    def add_filter(self, name: str) -> None:
        self.filter_tags.append(name)
        self.changed.emit()

    def remove_filter(self, name: str) -> None:
        self.filter_tags.remove(name)
        self.changed.emit()
