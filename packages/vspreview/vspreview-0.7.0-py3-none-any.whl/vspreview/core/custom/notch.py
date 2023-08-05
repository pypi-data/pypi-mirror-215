
from __future__ import annotations

from typing import Iterable, Iterator, Sequence, TypeVar, cast

from PyQt6.QtCore import QLineF, Qt
from PyQt6.QtGui import QColor
from vstools import fallback

from ..types import Frame, Scene, Time

__all__ = [
    'Notch',
    'Notches'
]


class Notch:
    def __init__(
        self, data: int | Frame | Time, color: QColor | Qt.GlobalColor | None = None,
        label: str | None = None, line: QLineF = QLineF()
    ) -> None:
        if isinstance(data, int):
            data = Frame(data)

        self.data = data
        self.color = cast(QColor, fallback(color, Qt.GlobalColor.white))
        self.label = fallback(label, '')
        self.line = line

    def __repr__(self) -> str:
        return '{}({}, {}, {}, {})'.format(
            type(self).__name__, repr(self.data), repr(self.color), repr(self.label), repr(self.line)
        )

    @classmethod
    def from_param(
        cls: type[NotchSelf], data: NotchT, color: QColor | Qt.GlobalColor | None = None, label: str | None = None
    ) -> Iterable[NotchSelf]:
        if isinstance(data, Notch):
            yield Notch(data.data, color if data.color is None else data.color, data.label or label, data.line)
            return

        if isinstance(data, Scene):
            if not label:
                label = data.label

            yield Notch(data.start, color, label)

            if data.end != data.start:
                yield Notch(data.end, color, label)

            return

        if isinstance(data, (int, Frame, Time)):
            yield Notch(data, color, label)
            return

        raise TypeError


NotchT = int | Frame | Scene | Time | Notch
NotchSelf = TypeVar('NotchSelf', bound=Notch)


class Notches:
    def __init__(
        self, other: Sequence[NotchT] | Notches | None = None,
        color: QColor | Qt.GlobalColor | None = None, label: str | None = None
    ) -> None:
        self.items = list[Notch]()

        if isinstance(other, Notches):
            self.items = list(other.items)
            return

        if isinstance(other, Sequence):
            for notch in other:
                self.add(notch, color, label)

    def add(
        self, data: NotchT, color: QColor | Qt.GlobalColor | None = None, label: str | None = None
    ) -> None:
        self.items.extend(Notch.from_param(data, color, label))

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> Notch:
        return self.items[index]

    def __iter__(self) -> Iterator[Notch]:
        return iter(self.items)

    def __repr__(self) -> str:
        return '{}({})'.format(type(self).__name__, repr(self.items))
