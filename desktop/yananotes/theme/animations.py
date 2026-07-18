"""Smooth transition helpers, kept small and reusable.

Every page change and reveal in the app goes through these so motion feels
consistent: a short fade combined with a gentle vertical slide.
"""
from __future__ import annotations

from PySide6.QtCore import (
    QAbstractAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    Qt,
)
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget

FAST = 180
NORMAL = 260


def fade_in(widget: QWidget, duration: int = NORMAL) -> QPropertyAnimation:
    """Fade a widget from transparent to opaque."""
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    anim = QPropertyAnimation(effect, b"opacity", widget)
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    anim.finished.connect(lambda: widget.setGraphicsEffect(None))
    anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
    return anim


def slide_fade_in(widget: QWidget, offset: int = 18, duration: int = NORMAL) -> None:
    """Reveal a widget with a combined upward slide and fade."""
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    group = QParallelAnimationGroup(widget)

    fade = QPropertyAnimation(effect, b"opacity")
    fade.setDuration(duration)
    fade.setStartValue(0.0)
    fade.setEndValue(1.0)
    fade.setEasingCurve(QEasingCurve.Type.OutCubic)

    start_pos = widget.pos() + QPoint(0, offset)
    end_pos = widget.pos()
    slide = QPropertyAnimation(widget, b"pos")
    slide.setDuration(duration)
    slide.setStartValue(start_pos)
    slide.setEndValue(end_pos)
    slide.setEasingCurve(QEasingCurve.Type.OutCubic)

    group.addAnimation(fade)
    group.addAnimation(slide)
    group.finished.connect(lambda: widget.setGraphicsEffect(None))
    group.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
    # Keep a reference so the group is not garbage collected mid flight.
    widget._reveal_anim = group  # type: ignore[attr-defined]


def cross_fade(old: QWidget | None, new: QWidget, duration: int = FAST) -> None:
    """Fade the new page in. The stacked widget handles removing the old."""
    if old is not None:
        old_effect = QGraphicsOpacityEffect(old)
        old.setGraphicsEffect(old_effect)
        out = QPropertyAnimation(old_effect, b"opacity", old)
        out.setDuration(duration)
        out.setStartValue(1.0)
        out.setEndValue(0.0)
        out.finished.connect(lambda: old.setGraphicsEffect(None))
        out.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
    slide_fade_in(new, offset=12, duration=duration + 80)
