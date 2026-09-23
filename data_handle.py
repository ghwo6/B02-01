import os,json
from models import init_categories_file

DIR_NAME = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIR_NAME,"data")
TRANSACTIONS_FILE = os.path.join(DATA_DIR,"transactions.jsonl")
CATEGORIES_FILE = os.path.join(DATA_DIR,"categories.jsonl")
BUDGETS_FILE = os.path.join(DATA_DIR,"budgets.jsonl")

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
# 메인에서 쓰고 있어서 이대로 주자
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
    ...