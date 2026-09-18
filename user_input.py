import datetime

def date_input():
    # 잘못 되면 다시 실행 하기 위해 while문
    while True:
        # 오류날 수 있으니 0으로 초기화함 (y , m , d)
        y , m , d = 0,0,0
        # 가공할수 있으나 헷갈리므로 raw_input으로 설정함
        raw_input = input("날짜를 입력해 주세요. YYYY MM DD >").strip().split()
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

def str_input(prompt:str,required:bool=False):
    while True:
        data_input = input(prompt).strip()
        if required:
            if data_input =="":
                print("필수로 입력해야 합니다.","다시 입력해 주세요.",sep="\n")
                continue
            else:
                # 정상적으로 입력됨
                return data_input
        else:
            # 입력안해도 되는 입력값
            return data_input
        
money_type_list = ["income","expense"]

def money_type_verify()->str:
    while True:
        raw_data = str_input("income 또는 expense를 입력하세요. >")
        if raw_data.lower() in money_type_list:
            return raw_data.lower()
        else:
            print("다시 입력해주세요.")

    

def validate_date(date_text):
    try:
        date = datetime.datetime.strptime(date_text,"%Y-%m-%d")
        return date
    except ValueError:
        print("날짜를 잘못 입력하셨습니다.")
if __name__ == "__main__":

    # date_input() 테스트
    # print(date_input())

    # str_input() 함수 테스트
    # str01 = str_input("태그를 입력해주세요. >")
    # print(str01)
    # if str01:
    #     print("str01 = ","입력됨" ,str01)
    # else:
    #     print("str01 = ","입력안됨" ,str01)

    # money_type_verify() 검증
    # money_type = money_type_verify()
    # print(money_type)
    