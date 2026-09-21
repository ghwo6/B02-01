import sys
import argparse
from user_input import date_input,str_input,money_type_verify,category_input,amount_input
from data_handle import new_trasaction_number
from models import Transaction
from repository import TransactionRepository

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

def new_tx():
    # 날짜 입력 받음
    date = date_input()
    # 타입 입력 받음 (income / expense)
    print("income = 수익", "expense = 지출")
    money_type = money_type_verify()
    # 카테고리1 - categories.jsonl에 name이 있는지 확인 타입에 맞는지 확인함
    category,verify_type = category_input()
    # categories.jsonl에 없다면 추가 해달라고 요청
    # categories에 타입이 맞지 않는다면 변환하자 income -> expense 또는 반대로
    # 카테고리2 - 카테고리 입력받음
    
    if money_type != verify_type:
        print(f"{category}는 {verify_type}입니다.")
        print(f"{money_type}을 {verify_type}으로 바꿉니다.")
        money_type = verify_type
    # 금액 입력 (양수 , int(금액이니까))
    price = amount_input("금액을 입력해주세요 (원). (+값으로 입력 부탁드립니다.) > ")
    # 메모 입력받음 (선택)
    memo = str_input("메모를 입력해주세요. (선택). > ",required=False)
    # 태그 입력받음 (선택)
    tag = str_input("태그를 입력해주세요. (선택). > ",required=False,is_tags=True)
    id = new_trasaction_number()
    tx = Transaction(
        id=id,
        type=money_type,
        date=date,
        amount=price,
        category=category,
        memo=memo,
        tags= tag if tag else None
    )
    return tx

def f_add():
    repo = TransactionRepository(data_dir="./data")
    tx = new_tx()
    repo.save(tx)

    print(f"새로운 거래내역 {tx.id}가 저장되었습니다.")



def f_list(args):
    repo = TransactionRepository(data_dir="./data")
    tx_list = repo.find_all()

    if not tx_list:
        print("등록된 거래 내역이 없습니다.")
        return
    
    # 날짜와 id로 최신인지 파악하는 코드 혹시 몰라서 놔둠
    # tx_list.sort(key=lambda x: (x.date, x.id), reverse=True)

    # id순으로 최신인지 파악
    tx_list.sort(key=lambda x: (x.id),reverse=True)

    # --limit 인자가 주우졌다면ㅇ 그 개수만큼만 슬라이싱
    if args.limit is not None:
        if args.limit <= 0:
            print("--limit 값은 1 이상의 양수여야 합니다.")
            return
        tx_list = tx_list[:args.limit]

    #출력
    print("\n[ 거래 내역 목록 ]")
    print(f"{'ID':<10} {'날짜':<12} {"구분":<8} {"카테고리"}")

# 일단은 매개변수가 있으면 출력하는 기능으로 구현함
def parser():

    parser = argparse.ArgumentParser(prog="budget_app",description="나만의 가계부 입니다.")

    # 사용자가 입력한 명령어 이름을 'command'라는 변수에 담도록 설정 with GEMINI
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ["add","list","update","delete","search","summary","budget","category","import","export"]

    # 각 명령어를 독립된 서브 커맨드로 입력함 with GEMINI

    p_add = subparsers.add_parser("add",help="거래 추가")
    p_add.add_argument("--help",action="store_true")
    p_add.set_defaults(func=f_add)

    # p_list = subparsers.add_parser("list",help="거래 추가")
    p_list = subparsers.add_parser("list",help="거래 내역 조회")
    p_list.add_argument("--help",action="store_true")
    p_list.add_argument("--limit",type=int,default=None,help = "출력할 최신 거래 내역 개수 (예: --limit 5)")
    p_list.set_defaults(func=f_list)

    p_update = subparsers.add_parser("update",help="거래 추가")
    p_update.add_argument("--help",action="store_true")
    p_update.add_argument("--id",help="업데이트할 ID를 입력해주세요.")

    p_delete = subparsers.add_parser("delete",help="거래 추가")
    p_delete.add_argument("--help",action="store_true")
    # p_search = subparsers.add_parser("search",help="거래 추가")
    # p_summary = subparsers.add_parser("summary",help="거래 추가")
    # p_budget = subparsers.add_parser("budget",help="거래 추가")
    # p_category = subparsers.add_parser("category",help="거래 추가")
    # p_import = subparsers.add_parser("import",help="거래 추가")
    # p_export = subparsers.add_parser("export",help="거래 추가")


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
        for v in sys.argv[1:]:
            print(v)
    else:
        print("arg가 입력되지 않았습니다.")
        print("사용법이 필요하시면 --help를 입력해주세요.")


if __name__ == "__main__":
    try:
        f_add()
    except KeyboardInterrupt:
        print("CTRL + C로 프로그램을 종료합니다.")
        sys.exit(0)
    except IOError:
        print("CTRL + D 로 프로그램을 종료합니다.")
        sys.exit(0)