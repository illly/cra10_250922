import abc
class Calendar:
    DOW = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }


    def is_valid_dow(day):
        return day in Calendar.DOW


class Policy(abc.ABC):
    def __init__(self):
        self.init_general_policy()
        self.init_score_policy()
        self.init_grade_policy()


    @abc.abstractmethod
    def init_general_policy(self):
        pass


    @abc.abstractmethod
    def init_score_policy(self):
        pass


    @abc.abstractmethod
    def init_grade_policy(self):
        pass


class PolicyVersion1(Policy):
    def init_general_policy(self):
        self.MAX_MEMBERS = 100
        self.TRAINING_DOW = [Calendar.DOW["wednesday"]]
        self.WEEKEND_DOW = [Calendar.DOW["saturday"], Calendar.DOW["sunday"]]


    def init_score_policy(self):
        self.ATTENDANCE_BONUS_CONDITION = 10
        self.ATTENDANCE_BONUS_SCORE = 10
        self.TRAINING_ATTENDANCE_SCORE = 3
        self.WEEKEND_ATTENDANCE_SCORE = 2
        self.ATTENDANCE_SCORE = 1


    def init_grade_policy(self):
    # define grade policy
        self.GRADE = [
            "GOLD",
            "SILVER",
            "NORMAL",
        ]
        self.GRADE_CHANGE_SCORE = {
            "NORMAL": 0,
            "GOLD": 50,
            "SILVER": 30,
        }
        self.CUT_PROTECTED_GRADE = [
            self.GRADE.index(grade) for grade in self.GRADE
                if grade == 'GOLD'
                or grade == 'SILVER'
        ]