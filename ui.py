from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt, QFile, QTimer
from PySide6.QtUiTools import QUiLoader
from uti import wait
from functools import partial
import pydirectinput as pdi
from global_hotkeys import register_hotkey, start_checking_hotkeys, stop_checking_hotkeys, clear_hotkeys

class SwapWindow:
    def __init__(self):

        # 加载 UI 文件
        loader = QUiLoader()
        ui_file = QFile('ui/swap.ui')
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.ui.move(0, 0)

        self.pos_dict = {1: {1: (587, 636),
                            2: (712, 634),
                            3: (839, 635),
                            4: (963, 633),
                            5: (1092, 639),
                            6: (1217, 637),
                            7: (1340, 636)},
                            2: {1: (536, 558),
                            2: (657, 558),
                            3: (781, 556),
                            4: (902, 556),
                            5: (1024, 558),
                            6: (1146, 558),
                            7: (1265, 557)},
                            3: {1: (609, 483),
                            2: (728, 485),
                            3: (847, 484),
                            4: (964, 481),
                            5: (1081, 483),
                            6: (1198, 483),
                            7: (1314, 481)},
                            4: {1: (564, 415),
                            2: (681, 416),
                            3: (792, 415),
                            4: (906, 415),
                            5: (1018, 416),
                            6: (1131, 417),
                            7: (1245, 414)}}

        # 设置窗口属性
        self.ui.setWindowFlags(self.ui.windowFlags() | Qt.WindowStaysOnTopHint) # 窗口置顶

        # 设置样式表
        self.ui.setStyleSheet("""
            QListWidget::item:selected {
                background-color: #a0d8ef;
                color: black;
            }
        """)

        register_hotkey("s", self.swap_chess, None, False)

        self.ui.btn_add.clicked.connect(self.add_loc)
        self.ui.btn_remove.clicked.connect(self.remove_loc)
        self.ui.btn_start.clicked.connect(self.start_listen)
        self.ui.btn_stop.clicked.connect(self.stop_listen)

    def add_loc(self):
        r = self.ui.spinBox_row.value()
        c = self.ui.spinBox_col.value()
        self.ui.listWidget.addItem(f"{r},{c}")

    def remove_loc(self):
        self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())

    def swap_chess(self,):
        pdi.PAUSE = self.ui.spinBox_pause.value() / 1000
        row_count = self.ui.listWidget.count()
        locs = [self.ui.listWidget.item(i).text() for i in range(row_count)]
        for loc in locs:
            r, c = int(loc[0]), int(loc[2])
            x1, y1 = self.pos_dict[r][c]
            x2, y2 = self.pos_dict[r][8-c]
            if abs(4-c) > 1:
                pdi.mouseDown(x1, y1)
                pdi.mouseUp(x2, y2)
            else:
                pdi.mouseDown(x1, y1)
                wait(80)
                pdi.mouseUp(x2, y2)
        for i, loc in enumerate(locs):
            c = int(loc[2])
            item = self.ui.listWidget.item(i)
            item.setText(loc[:2] + f"{8-c}")

    def start_listen(self):
        self.ui.btn_start.setEnabled(False)
        start_checking_hotkeys()
    
    def stop_listen(self):
        self.ui.btn_start.setEnabled(True)
        stop_checking_hotkeys()

    def perform_mouse_click(self):
        pdi.mouseDown(x=578, y=671, button='left')

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("TFT SWAP")
        self.setFixedSize(50, 50)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建按钮
        self.btn = QPushButton("S")
        self.btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn.clicked.connect(self.show_swap)
        
        # 添加按钮到布局
        main_layout.addWidget(self.btn)
        
        # 设置布局到中央部件
        central_widget.setLayout(main_layout)
        self.move(0, 0)

        self.swap = SwapWindow()

    def show_swap(self):
        self.swap.ui.show()
        self.swap.ui.showNormal()

    # def addpos(self):
    #     for i in range(1, 5):
    #         self.pos_dict[i] = {}
    #         for j in range(1, 8):
    #             wait(5000)
    #             self.pos_dict[i][j] = pdi.position()
    #             self.btn.setText(f"{i},{j}")