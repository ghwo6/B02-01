import sys
import argparse
from user_input import date_input,str_input,money_type_verify,category_input,amount_input
from models import Transaction,Category
from repository import TransactionRepository, CategoryRepository
from decorators import handle_errors

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

def new_tx(repo:TransactionRepository):
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
    id = repo.generate_new_id()
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

@handle_errors(hint="카테고리 명 중복 여부 및 입력 형식을 확인해 주세요.")
def f_add(args):
    repo = TransactionRepository(data_dir="./data")
    tx = new_tx(repo)
    repo.save(tx)

    print(f"새로운 거래내역 {tx.id}가 저장되었습니다.")



def f_list(args):

    repo = TransactionRepository(data_dir="./data")
    tx_list = repo.find_all()

    if not tx_list:
        print("등록된 거래 내역이 없습니다.")
        return
    

    # --limit 인자가 주어졌다면 그 개수만큼만 슬라이싱
    if args.limit is not None:
        if args.limit <= 0:
            print("--limit 값은 1 이상의 양수여야 합니다.")
            return
        else:
            limit = args.limit
    else:
        limit = None

    tx_stream = repo.find_latest(limit=limit)

    #출력
    print("\n[ 거래 내역 목록 ]")
    print(f"{'ID':<12} | {'날짜':<8} | {'구분':<8} | {'카테고리':<6} | {'금액':>9} | 메모 /   [태그]")
    print('-'*75)

    count = 0
    for tx in tx_stream:
            count +=1
            tx_type = "수입" if tx.type =="income" else "지출"
            tags_str = f"[{', '.join(tx.tags)}]" if tx.tags else ""
            memo_str = f"{tx.memo or ''} {tags_str}".strip()

            # 천 단위 콤마(,d) 포맷팅 적용
            print(f"{tx.id:<12} | {tx.date:<10} | {tx_type:<8} | {tx.category:<8} | {tx.amount:>9,d}원 | {memo_str}")
    
    if count==0:
        print("등록된 거래 내역이 없습니다.")
    else:
        print("-"*75)
        print(f"총 {count}건의 거래 내역이 출력되었습니다.")

def f_search(args):
    repo = TransactionRepository(data_dir="./data")
    
    #repo.search 제너레이터 호출
    tx_stream = repo.search(
        date_from=getattr(args, "date_from", None),
        date_to=getattr(args, "date_to", None),
        category=getattr(args, "category", None),
        tx_type=getattr(args, "type", None),
        q=getattr(args, "q", None),
        tag=getattr(args, "tag", None)
    )

    print("\n[ 거래 내역 검색 결과 ]")
    print(f"{'ID':<12} | {'날짜':<8} | {'구분':<8} | {'카테고리':<6} | {'금액':>9} | 메모 /   [태그]")
    print("-"*75)
    
    count = 0
    for tx in tx_stream:
            count +=1
            tx_type = "수입" if tx.type =="income" else "지출"
            tags_str = f"[{', '.join(tx.tags)}]" if tx.tags else ""
            memo_str = f"{tx.memo or ''} {tags_str}".strip()
        
            print(f"{tx.id:<12} | {tx.date:<10} | {tx_type:<8} | {tx.category:<8} | {tx.amount:>9,d}원 | {memo_str}")

    if count ==0:
        print("조건에 일치하는 거래 내역이 없습니다.")
    else:
        print("-"*75)
        print(f"총 {count}건의 거래 내역이 검색되었습니다.")

def f_delete(args):
    repo = TransactionRepository()
    tx_id = args.id

    # 삭제 실행
    success = repo.delete(tx_id)

    # 결과 메시지 출력
    if success:
        print(f"[삭제 완료] 거래 ID '{tx_id}'내역이 안전하게 삭제되었습니다.")
    else:
        print(f"[오류] ID가 '{tx_id}'인 거래 데이터를 찾을 수 없습니다. (없는 데이터).")
def f_update(args):
    repo = TransactionRepository()
    tx_id = args.id
    
    # 기존 데이터 조회
    tx = repo.find_by_id(tx_id)
    if not tx:
        print(f"[오류] ID가 '{tx_id}'인 거래 데이터를 찾을 수 없습니다. (없는데이터)")
        return
    
    # 현재 상태 출력
    print(f"\n[ 수정 대상 거래 정보: {tx.id} ]")
    print(f"1. 날짜     : {tx.date}")
    print(f"2. 타입     : {tx.type} ({'수입' if tx.type == 'income' else '지출'})")
    print(f"3. 카테고리 : {tx.category}")
    print(f"4. 금액     : {tx.amount:,d}원")
    print(f"5. 메모     : {tx.memo or '(없음)'}")
    print(f"6. 태그     : {', '.join(tx.tags) if tx.tags else '(없음)'}")
    print("-" * 50)

    # B 대화형 수정
    print("수정할 항목의 번호를 입력하세요 (여러 개면 쉼표 또는 '띄어쓰기'로 구분 예: 1, 4 / 취소는 0):")
    choices = input("선택 > ").strip().replace(","," ").split()
    selected_fields = [c.strip() for c in choices if c.strip()]

    valid_key = {"1","2","3","4","5","6"}
    
    # 조건문
    # field in valid_key
    # for문
    # field for field in selected_fields
    if "0" in selected_fields or not any(field in valid_key for field in selected_fields):
        print("[알림] 수정을 취소했습니다.")
        return
    
    # 각 항목별 재입력
    if "1" in selected_fields:
        print("\n[새 날짜 입력]")
        tx.date = date_input()
    
    if "2" in selected_fields:
        print("\n[새 타입 입력]")
        tx.type = money_type_verify()
    
    if "3" in selected_fields:
        print("\n[새 카테고리 입력]")
        cat_name, verify_type = category_input()
        tx.category = cat_name
        if tx.type != verify_type:
            print(f"\n[알림] '{cat_name}'은(는) '{verify_type}' 카테고리입니다.")
            print(f"타입을 '{tx.type}'에서 '{verify_type}'(으)로 자동 변경합니다.")
            tx.type = verify_type

    if "4" in selected_fields:
        print("\n[새 금액 입력]")
        tx.amount = amount_input("금액을 입력해주세요 (원) > ")

    if "5" in selected_fields:
        print("\n[새 메모 입력]")
        tx.memo = str_input("메모를 입력해주세요 (선택) > ", required=False)

    if "6" in selected_fields:
        print("\n[새 태그 입력]")
        tx.tags = str_input("태그를 입력해주세요 (공백 구분) (선택) > ", required=False, is_tags=True)

    repo.update(tx)
    print(f"\n[수정 완료] 거래 ID '{tx.id}' 내역이 성공적으로 업데이트되었습니다.")

@handle_errors(hint="카테고리 저장소 파일 상태를 확인해 주세요.")
def f_category_list(args):
    cat_repo = CategoryRepository()
    print("\n[ 등록된 카테고리 목록 ]")
    print(f"{'구분':<8} | 카테고리명")
    print("-"*30)

    count = 0
    for c in cat_repo.find_all():
        count +=1
        c_type = "수입" if c.type == "income" else "지출"
        print(f"{c_type:<8} | {c.name}")
    
    print("-"*30)
    print(f"총 {count}개의 카테고리가 등록되어 있습니다.")
    
@handle_errors()
def f_category_add(args):
    cat_repo = CategoryRepository()
    name = input("카테고리명: >").strip()
    
    if not name:
        print("[오류] 카테고리명을 입력해야 합니다.")
        return
    
    if cat_repo.exists(name):
        print(f"[오류] 이미 존재하는 카테고리입니다. {name}")
        return
    
    c_type = money_type_verify()
    cat = Category(type=c_type,name=name)
    
    if cat_repo.add(cat):
        print(f"[저장 완료] category={cat.name} ({cat.type})")
    else:
        print(f"[오류] 카테고리 저장에 실패했습니다.")

@handle_errors(hint="삭제하려는 카테고리명을 정확히 입력해 주세요.")
def f_category_remove(args):
    cat_repo = CategoryRepository()
    tx_repo = TransactionRepository()

    name = input("삭제할 카테고리명: ").strip()

    if not name:
        print("[오류] 카테고리명을 입력해야 합니다.")
        return
    
    if not cat_repo.exists(name):
        print(f"[오류] 존재하지 않는 카테고리입니다.: {name}")
        return
    
    # 거래 내역 있으면 삭제 불가
    if cat_repo.is_used(name,tx_repo):
        print(f"\n[삭제 불가] '{name}' 카테고리는 기존 거래 내역에서 사용중입니다.")
        print("[안내] 사용 중인 거래 내역의 카테고리를 먼저 수정하거나 삭제해주세요.")
        return
    
    if cat_repo.remove(name):
        print(f"[삭제 완료] category={name}")
    else:
        print(f"[오류] 카테고리 삭제에 실패했습니다.")

# 일단은 매개변수가 있으면 출력하는 기능으로 구현함
def parser():

    parser = argparse.ArgumentParser(prog="budget_app",description="나만의 가계부 입니다.")

    # 사용자가 입력한 명령어 이름을 'command'라는 변수에 담도록 설정 with GEMINI
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ["add","list","update","delete","search","summary","budget","category","import","export"]

    # 각 명령어를 독립된 서브 커맨드로 입력함 with GEMINI

    p_add = subparsers.add_parser("add",help="거래 추가")
    p_add.set_defaults(func=f_add)

    p_list = subparsers.add_parser("list",help="거래 내역 조회")
    p_list.add_argument("--limit",type=int,default=None,help = "출력할 최신 거래 내역 개수 (예: --limit 5)")
    p_list.set_defaults(func=f_list)

    p_search = subparsers.add_parser("search", help="거래 검색")
    p_search.add_argument("--from", dest="date_from", help="시작 날짜 (YYYY-MM-DD)")
    p_search.add_argument("--to", dest="date_to", help="종료 날짜 (YYYY-MM-DD)")
    p_search.add_argument("--category", help="카테고리 이름")
    p_search.add_argument("--type", choices=["income", "expense"], help="타입 (income/expense)")
    p_search.add_argument("--q", help="메모 검색어")
    p_search.add_argument("--tag", help="태그 이름")
    p_search.set_defaults(func=f_search)
    
    p_update = subparsers.add_parser("update", help="거래 수정")
    p_update.add_argument("--id", required=True, help="수정할 거래 ID (예: TX-000001)")
    p_update.set_defaults(func=f_update)

    p_delete = subparsers.add_parser("delete", help="거래 삭제")
    p_delete.add_argument("--id", required=True, help="삭제할 거래 ID (예: TX-000001)")
    p_delete.set_defaults(func=f_delete)
    
    p_category = subparsers.add_parser("category",help="카테고리 목록 관리")
    cat_subparsers = p_category.add_subparsers(dest="subcommand",required=True)
    
    # category list
    p_cat_list = cat_subparsers.add_parser("list",help="카테고리 목록 조회")
    p_cat_list.set_defaults(func=f_category_list)

    # category add
    p_cat_add = cat_subparsers.add_parser("add",help="카테고리 추가")
    p_cat_add.add_argument("--name",help="카테고리명")
    p_cat_add.add_argument("--type",choices=["income","expense"],help="카테고리 타입")
    p_cat_add.set_defaults(func=f_category_add)

    # category remove
    p_cat_remove = cat_subparsers.add_parser("remove",help="카테고리 삭제")
    p_cat_remove.add_argument("--name",help="삭제할 카테고리명")
    p_cat_remove.set_defaults(func=f_category_remove)


    # p_summary = subparsers.add_parser("summary",help="거래 추가")
    # p_budget = subparsers.add_parser("budget",help="거래 추가")
    # p_category = subparsers.add_parser("category",help="거래 추가")
    # p_import = subparsers.add_parser("import",help="거래 추가")
    # p_export = subparsers.add_parser("export",help="거래 추가")
    args = parser.parse_args()
    args.func(args)

    # # 실습을 위해 출력해봄
    # for v in sys.argv[1:]:
    #     print(v)

if __name__ == "__main__":
    try:
        parser()
    except KeyboardInterrupt:
        print("CTRL + C로 프로그램을 종료합니다.")
        sys.exit(0)
    except IOError:
        print("CTRL + D 로 프로그램을 종료합니다.")
        sys.exit(0)