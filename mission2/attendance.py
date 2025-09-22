from AttendancePolicy import Policy, Calendar

# define file spec
FILE_PATH = "attendance_weekday_500.txt"
NAME_FIELD = "name"
DAY_OF_WEEK_FIELD = "dow"
MAX_FILE_LENGTH = 500
NO_FIELDS = 2

class AttendanceManager:
    def __init__(self, policy):
        self.policy = policy
        self.init_database()

    def init_database(self):
        # init DB
        self.members = {}
        self.member_cnt = 0

        self.attendances = [[0] * self.policy.MAX_MEMBERS for _ in range(self.policy.MAX_MEMBERS)]
        self.points = [0] * self.policy.MAX_MEMBERS
        self.grades = [0] * self.policy.MAX_MEMBERS
        self.names = [''] * self.policy.MAX_MEMBERS

    def apply_attendance_data(self, records):
        for r in records:
            #데이터를 클린징하 후 db에 적재
            name = r.get(NAME_FIELD)
            dow = r.get(DAY_OF_WEEK_FIELD)
            member_id = self.get_member_id(name)

            self.points[member_id] += self.calculate_points(dow)
            self.attendances[member_id][dow] += 1


    def calculate_points(self, dow) -> int:
        point = 0
        if dow in self.policy.TRAINING_DOW:
            point += self.policy.TRAINING_ATTENDANCE_SCORE
        elif dow in self.policy.WEEKEND_DOW:
            point += self.policy.WEEKEND_ATTENDANCE_SCORE
        else:
            point += self.policy.ATTENDANCE_SCORE
        return point


    def get_member_id(self, name):

        if name not in self.members:
            self.member_cnt += 1
            self.members[name] = self.member_cnt
            self.names[self.member_cnt] = name
        return self.members.get(name)


    def manage_attendance(self):
        records = self.read_file()
        if len(records) < 0:
            return
        self.apply_attendance_data(records)
        self.apply_bonus()
        self.change_member_grade()
        self.suggest_player_to_remove()


    def apply_bonus(self):
        for i in range(1, self.member_cnt + 1):
            if sum([self.attendances[i][dow] for dow in self.policy.TRAINING_DOW]) >= self.policy.ATTENDANCE_BONUS_CONDITION:
                self.points[i] += self.policy.ATTENDANCE_BONUS_SCORE
            if sum([self.attendances[i][dow] for dow in self.policy.WEEKEND_DOW]) >= self.policy.ATTENDANCE_BONUS_CONDITION:
                self.points[i] += self.policy.ATTENDANCE_BONUS_SCORE


    def change_member_grade(self):
        for member_id in range(1, self.member_cnt + 1):
            for grade_id, grade in enumerate(self.policy.GRADE):
                if self.points[member_id] >= self.policy.GRADE_CHANGE_SCORE_LIMIT.get(grade):
                    # 포인트가 50점 이상인 경우 1등급(골드)
                    self.grades[member_id] = grade_id
                    break

            # 회원 별 점수 및 등급 출력
            print(f"NAME : {self.names[member_id]}, POINT : {self.points[member_id]}, GRADE : ", end="")
            print(self.policy.GRADE[self.grades[member_id]])


    def suggest_player_to_remove(self):
        print("\nRemoved player")
        print("==============")
        for i in range(1, self.member_cnt + 1):
            if self.grades[i] in self.policy.KEEP_GRADE:
                continue
            training_attendances = sum([1 for training_dow in self.policy.TRAINING_DOW if self.attendances[i][training_dow] != 0])
            weekend_attendances = sum([1 for weekend_dow in self.policy.WEEKEND_DOW if self.attendances[i][weekend_dow] != 0])
            if training_attendances == weekend_attendances == 0:
                print(self.names[i])


    def read_file(self) -> list[list[str]]:
        records = []
        try:
            # Read Input File
            with open(FILE_PATH, encoding='utf-8') as f:
                for _ in range(MAX_FILE_LENGTH):
                    line = f.readline()
                    if not line:
                        break
                    r = line.strip().split()
                    if len(r) == NO_FIELDS:
                        records.append(self.format_record(r))
                    else:
                        raise ValueError('Invalid data format came with reading file')
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        return records


    def format_record(self, record):
        dow = record[1].lower()
        if not Calendar.is_valid_dow(dow):
            raise ValueError('Invalid Day of week came')
        return {
            NAME_FIELD: record[0],
            DAY_OF_WEEK_FIELD: Calendar.DOW.get(dow)
        }


if __name__ == "__main__":
    manager = AttendanceManager(Policy())
    manager.manage_attendance()