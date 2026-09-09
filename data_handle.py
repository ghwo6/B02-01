import os,json

DIR_NAME = os.path.dirname(__file__)
TRANSACTIONS_FILE = os.path.join(DIR_NAME,"transactions.jsonl")
CATEGORIES_FILE = os.path.join(DIR_NAME,"categories.jsonl")
BUDGETS_FILE = os.path.join(DIR_NAME,"budgets.jsonl")



# def load_json(file_name:str):
#     try:
#         with open(file_name,"rt",encoding="UTF-8") as f:
#             json.loads(f)
#     except FileNotFoundError as e:
#         # 초기 파일 만들기
#         ...
