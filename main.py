import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer

from game import Contract, Building

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('basicUi.ui', self)
        # show main window
        self.show()

        self.complete_buildings = []

        self.buildings = {"projecting": Building(self.pb_project_1, self.pb_project_2, "projecting"),
                         "prototyping": Building(self.pb_prototype_1, self.pb_prototype_2, "prototyping"),
                         "assembling": Building(self.pb_assembly_1, self.pb_assembly_2, "assembling"),
                         "science": Building(self.pb_science_1, self.pb_science_2, "science"),
                         "testing": Building(self.pb_test_1, self.pb_test_2, "testing"),
                         "starting": Building(self.pb_start_1, self.pb_start_2, "starting"),
                         "control": Building(self.pb_control_1, self.pb_control_2, "control")}

        self.current_building = self.buildings["projecting"]

        self.projectButton.clicked.connect(lambda: self.select_building("projecting"))
        self.prototypeButton.clicked.connect(lambda: self.select_building("prototyping"))
        self.buildButton.clicked.connect(lambda: self.select_building("assembling"))
        self.sienceButton.clicked.connect(lambda: self.select_building("science"))
        self.testButton.clicked.connect(lambda: self.select_building("testing"))
        self.controlButton.clicked.connect(lambda: self.select_building("control"))
        self.startButton.clicked.connect(lambda: self.select_building("starting"))
        self.goButton.clicked.connect(self.start_game)
        self.restartButton.clicked.connect(self.restart_game)

        self.slider1.sliderMoved.connect(lambda value: self.update_parameter("financing", value))
        self.slider2.sliderMoved.connect(lambda value: self.update_parameter("crunch", value))
        self.slider3.sliderMoved.connect(lambda value: self.update_employer("technical_skills", value))
        self.slider4.sliderMoved.connect(lambda value: self.update_employer("motivation", value))

        tmp = 0
        self.current_building.set_contract(Contract())
        for _, build in self.buildings.items():
            build.crunch = 90
            build.financing = 90
            tmp += 15

        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_progress_bars)
        self.timer.setInterval(50)

        self.time = 0

        self.sec_timer = QTimer()
        self.sec_timer.setSingleShot(False)
        self.sec_timer.timeout.connect(self.second_clock)
        self.sec_timer.setInterval(1000)

        self.ui_update()

    def start_game(self):
        self.timer.start(50)
        self.sec_timer.start(1000)
        self.time = self.current_building.current_contract.time

    def second_clock(self):
        if self.time > 0:
            self.time -= 1

    def select_employer(self, employer):
        unit = vars(self.current_building)[employer]
        self.current_building.current_unit = unit
        self.ui_update()

    def select_building(self, build_name):
        self.current_building = self.buildings[build_name]
        self.ui_update()

    def update_parameter(self, parameter_name, value):
        vars(self.current_building)[parameter_name] = float(value)
        self.ui_update()

    def ui_update(self):
        out_string = ""
        out_string += f"Current building: {self.current_building}\n"
        out_string += f"Current unit: {self.current_building.current_unit}\n"
        if self.current_building.current_contract is not None:
            out_string += f"Money: {self.current_building.current_contract.money}\n"
        out_string += f"{self.current_building.speed:.3f}\n"
        out_string += f"Time: {self.time // 60:02}:{self.time % 60:02}\n\n"
        for frame in self.complete_buildings:
            out_string += frame + "\n"

        self.continue_check()
        self.complete_check()

        self.textBrowser.setText(out_string)

        self.slider1.setValue(int(self.current_building.financing))
        self.slider2.setValue(int(self.current_building.crunch))
        self.slider3.setValue(int(self.current_building.current_unit.technical_skills))
        self.slider4.setValue(int(self.current_building.current_unit.motivation))

        self.lineEdit_1.setText(f"Financing: {self.current_building.financing:.3f}")
        self.lineEdit_2.setText(f"Crunch: {self.current_building.crunch:.3f}")
        self.lineEdit_3.setText(f"Skills: {self.current_building.current_unit.technical_skills:.3f}")
        self.lineEdit_4.setText(f"Motivation: {self.current_building.current_unit.motivation:.3f}")

    def update_employer(self, unit_name, value):
        vars(self.current_building.current_unit)[unit_name] = float(value)
        self.ui_update()

    def update_progress_bars(self):
        self.ui_update()
        for _, building in self.buildings.items():
            if building.work_now == True:
                building.set_speed()
                building.calc_progress()
                progress = building.get_progress()
                building.bar_1.setValue(int(progress))


    def restart_game(self):
        self.timer.stop()
        self.sec_timer.stop()
        for _, build in self.buildings.items():
            build.current_contract = Contract()
            build.bar_1.setValue(0)
            build.bar_2.setValue(0)
            build.progress = 0
            build.success = 0
        self.ui_update()
        self.complete_buildings.clear()

    def complete_check(self):
        for name, build in self.buildings.items():
            if build.work_complete == True:
                build.work_complete = False
                text = f"{build.name} {build.crunch:.0f} {build.weak_spots}"
                self.complete_buildings.append(text)

    def continue_check(self):
        contract_gave = False
        self.contract = None
        for name, build in self.buildings.items():
            if contract_gave == True:
                build.set_contract(self.contract)
                return
            self.contract = build.try_give_contract()
            if self.contract is not None and name != "control":
                contract_gave = True




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()