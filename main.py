import sys
import argparse
from user_input import date_input,str_input,money_type_verify

PROGRAM_END_POINT = "./main.py"
USAGE_LIST = ["add","list","update","delete","search","summary","budget","category","import","export"]

def defalut_use_print():
    print(f"python {PROGRAM_END_POINT} [usage]")
    print("[usage]는 다음과 같습니다.")
    print_usage()
    return

def print_usage():
    print()
    print(*USAGE_LIST[0:len(USAGE_LIST)//2])
    print(*USAGE_LIST[len(USAGE_LIST)//2:])
    print()

    return

def f_add():
    """
    # 날짜 입력 받음
    # 타입 입력 받음 (income / expense)
    # 카테고리1 - categories.jsonl에 name이 있는지 확인 타입에 맞는지 확인함
    # categories.jsonl에 없다면 추가 해달라고 요청
    # categories에 타입이 맞지 않는다면 변환하자 income -> expense 또는 반대로
    # 카테고리2 - 카테고리 입력받음
    # 금액 입력 (양수 , int(금액이니까))
    # 메모 입력받음 (선택)
    # 태그 입력받음 (선택)
    """


    # 날짜 입력 받음
    date = date_input()
    # 타입 입력 받음 (income / expense)
    print("income = 수익", "expense = 지출", "default = expense")
    money_type = money_type_verify()
    # 카테고리1 - categories.jsonl에 name이 있는지 확인 타입에 맞는지 확인함
    
    # categories.jsonl에 없다면 추가 해달라고 요청
    # categories에 타입이 맞지 않는다면 변환하자 income -> expense 또는 반대로
    # 카테고리2 - 카테고리 입력받음
    # 금액 입력 (양수 , int(금액이니까))
    # 메모 입력받음 (선택)
    # 태그 입력받음 (선택)

    ...

def f_list():
    ...

# 일단은 매개변수가 있으면 출력하는 기능으로 구현함
def parser():

    parser = argparse.ArgumentParser(prog="budget_app")

    # 사용자가 입력한 명령어 이름을 'command'라는 변수에 담도록 설정 with GEMINI
    
    subparsers = parser.add_subparsers(dest="command", required=True,choices=USAGE_LIST)

    # 각 명령어를 독립된 서브 커맨드로 입력함 with GEMINI

    # ["add","list","update","delete","search","summary","budget","category","import","export"]
    p_add = subparsers.add_parser("add",help="거래 추가")
    p_add.set_defaults(func=f_add)

    p_list = subparsers.add_parser("list",help="거래 추가")

    p_update = subparsers.add_parser("update",help="거래 추가")
    p_delete = subparsers.add_parser("delete",help="거래 추가")
    p_search = subparsers.add_parser("search",help="거래 추가")
    p_summary = subparsers.add_parser("summary",help="거래 추가")
    p_budget = subparsers.add_parser("budget",help="거래 추가")
    p_category = subparsers.add_parser("category",help="거래 추가")
    p_import = subparsers.add_parser("import",help="거래 추가")
    p_export = subparsers.add_parser("export",help="거래 추가")


    if len(sys.argv) >1 :
        if sys.argv[1] == "--h":

            defalut_use_print()

            # print("add , list , update , delete , search")
            # print("summary , budget , category , import , export")

            
        else:
            # 라우팅 하는 부분
            if sys.argv[1] in USAGE_LIST:
                print("ok")
            else:
                print("사용 방법을 확인해주세요.")


        # 실습을 위해 출력해봄
        # for v in sys.argv[1:]:
        #     print(v)
    else:
        print("arg가 입력되지 않았습니다.")
        print("사용법이 필요하시면 --help를 입력해주세요.")

if __name__ == "__main__":
    print()
    parser()
    print()