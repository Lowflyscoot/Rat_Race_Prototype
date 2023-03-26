from random import randint

class Contract():
    def __init__(self):
        self.difficulty = 30
        self.money = 3000
        self.time = 180
        self.goal = "Просто выжить"

class Employer():
    def __init__(self, name):
        self.name = name
        self.technical_skills = 99.0
        self.false_motivation = 0.0
        self.motivation = 99.0
        self.weekend = False

    def __str__(self):
        return self.name

class Building():
    def __init__(self, bar1_obj, bar2_obj, name):
        self.success = 0
        self.progress = 0
        self.speed = 0

        self.name = name
        self.bar_1 = bar1_obj
        self.bar_2 = bar2_obj
        self.financing = 90.0
        self.crunch = 90.0
        self.employer = Employer("emp_boss")
        self.current_unit = self.employer
        self.weak_spots = 0
        self.work_now = False
        self.work_complete = False

        self.current_contract = None

    def __str__(self):
        return self.name

    def set_contract(self, contract_obj):
        self.work_now = True
        self.current_contract = contract_obj

    def set_speed(self):
        if self.current_contract is not None:
            result_speed = (10 * (self.employer.technical_skills * (self.employer.motivation / 100) - self.current_contract.difficulty) / 100) / ((100 - self.crunch) / 100)
            if result_speed > 100:
                result_speed = 100
            self.speed = result_speed
            if self.speed < 0:
                self.speed = 0
        else:
            self.speed = 0

    def calc_progress(self):
        if self.current_contract is not None:
            if self.success < 100 and self.current_contract.money > 0 and self.work_now == True:
                self.calc_money()

                if randint(1, 100) < (self.crunch / 10):
                    self.weak_spots += 1
                if self.employer.weekend == False:
                    if self.employer.motivation > 0.0:
                        if self.speed > 0.0:
                            tmp = (0.02 + 0.02 * (self.crunch / 10)) * (1 - self.financing / 100)
                            self.employer.motivation -= tmp
                            self.employer.false_motivation += tmp
                        else:
                            self.employer.weekend = True
                    else:
                        self.employer.motivation = 0

                    self.calc_bars()

                else:
                    if self.employer.false_motivation >= 0.1:
                        self.employer.motivation += 0.1
                        self.employer.false_motivation -= 0.1
                    else:
                        self.employer.weekend = False

    def calc_bars(self):
        self.progress += self.speed
        if self.progress >= 100:
            self.progress = 0
            if self.success + 3 < 100:
                self.success += 3
            else:
                self.success = 100
                self.work_complete = True
            self.bar_2.setValue(self.success)

    def calc_money(self):
        self.current_contract.money -= 1 * (1 + (self.financing / 100))

    def get_progress(self):
        return self.progress

    def try_give_contract(self):
        if self.work_complete == True and self.work_now == True:
            self.work_now = False
            return self.current_contract
        else:
            return None