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
    

# def load_json(file_name:str):
#     try:
#         with open(file_name,"rt",encoding="UTF-8") as f:
#             json.loads(f)
#     except FileNotFoundError as e:
#         # 초기 파일 만들기
#         ...

if __name__ =="__main__":
    default_file_check()