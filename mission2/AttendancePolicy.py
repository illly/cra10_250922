class Policy:
    MAX_MEMBERS = 100
    ATTENDANCE_BONUS_CONDITION = 10
    ATTENDANCE_BONUS_SCORE = 10
    DOW = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }
    TRAINING_DOW = [DOW["wednesday"]]
    WEEKEND_DOW = [DOW["saturday"], DOW["sunday"]]

    TRAINING_ATTENDANCE_SCORE = 3
    WEEKEND_ATTENDANCE_SCORE = 2
    ATTENDANCE_SCORE = 1