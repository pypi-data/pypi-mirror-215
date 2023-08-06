#!/usr/bin/python3

import sys
from argparse import ArgumentParser
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QIcon, QImage, QPixmap
from karoto.backend import Backend, CartItem, DuplicateError
from karoto.storage_feed import StorageFeed
from karoto.shopping_feed import ShoppingFeed
from karoto.error_bar import ErrorBar
from karoto.tags import TagFilter
from karoto import style


class MainWindow(QWidget):
    def __init__(self, backend: Backend):
        super().__init__()

        self.backend = backend
        self.init_ui()

    def init_ui(self) -> None:
        self.setStyleSheet(style.default)

        topbar = QHBoxLayout()

        self.menu_button = QPushButton()
        self.menu_button.clicked.connect(self.toggle_view)
        self.menu_button.setObjectName("menu_button")
        self.menu_button.setProperty("class", "top_bar")
        topbar.addWidget(self.menu_button)

        self.filter_button = QPushButton()
        self.filter_button.clicked.connect(self.toggle_filter)
        self.filter_button.setProperty("class", "top_bar")
        topbar.addWidget(self.filter_button)

        self.searchfield = QLineEdit()
        self.searchfield.textChanged.connect(lambda: self.refresh())
        self.searchfield.setPlaceholderText("\U0001F50D Search...")
        self.searchfield.setObjectName("search_field")
        self.searchfield.setProperty("class", "top_bar")
        topbar.addWidget(self.searchfield)

        self.tag_filter = TagFilter()
        self.tag_filter.changed.connect(self.refresh)
        self.tag_filter.setHidden(False)
        self.toggle_filter()

        self.error_bar = ErrorBar()
        self.error_bar.setObjectName("error_bar")

        self.shopping_feed = ShoppingFeed()
        self.storage_feed = StorageFeed()

        self.shopping_feed.item_changed.connect(self.on_item_changed)
        self.shopping_feed.warn_message.connect(self.error_bar.show_warning)
        self.shopping_feed.needs_reload.connect(self.refresh)
        self.storage_feed.item_changed.connect(self.on_item_changed)
        self.storage_feed.item_deleted.connect(self.delete)
        self.storage_feed.new_item.connect(self.on_new_item)
        self.storage_feed.name_changed.connect(self.on_name_changed)
        self.storage_feed.warn_message.connect(self.error_bar.show_warning)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.shopping_feed)
        self.stack.addWidget(self.storage_feed)

        vbox = QVBoxLayout()
        vbox.addLayout(topbar)
        vbox.addWidget(self.tag_filter)
        vbox.addWidget(self.error_bar)
        vbox.addWidget(self.stack)

        vbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vbox)

        self.refresh()
        self.show()

    @property
    def is_in_storage_mode(self) -> bool:
        return self.stack.currentWidget() == self.storage_feed

    def refresh(self) -> None:
        self.tag_filter.update_all_tags(
            self.backend.get_tags(
                search=self.searchterm,
                filter_tags=self.tag_filter.filter_tags,
                storage_mode=self.is_in_storage_mode,
            )
        )

        if self.is_in_storage_mode:
            self.storage_feed.show_items(
                self.backend.get_items_in_stock(
                    search=self.searchterm,
                    filter_tags=self.tag_filter.filter_tags,
                ),
            )
            menu_icon_svg = style.menu_home_icon_svg
        else:
            self.shopping_feed.show_items(
                self.backend.get_items_to_buy(
                    search=self.searchterm,
                    filter_tags=self.tag_filter.filter_tags,
                ),
            )
            menu_icon_svg = style.menu_cart_icon_svg

        menu_icon = QIcon(
            QPixmap(QImage.fromData(menu_icon_svg))
        )
        self.menu_button.setIcon(menu_icon)

    @property
    def searchterm(self) -> str:
        return self.searchfield.text()

    def on_new_item(self, item: CartItem) -> None:
        try:
            self.backend.add_item(item)
        except DuplicateError:
            self.error_bar.show_warning(
                f'Item "{item.name}" already exists. Aborting...'
            )
            return

        self.backend.save_list()
        self.refresh()

    def on_item_changed(self, item: CartItem) -> None:
        if item.is_dead:
            self.delete(item)
        else:
            self.backend.save_list()

    def on_name_changed(self, item: CartItem, new_name: str) -> None:
        if self.backend.get_item_by_name(new_name) is not None:
            self.error_bar.show_warning(
                f'Tried to rename "{item.name}" to "{new_name}"'
                " which already exists. Aborting..."
            )
            return
        item.name = new_name

    def delete(self, item: CartItem) -> None:
        self.backend.delete(item)
        self.backend.save_list()
        self.refresh()

    def toggle_view(self) -> None:
        if self.stack.currentWidget() == self.storage_feed:
            self.stack.setCurrentWidget(self.shopping_feed)
        else:
            self.stack.setCurrentWidget(self.storage_feed)
        self.refresh()

    def toggle_filter(self) -> None:
        self.tag_filter.setHidden(not self.tag_filter.isHidden())

        if self.tag_filter.isHidden():
            filter_icon_svg = style.filter_plus_icon_svg
        else:
            filter_icon_svg = style.filter_minus_icon_svg

        filter_icon = QIcon(
            QPixmap(QImage.fromData(filter_icon_svg))
        )
        self.filter_button.setIcon(filter_icon)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--list", "-l",
        type=str,
        help="Use an alternative list by name (without extension)",
        default="default",
    )
    parser.add_argument(
        "--list-file",
        type=str,
        help="Use an alternative list file",
        default=None,
    )
    args = parser.parse_args()
    app = QApplication(sys.argv)
    backend = Backend(list_name=args.list, list_file=args.list_file)
    gui = MainWindow(backend=backend)  # noqa: F841
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
