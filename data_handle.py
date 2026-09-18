import os,json
from dataclass import init_categories_file

DIR_NAME = os.path.dirname(__file__)
TRANSACTIONS_FILE = os.path.join(DIR_NAME,"transactions.jsonl")
CATEGORIES_FILE = os.path.join(DIR_NAME,"categories.jsonl")
BUDGETS_FILE = os.path.join(DIR_NAME,"budgets.jsonl")

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
                line_jsonl = json.dumps(raw_line)
                line_jsonl = json.loads(raw_line)
                yield line_jsonl
    except UnicodeDecodeError:
        print(filename," 파일을 utf-8로 읽을 수 없습니다.")
    except FileNotFoundError:
        print(filename," 파일이 없습니다.")
    except json.JSONDecodeError:
        print(filename," 파일을 JSON으로 해독(Decode)할 수 없습니다.")

# def load_json(file_name:str):
#     try:
#         with open(file_name,"rt",encoding="UTF-8") as f:
#             json.loads(f)
#     except FileNotFoundError as e:
#         # 초기 파일 만들기
#         ...

if __name__ =="__main__":
    # 초기 데이터 만들기 함수 쓸모없었음
    # default_file_check()

    # load_jsonl 함수 테스트
    l = load_jsonl(CATEGORIES_FILE)
    for line in l:
        print(line)
        print(f"type(line) = {type(line)}")
    ...