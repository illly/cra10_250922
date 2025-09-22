id1 = {}
id_cnt = 0

# dat[사용자ID][요일]
dat = [[0] * 100 for _ in range(100)]
points = [0] * 100
grade = [0] * 100
names = [''] * 100
wed = [0] * 100
weeken = [0] * 100

def input2(w, wk):
    #데이터를 클린징하 후 db에 적재
    global id_cnt

    # 회원 테이블 초기화
    if w not in id1:
        id_cnt += 1
        id1[w] = id_cnt
        names[id_cnt] = w
    # 회원 id 획득
    id2 = id1[w]

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
        wed[id2] += 1
    elif wk == "thursday":
        index = 3
        add_point += 1
    elif wk == "friday":
        index = 4
        add_point += 1
    elif wk == "saturday":
        index = 5
        add_point += 2
        weeken[id2] += 1
    elif wk == "sunday":
        index = 6
        add_point += 2
        weeken[id2] += 1
    # 출석 도장 찍고
    dat[id2][index] += 1
    # 점수 테이블 업데이트
    points[id2] += add_point

def input_file():
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
                    input2(parts[0], parts[1])
        # 점수 부여, 요일 별 점수 부여 룰이 명시적으로 들어나도록 수정 필요
        for i in range(1, id_cnt + 1):
            if dat[i][2] > 9:
                #수요일에 10번 이상 참석한 경우 10점 가산점
                points[i] += 10
            if dat[i][5] + dat[i][6] > 9:
                # 주말(토요일, 일요일)에 10번 이상 참석한 경우 10점 가산점
                points[i] += 10
            if points[i] >= 50:
                # 포인트가 50점 이상인 경우 1등급(골드)
                grade[i] = 1
            elif points[i] >= 30:
                # 포인트가 30점 이상인 경우 2등급(실버)
                grade[i] = 2
            else:
                # 그외 0등급(노말)
                grade[i] = 0
            # 확장성을 고려하여 리팩토링 필요

            # 회원 별 점수 및 등급 출력
            print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : ", end="")
            if grade[i] == 1:
                print("GOLD")
            elif grade[i] == 2:
                print("SILVER")
            else:
                print("NORMAL")
        # 탈락 후보 출력
        print("\nRemoved player")
        print("==============")
        for i in range(1, id_cnt + 1):
            if grade[i] not in (1, 2) and wed[i] == 0 and weeken[i] == 0:
                print(names[i])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    input_file()