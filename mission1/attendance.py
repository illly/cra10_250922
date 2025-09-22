
FILE_PATH = "attendance_weekday_500.txt"
NAME_FIELD = "name"
DAY_OF_WEEK_FIELD = "dow"

# define policy
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
GRADE = [
    "GOLD",
    "SILVER",
    "NORMAL",
]

KEEP_GRADE = [grade for grade in GRADE
                  if grade == 'GOLD'
                  or grade == 'SILVER'
              ]

GRADE_CHANGE_SCORE_LIMIT = {
    "NORMAL": 0,
    "GOLD": 50,
    "SILVER": 30,
}
TRAINING_DOW = [DOW["wednesday"]]
WEEKEND_DOW = [DOW["saturday"], DOW["sunday"]]

TRAINING_ATTENDANCE_SCORE = 3
WEEKEND_ATTENDANCE_SCORE = 2
ATTENDANCE_SCORE = 1

# init DB
members = {}
member_cnt = 0

attendances = [[0] * MAX_MEMBERS for _ in range(MAX_MEMBERS)]
points = [0] * MAX_MEMBERS
grades = [0] * MAX_MEMBERS
names = [''] * MAX_MEMBERS


def apply_attendance_data(records):
    for r in records:
        #데이터를 클린징하 후 db에 적재
        name = r.get(NAME_FIELD)
        dow = r.get(DAY_OF_WEEK_FIELD)
        member_id = get_member_id(name)

        points[member_id] += calculate_points(dow)
        attendances[member_id][dow] += 1


def calculate_points(dow) -> int:
    point = 0
    if dow in TRAINING_DOW:
        point += TRAINING_ATTENDANCE_SCORE
    elif dow in WEEKEND_DOW:
        point += WEEKEND_ATTENDANCE_SCORE
    else:
        point += ATTENDANCE_SCORE
    return point


def get_member_id(name):
    global member_cnt

    if name not in members:
        member_cnt += 1
        members[name] = member_cnt
        names[member_cnt] = name
    return members.get(name)


def manage_attendance():
    records = read_file()
    if len(records) < 0:
        return
    apply_attendance_data(records)
    apply_bonus()
    change_member_grade()
    suggest_player_to_remove()


def apply_bonus():
    for i in range(1, member_cnt + 1):
        if sum([attendances[i][dow] for dow in TRAINING_DOW]) >= ATTENDANCE_BONUS_CONDITION:
            points[i] += ATTENDANCE_BONUS_SCORE
        if sum([attendances[i][dow] for dow in WEEKEND_DOW]) >= ATTENDANCE_BONUS_CONDITION:
            points[i] += ATTENDANCE_BONUS_SCORE


def change_member_grade():
    for member_id in range(1, member_cnt + 1):
        for grade_id, grade in enumerate(GRADE):
            if points[member_id] >= GRADE_CHANGE_SCORE_LIMIT.get(grade):
                # 포인트가 50점 이상인 경우 1등급(골드)
                grades[member_id] = grade_id
                break

        # 회원 별 점수 및 등급 출력
        print(f"NAME : {names[member_id]}, POINT : {points[member_id]}, GRADE : ", end="")
        print(GRADE[grades[member_id]])


def suggest_player_to_remove():
    print("\nRemoved player")
    print("==============")
    for i in range(1, member_cnt + 1):
        if grades[i] in KEEP_GRADE:
            continue
        training_attendances = sum([1 for training_dow in TRAINING_DOW if attendances[i][training_dow] != 0])
        weekend_attendances = sum([1 for weekend_dow in WEEKEND_DOW if attendances[i][weekend_dow] != 0])
        if training_attendances == weekend_attendances == 0:
            print(names[i])


def read_file() -> list[list[str]]:
    records = []
    try:
        # Read Input File
        with open(FILE_PATH, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                r = line.strip().split()
                if len(r) == 2:
                    records.append(format_record(r))
                else:
                    raise ValueError('Invalid data format came with reading file')
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    return records


def format_record(record):
    dow = record[1].lower()
    if dow not in DOW.keys():
        raise ValueError('Invalid Day of week came')
    return {
        NAME_FIELD: record[0],
        DAY_OF_WEEK_FIELD: DOW.get(dow)
    }


if __name__ == "__main__":
    manage_attendance()