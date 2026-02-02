from PySide6.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QDialog)

class FocusSettingsDialog(QDialog):
    def __init__(self, work, break_time):
        super().__init__()
        self.setWindowTitle("FOCUS Settings")

        # Main vertical layout
        layout = QVBoxLayout()

        # Rows for settings
        self.work_spin = self._row(layout, "Work (min)", work)
        self.break_spin = self._row(layout, "Break (min)", break_time)

        # Button row
        btns = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        btns.addStretch()
        btns.addWidget(self.cancel_btn)
        btns.addWidget(self.save_btn)

        layout.addLayout(btns)
        self.setLayout(layout)

        # Dialog behavior
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.accept)

    def _row(self, parent_layout, label, value):
        """
        Creates a labeled spinbox row and adds it to the parent layout.
        Returns the QSpinBox so the controller can read its value.
        """
        row = QHBoxLayout()

        lbl = QLabel(label)
        spin = QSpinBox()
        spin.setRange(1, 120)
        spin.setValue(value)

        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(spin)

        parent_layout.addLayout(row)
        return spin
