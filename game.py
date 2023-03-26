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
        self.financing = 20.0
        self.crunch = 30.0
        self.minimal_take_level = 90
        self.employer = Employer("emp_boss")
        self.current_unit = self.employer
        self.weak_spots = 0
        self.work_now = False
        self.work_complete = False

        self.current_contract = None

        self.support = False
        self.next_build = None
        self.past_build = None
        self.next_support_build = None
        self.connected_build = None
        self.bonus_speed_timer = 0

    def __str__(self):
        return self.name

    def set_contract(self, contract_obj):
        self.work_now = True
        self.current_contract = contract_obj

    def set_speed(self):
        if self.current_contract is not None:
            result_speed = (10 * (self.employer.technical_skills * (self.employer.motivation / 100) - self.current_contract.difficulty) / 100) / ((100 - self.crunch) / 100)
            if self.bonus_speed_timer != 0:
                result_speed += 10
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
            if self.success + 3 < 100 and not self.support:
                self.success += 3
            elif not self.support:
                self.success = 100
                self.work_complete = True
            if self.next_support_build is not None:
                self.next_support_build.current_contract = self.current_contract
                self.next_support_build.work_now = True
            if self.support:
                if not self.next_build.support:
                    self.next_build.bonus_speed_timer = 10
                else:
                    self.next_build.current_contract = self.current_contract
                    self.next_build.work_now = True
                self.work_now = False

            self.bar_2.setValue(self.success)

    def calc_money(self):
        self.current_contract.money -= 1 * (1 + (self.financing / 100))

    def get_progress(self):
        return self.progress

    def try_give_contract(self):
        if self.next_build is not None:
            if self.work_now == True and self.success >= self.next_build.minimal_take_level and self.next_build.current_contract is None:
                return self.current_contract
            else:
                return None
        return None