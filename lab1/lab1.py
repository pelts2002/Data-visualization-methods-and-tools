import sys, random, math
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (чисто для 3Дшки)
import numpy as np


class krivaya_okno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графики АСУ8")
        self.resize(1100, 700)

        self.chto_seychas = "line"  # line, bars, anim, 3d
        self.fazaaa = 0.0

        # центральная штука
        self.korobka = QWidget()
        self.setCentralWidget(self.korobka)
        self.v = QVBoxLayout(self.korobka)

        # matplotlib фигура
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.kholst = FigureCanvas(self.fig)
        self.v.addWidget(self.kholst)
        self.ax = self.fig.add_subplot(111)

        # панель кнопок и ползунков
        p = QHBoxLayout()
        self.v.addLayout(p)

        # кнопки
        self.knopka_line = QPushButton("Линейный")
        self.knopka_bar = QPushButton("Столбцы")
        self.knopka_anim = QPushButton("Анимация")
        self.knopka_3d = QPushButton("3D")
        self.knopka_stop = QPushButton("Стоп анимации")

        p.addWidget(self.knopka_line)
        p.addWidget(self.knopka_bar)
        p.addWidget(self.knopka_anim)
        p.addWidget(self.knopka_3d)
        p.addWidget(self.knopka_stop)

        # слайдеры
        self.lbl1 = QLabel("Точек/Столбцов: 50")
        self.s1 = QSlider(QtCore.Qt.Horizontal)
        self.s1.setMinimum(3)
        self.s1.setMaximum(500)
        self.s1.setValue(50)
        self.s1.setTickInterval(1)

        self.lbl2 = QLabel("Скорость анимации (мс): 50")
        self.s2 = QSlider(QtCore.Qt.Horizontal)
        self.s2.setMinimum(10)
        self.s2.setMaximum(300)
        self.s2.setValue(50)
        self.s2.setTickInterval(1)

        p2 = QVBoxLayout()
        p2.addWidget(self.lbl1)
        p2.addWidget(self.s1)
        p2.addWidget(self.lbl2)
        p2.addWidget(self.s2)
        self.v.addLayout(p2)

        # таймер для анимации (без изысков)
        self.t = QtCore.QTimer(self)
        self.t.setInterval(self.s2.value())
        self.t.timeout.connect(self._tik)

        # коннекты
        self.knopka_line.clicked.connect(self._pokazat_liniya)
        self.knopka_bar.clicked.connect(self._pokazat_palki)
        self.knopka_anim.clicked.connect(self._pokazat_anim)
        self.knopka_3d.clicked.connect(self._pokazat_3d)
        self.knopka_stop.clicked.connect(self._stop_anim)
        self.s1.valueChanged.connect(self._pererisovat_po_s1)
        self.s2.valueChanged.connect(self._skorost)

        # стартовая картинка
        self._pokazat_liniya()

    # ниже функции кривые, но ладно
    def _ochistit(self):
        # удаляем оси и создаем новые для 2D, иначе 3D не исчезает нормально
        self.fig.clear()
        if self.chto_seychas == "3d":
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.ax = self.fig.add_subplot(111)

    def _pokazat_liniya(self):
        self.chto_seychas = "line"
        self.t.stop()
        self._ochistit()
        n = self.s1.value()
        x = list(range(n))
        y = [random.randint(-50, 50) for _ in range(n)]
        self.ax.plot(x, y, '-', marker='o', linewidth=1, markersize=3, color='tab:blue')
        self.ax.set_title("Линейный график (по точкам)")
        self.ax.set_xlabel("ось X")
        self.ax.set_ylabel("ось Y")
        self.ax.grid(True, linestyle='--', alpha=0.4)
        self.kholst.draw()

    def _pokazat_palki(self):
        self.chto_seychas = "bars"
        self.t.stop()
        self._ochistit()
        n = max(3, min(50, self.s1.value()))
        hh = [random.randint(1, 20) for _ in range(n)]
        xx = np.arange(n)
        self.ax.bar(xx, hh, color='tab:orange')
        self.ax.set_title("Столбчатая диаграмма")
        self.ax.set_xlabel("категория")
        self.ax.set_ylabel("величина")
        self.ax.set_xticks(xx)
        self.ax.set_xticklabels([str(i) for i in xx], rotation=0, fontsize=8)
        self.ax.grid(True, axis='y', linestyle=':', alpha=0.3)
        self.kholst.draw()

    def _pokazat_anim(self):
        self.chto_seychas = "anim"
        self._ochistit()
        self.ax.set_title("Анимированный график (синусик)")
        self.ax.set_xlabel("ось X")
        self.ax.set_ylabel("ось Y")
        self.ax.grid(True, linestyle='--', alpha=0.4)
        self.X_anim = np.linspace(0, 2*np.pi, 400)
        self.fazaaa = 0.0
        self.ln_anim, = self.ax.plot(self.X_anim, np.sin(self.X_anim + self.fazaaa), color='tab:green')
        self.kholst.draw()
        self.t.start()

    def _pokazat_3d(self):
        self.chto_seychas = "3d"
        self.t.stop()
        self._ochistit()
        # простая поверхность
        uu = np.linspace(-4, 4, 40)
        vv = np.linspace(-4, 4, 40)
        U, V = np.meshgrid(uu, vv)
        R = np.sqrt(U**2 + V**2) + 1e-6
        Z = np.sin(R) / R
        self.ax.plot_surface(U, V, Z, cmap='viridis', edgecolor='none', alpha=0.9)
        self.ax.set_title("3D график (sin(r)/r)")
        self.ax.set_xlabel("ось X")
        self.ax.set_ylabel("ось Y")
        self.ax.set_zlabel("ось Z")
        self.kholst.draw()

    def _tik(self):
        if self.chto_seychas != "anim":
            return
        self.fazaaa += 0.15
        if hasattr(self, 'ln_anim'):
            y = np.sin(self.X_anim + self.fazaaa)
            self.ln_anim.set_ydata(y)
            self.kholst.draw()

    def _pererisovat_po_s1(self, val):
        self.lbl1.setText(f"Точек/Столбцов: {val}")
        # обновляем текущий график в зависимости от режима
        if self.chto_seychas == "line":
            self._pokazat_liniya()
        elif self.chto_seychas == "bars":
            self._pokazat_palki()
        # для анимации ползунок s1 не влияет, чтобы не усложнять
        # для 3D тоже не трогаем, иначе всё зависнет :)

    def _skorost(self, val):
        self.lbl2.setText(f"Скорость анимации (мс): {val}")
        try:
            self.t.setInterval(val)
        except Exception as oops:
            print("ой:", oops)

    def _stop_anim(self):
        self.t.stop()


def zapusk():
    app = QApplication(sys.argv)
    okno = krivaya_okno()
    okno.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    zapusk()