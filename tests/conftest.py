import os

# The GUI tests must run without a display (locally and on CI runners), so force
# Qt's offscreen platform before any QApplication is created by pytest-qt.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
