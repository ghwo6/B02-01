import os,json
from models import init_categories_file
DIR_NAME = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIR_NAME,"data")
TRANSACTIONS_FILE = os.path.join(DIR_NAME,DATA_DIR,"transactions.jsonl")
CATEGORIES_FILE = os.path.join(DIR_NAME,DATA_DIR,"categories.jsonl")
BUDGETS_FILE = os.path.join(DIR_NAME,DATA_DIR,"budgets.jsonl")

def default_file_check():
    if os.path.exists(TRANSACTIONS_FILE):
        print("transactions.jsonl 파일 로드됨")
    else:
        make_like_touch(TRANSACTIONS_FILE)

    if os.path.exists(CATEGORIES_FILE):
        print("categories.jsonl 파일 로드됨")
    else:
        init_categories_file(CATEGORIES_FILE)
    if os.path.exists(BUDGETS_FILE):
        print("budgets.jsonl 파일 로드됨")
    else:
        make_like_touch(BUDGETS_FILE)

def make_like_touch(filepath:str):
    with open(filepath,'wt',encoding="utf-8"):
        return

def load_jsonl(filename):
    try:
        with open(filename,"rt",encoding="utf-8") as f:
            for raw_line in f:
                # 에러 낫었음
                # line_jsonl = json.dumps(raw_line)
                line_jsonl = json.loads(raw_line)
                yield line_jsonl
    except UnicodeDecodeError:
        print(filename," 파일을 utf-8로 읽을 수 없습니다.")
    except FileNotFoundError:
        print(filename," 파일이 없습니다.")
    except json.JSONDecodeError:
        print(filename," 파일을 JSON으로 해독(Decode)할 수 없습니다.")

def generator_categories_jsonl():
    return load_jsonl(CATEGORIES_FILE)
def lgenerator_budgets_jsonl():
    return load_jsonl(BUDGETS_FILE)
def generator_transactions_jsonl():
    return load_jsonl(TRANSACTIONS_FILE)

def trasaction_append(tx_dict):
    with open(TRANSACTIONS_FILE,"a",encoding="utf-8") as f:
        line = json.dumps(tx_dict,ensure_ascii=False)
        f.write(line + "\n")

# 리스트로 반환
def return_categories_jsonl()->list[dict]:
    categories_list = []
    for li in load_jsonl(CATEGORIES_FILE):
        categories_list.append(li)
    return categories_list

# user_input 함수에서 카테고리 입력할때 사용자에게 안내할때 사용함
def get_categories_name()->list:

    l = load_jsonl(CATEGORIES_FILE)
    li = []
    for line in l:
        li.append(line.get("name").strip())
    return li

# 카테고리를 읽어서 있는 카테고리인지 확인하는 함수를 user_input 에서 짜는 과정에서
# 카테고리 파일을 여러번 호출하게 될거 같아 categories.jsonl의 내용물을 변수로 받은 함수를 만듦
def get_categories()->list[dict]:

    l = load_jsonl(CATEGORIES_FILE)
    li = []
    for line in l:
        li.append(line)
        # li.append(line.get("name").strip())
    return li


# 제너레이터로 가져오기위해 폐기함
# def load_json(file_name:str):
#     try:
#         with open(file_name,"rt",encoding="UTF-8") as f:
#             json.loads(f)
#     except FileNotFoundError as e:
#         # 초기 파일 만들기
#         ...

# 새로운 id를 주기 위해 만든 함수
def new_trasaction_number()->str:
    transaction_number_list = []
    for i , di in enumerate(generator_transactions_jsonl()):
        try:
            raw_id = int(di["id"].replace("TX-",""))
        except Exception as e:
            print("new_trasaction_number 확인 요망", e)

        transaction_number_list.append(raw_id)
    transaction_number_list.sort()
    if len(transaction_number_list) == 0:
        new_number = 1
    else:
        new_number = int(transaction_number_list[-1]) +1
    print(new_number)
    return "TX-" +f"{new_number:06d}"

    # TX-1이 출력됨
    # return "TX-" +str(new_number)



if __name__ =="__main__":
    # 초기 데이터 만들기 함수 쓸모없었음
    # default_file_check()

    # load_jsonl 함수 테스트
    # l = load_jsonl(CATEGORIES_FILE)
    # for line in l:
    #     print(line)
    #     print(f"type(line) = {type(line)}")
    
    # 카테고리의 name만 뽑아봄
    # l = load_jsonl(CATEGORIES_FILE)
    # li = []
    # for line in l:
    #     li.append(line.get("name").strip())
    # print(li,sep = "")
    print(new_trasaction_number())