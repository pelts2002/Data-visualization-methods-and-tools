import os
import PyQt5
import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCanvas
import matplotlib.pyplot as plt

# Подсказываем, где искать плагины Qt
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
    os.path.dirname(PyQt5.__file__),
    "Qt",
    "plugins",
    "platforms"
)

# Главное окно программы
class megaWin(QMainWindow):  # Имя класса
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Колхозный график")  # называем окошко
        self.setGeometry(111, 222, 777, 555)  # размеры окна

        # Центральная часть окна
        megaWid = QWidget()
        self.setCentralWidget(megaWid)

        # Вертикальный макет (чтобы графики вставить внутрь)
        korobka = QVBoxLayout(megaWid)

        # Создаем фигуру с тремя подграфиками
        self.figura, self.axxx = plt.subplots(1, 3, figsize=(12, 4))
        self.holst = FigCanvas(self.figura)

        # Добавляем холст в макет
        korobka.addWidget(self.holst)

        # Рисуем графики
        self.risuiGrafiki()

    def risuiGrafiki(self):
        # ============= ДАННЫЕ =============
        xXx = list(range(1, 6))  # ось X
        yYy = [random.randint(1, 10) for _ in xXx]  # случайные значения для Y
        krugData = [random.randint(1, 10) for _ in range(5)]  # данные для круговой

        # ============= ЛИНЕЙНЫЙ =============
        self.axxx[0].plot(xXx, yYy, marker="*", color="purple", linewidth=2)
        self.axxx[0].set_title("Линия")

        # ============= СТОЛБИКИ =============
        self.axxx[1].bar(xXx, yYy, color="orange", edgecolor="black")
        self.axxx[1].set_title("Столбики")

        # ============= КРУГОВОЙ =============
        self.axxx[2].pie(krugData,
                         labels=[f"Часть {i+1}" for i in range(len(krugData))],
                         autopct='%1.1f%%',
                         shadow=True,
                         startangle=90)
        self.axxx[2].set_title("Кругляш")

        # Обновляем холст (перерисовываем графики)
        self.holst.draw()


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    okoshko = megaWin()  # главное имя переменной
    okoshko.show()
    sys.exit(app.exec_())