import datetime

def date_input():
    # 잘못 되면 다시 실행 하기 위해 while문
    while True:
        # 오류날 수 있으니 0으로 초기화함 (y , m , d)
        y , m , d = 0
        # 가공할수 있으나 헷갈리므로 raw_input으로 설정함
        raw_input = input("날짜를 입력해 주세요.").strip()
        if len(raw_input) == 3:
            # 3개가 입력됬을떄
            y , m , d = raw_input[0:2]
        else:
            # 3개가 아닐때
            print("년 월 일 ex) 2026 09 15 와 같이 '띄어쓰기'로 구분하여 주십니다.")
        if y.isdigit() and m.isdigit() and d.isdigit():
            # 숫자가 들어옴 (정상)
            ...
        else:
            # 숫자가 아님
            print("숫자가 아닌 값을 입력하셨습니다.")
            print("다시 입력해 주세요.")

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text,"%Y-%m-%d")

if __name__ == "__main__":

    ...