import abc

class GradePolicy(abc.ABC):
    pass

class GoldGradePolicy(GradePolicy):
    name = 'GOLD'
    minimum_score = 50
    cut_protected = True

class SilverGradePolicy(GradePolicy):
    name = 'SILVER'
    minimum_score = 30
    cut_protected = True

class NormalGradePolicy(GradePolicy):
    name = 'NORMAL'
    minimum_score = 0
    cut_protected = False