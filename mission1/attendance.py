from idlelib.run import manage_socket

members = {}
member_cnt = 0

# dat[사용자ID][요일]
MAX_MEMBERS = 100
attendances = [[0] * MAX_MEMBERS for _ in range(MAX_MEMBERS)]
points = [0] * MAX_MEMBERS
grades = [0] * MAX_MEMBERS
names = [''] * MAX_MEMBERS
training_attendances = [0] * MAX_MEMBERS
weekend_attendances = [0] * MAX_MEMBERS

def cleansing_and_input_data(w, wk):
    #데이터를 클린징하 후 db에 적재
    global member_cnt

    # 회원 테이블 초기화
    if w not in members:
        member_cnt += 1
        members[w] = member_cnt
        names[member_cnt] = w
    # 회원 id 획득
    id2 = members[w]

    # 점수 계산
    add_point = 0
    index = 0

    # 요일 별 점수 부여, day of week std를 이용하도록 개선 필요
    if wk == "monday":
        index = 0
        add_point += 1
    elif wk == "tuesday":
        index = 1
        add_point += 1
    elif wk == "wednesday":
        index = 2
        add_point += 3
        training_attendances[id2] += 1
    elif wk == "thursday":
        index = 3
        add_point += 1
    elif wk == "friday":
        index = 4
        add_point += 1
    elif wk == "saturday":
        index = 5
        add_point += 2
        weekend_attendances[id2] += 1
    elif wk == "sunday":
        index = 6
        add_point += 2
        weekend_attendances[id2] += 1
    # 출석 도장 찍고
    attendances[id2][index] += 1
    # 점수 테이블 업데이트
    points[id2] += add_point

def manage_attendance():
    #TODO: 이해한 다음 함수로 쪼개기
    try:
        # Read Input File
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                # 모든 row는 두개의 열로 구성되어 있음, 1개일 경우 예외처리 필요
                if len(parts) == 2:
                    cleansing_and_input_data(parts[0], parts[1])
        # 점수 부여, 요일 별 점수 부여 룰이 명시적으로 들어나도록 수정 필요
        for i in range(1, member_cnt + 1):
            if attendances[i][2] > 9:
                #수요일에 10번 이상 참석한 경우 10점 가산점
                points[i] += 10
            if attendances[i][5] + attendances[i][6] > 9:
                # 주말(토요일, 일요일)에 10번 이상 참석한 경우 10점 가산점
                points[i] += 10
            if points[i] >= 50:
                # 포인트가 50점 이상인 경우 1등급(골드)
                grades[i] = 1
            elif points[i] >= 30:
                # 포인트가 30점 이상인 경우 2등급(실버)
                grades[i] = 2
            else:
                # 그외 0등급(노말)
                grades[i] = 0
            # 확장성을 고려하여 리팩토링 필요

            # 회원 별 점수 및 등급 출력
            print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : ", end="")
            if grades[i] == 1:
                print("GOLD")
            elif grades[i] == 2:
                print("SILVER")
            else:
                print("NORMAL")
        # 탈락 후보 출력
        print("\nRemoved player")
        print("==============")
        for i in range(1, member_cnt + 1):
            if grades[i] not in (1, 2) and training_attendances[i] == 0 and weekend_attendances[i] == 0:
                print(names[i])
    
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    manage_attendance()