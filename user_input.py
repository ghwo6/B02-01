import datetime

def date_input():
    # 잘못 되면 다시 실행 하기 위해 while문
    while True:
        # 오류날 수 있으니 0으로 초기화함 (y , m , d)
        y , m , d = 0,0,0
        # 가공할수 있으나 헷갈리므로 raw_input으로 설정함
        raw_input = input("날짜를 입력해 주세요.").strip().split()
        if len(raw_input) == 3:
            # 3개가 입력됬을떄
            y , m , d = raw_input
        else:
            # 3개가 아닐때
            print("년 월 일 ex) 2026 09 15 와 같이 '띄어쓰기'로 구분하여 주십니다.")
            continue
        if y=="0" or m =="0" or d == "0":
            print("0을 입력하셨습니다. 정확하게 년 월 일을 입력해주세요")
            continue
        try:
            datetime.datetime.strptime(f"{y} {m} {d}", "%Y %m %d")
        except ValueError:
            print("날짜를 잘못 입력하셨습니다.")
            continue
        
        return f"{y} {m} {d}"

def validate_date(date_text):
    try:
        date = datetime.datetime.strptime(date_text,"%Y-%m-%d")
        return date
    except ValueError:
        print("날짜를 잘못 입력하셨습니다.")
    
if __name__ == "__main__":
    print(date_input())