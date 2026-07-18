"""Run blocking work (network, disk scans) off the UI thread.

Keeping every Supabase call and filesystem walk on a worker keeps the
interface responsive and the animations smooth. Results come back on the UI
thread via signals.
"""
from __future__ import annotations

from typing import Any, Callable

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal


class _Signals(QObject):
    ok = Signal(object)
    error = Signal(str)


class Task(QRunnable):
    """Run ``fn(*args, **kwargs)`` on the global thread pool."""

    def __init__(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        self.signals = _Signals()

    def run(self) -> None:  # noqa: D401 - QRunnable entry point
        try:
            result = self._fn(*self._args, **self._kwargs)
        except Exception as exc:  # surfaced to the UI as a friendly message
            self.signals.error.emit(str(exc))
        else:
            self.signals.ok.emit(result)


def run_async(
    fn: Callable[..., Any],
    on_ok: Callable[[Any], None],
    on_error: Callable[[str], None],
    *args: Any,
    **kwargs: Any,
) -> None:
    """Fire ``fn`` on a worker and route the outcome back to the UI thread."""
    task = Task(fn, *args, **kwargs)
    task.signals.ok.connect(on_ok)
    task.signals.error.connect(on_error)
    QThreadPool.globalInstance().start(task)
