import json,os
from pathlib import Path
from typing import List , Optional

from dataclasses import asdict

from models import Transaction,Category,Budget

from collections import deque
from decorators import _atomic_rewrite
from models import init_categories_file,DEFAULT_CATEGORIES



class TransactionRepository:
    def __init__(self,data_dir:str="./data"):
        self.dir_path = Path(data_dir)
        self.file_path = self.dir_path / "transactions.jsonl"
        self._init_storage()

        self.current_id = self._get_last_id()

    def _init_storage(self):
        """폴더와 파일이 없으면 자동 생성 (초기화)"""
        self.dir_path.mkdir(parents=True,exist_ok=True)
        if not self.file_path.exists():
            self.file_path.touch()

    def _get_last_id(self) ->int:
        """파일의 가장 마지막 줄만 읽어서 ID 숫자를 파악 (초기화 전용)"""
        # 파일의 사이즈가 0인지 확인하는 방법
        if self.file_path.stat().st_size ==0:
            return 0
        
        try:
        
            with open(self.file_path, "rt", encoding="utf-8") as f:
                # 내용이 비어있는 줄을 제외하고 진짜 내용이 있는 줄만 스트리밍
                non_empty_lines = (line.strip() for line in f if line.strip())
                # 파일의 맨 끝 1줄만 메모리에 가져옴
                last_line = deque(non_empty_lines, maxlen=1)

                if last_line:
                    data = json.loads(last_line[0])
                    return int(data["id"].replace("TX-", ""))
        except (json.JSONDecodeError,KeyError,ValueError):
            # 파일 내용이 손상되 어 있어도 크래시 없이 return 0
            return 0
        return 0

    def generate_new_id(self) ->str:
        self.current_id +=1
        return f"TX-{self.current_id:06d}"
    
    def save(self,tx:Transaction) -> None:
        """새로운 거래 내역을 JSONL 맨 끝에 한 줄 추가 (Append)"""
        with open(self.file_path,"a",encoding="utf-8") as f:
            line = json.dumps(asdict(tx),ensure_ascii=False)
            f.write(line + "\n")

    def find_all(self)->Transaction:
        for data_dict in self._load_json_safe():
            yield Transaction(**data_dict)

    def find_latest(self,limit:Optional[int]=None):
        for data_dict in self._load_json_safe(reverse=True, limit=limit):
            yield Transaction(**data_dict)
    
    def find_by_id(self,tx_id:str) -> Optional[Transaction]:
        """특정 ID를 가진 거래 찾기"""
        for tx in self.find_all():
            if tx.id == tx_id:
                return tx
        return None
    
    def _load_json_safe(self,reverse=False,limit=None):
        # 파일이 존재 하지는 + 용량이 0인지 확인 touch일수 있으니
        if not self.file_path.exists() or self.file_path.stat().st_size ==0:
            return
        try:
            with open(self.file_path,"rt",encoding="utf-8") as f:
                # deque를 쓰면 limit만큼 역순으로 , 안 쓰면 위에서부터 그대로 나옴
                lines = reversed(deque(f,maxlen=limit)) if reverse else f

                for raw_line in lines:
                    raw_line = raw_line.strip() if isinstance(raw_line,str) else raw_line
                    if not raw_line:
                        continue

                    try:
                        yield json.loads(raw_line)
                    except json.JSONDecodeError:
                        print(f"JSON을 Decode 할 수 없습니다. {raw_line}")

        except (json.JSONDecodeError, KeyError, ValueError):
            # 💥 파일에 데이터는 있는데 마지막 줄이 깨진 비정상 상황!
            print(f"[경고] {self.file_path.name}의 마지막 데이터가 손상되어 ID를 확인할 수 없습니다.")
            print("[힌트] 파일 맨 끝 줄의 JSON 형식을 확인하거나 해당 줄을 삭제해 주세요.")
            sys.exit(1)
    
    def search(self,
    date_from:Optional[str]=None, # 시작일
    date_to:Optional[str]=None, # 종료일
    category:Optional[str] = None, # 카테고리
    tx_type : Optional[str]=None, # income / expense
    q:Optional[str] = None, # 메모
    tag:Optional[str]=None #태그
    ):
    # 조건에 일치하는 거래 내역만 최신순으로 스트리밍하는 제너레이터
        for tx in self.find_latest(limit=None):
            # 시작일
            if date_from and tx.date < date_from:
                continue
            # 종료일
            if date_to and tx.date > date_to:
                continue
            # 타입조건 (income / expense)
            if tx_type and tx.type != tx_type:
                continue
            # 카테고리 조건
            if category and tx.category != category:
                continue
            # 메모 검색 (키워드 부분 일치)
            if q and (not tx.memo or q.lower() not in tx.memo.lower()):
                continue
            # 태그 검색
            if tag and (not tx.tags or tag not in tx.tags):
                continue

            # 모든 필터를 통과한 거래만 yield함
            yield tx
    def delete(self,tx_id:str)->bool:
        # 특정 ID의 거래 삭제 (원자적 교체)
        target = self.find_by_id(tx_id)
        if not target:
            return False
        
        # 해당 tx_id만 제외하고 나머지는 파일 재작성
        # 원자적 교체를 구현하기 위해서 jsonl파일을 수정할때
        # 제거 또는 변경할 jsonl구문을 제외하고는 그대로 반환해야 함
        def generate_remaining():
            for tx in self.find_all():
                # 
                if tx.id != tx_id:
                    yield tx
        self._atomic_rewrite(generate_remaining())
        return True
    def update(self,updated_tx:Transaction) -> bool:
        # 특정 ID의 거래 정보 업데이트 (원자적 교체)
        target = self.find_by_id(updated_tx.id)
        if not target:
            return False
        
        # 해당 ID는 updated_tx로 바꾸고 파일 재작성
        def generate_updated():
            for tx in self.find_all():
                if tx.id == updated_tx.id:
                    yield updated_tx
                else:
                    yield tx
        self._atomic_rewrite(generate_updated())
        return True


    def _atomic_rewrite(self,tx_generator) ->None:
        # 임시 파일(.tmp)를 생성하고 쓰고 os.replace로 원자적 교체
        temp_file = self.file_path.with_suffix(".tmp")
        with open(temp_file,"w",encoding="utf-8") as f:
            for tx in tx_generator:
                line = json.dumps(asdict(tx),ensure_ascii=False)
                f.write(line + "\n")
        # 원본 파일을 임시 파일로 즉시 안전하게 교체
        os.replace(temp_file,self.file_path)

class CategoryRepository:
    def __init__(self,data_dir:str="./data"):
        self.dir_path = Path(data_dir)
        self.file_path = self.dir_path / "categories.jsonl"
        self._init_storage()
    
    def _init_storage(self):
        # 폴더 및 파일이 없으면 기본 카테고리로 초기화함
        self.dir_path.mkdir(parents=True,exist_ok=True)
        # stat().st_size로 바이트 크기를 알수있다.
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            with open(self.file_path,"w",encoding="utf-8") as f:
                for cat in DEFAULT_CATEGORIES:
                    f.write(json.dumps(asdict(cat),ensure_ascii=False) + "\n")
    
    def find_all(self):
        # 카테고리를 한 줄 씩 스트리밍
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return
        
        with open(self.file_path,"rt",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield Category(**json.loads(line))
    
    # 제너레이터를 소모하여 존재 여부 확인
    def exists(self,name:str) -> bool:
        # 왜 any가 들어갔는가 ?
        # 카테고리1와
        # 카테고리2 , ...
        # 모두 확인한 결과가
        # return any(True , False ,False, ~) 로 들어가기 때문에 
        return any(cat.name == name for cat in self.find_all())
    
    def add(self,category:Category) -> bool:
        if self.exists(category.name):
            return False
        
        with open(self.file_path,"a",encoding="utf-8") as f:
            f.write(json.dumps(asdict(category),ensure_ascii=False) + "\n")
        return True
    
    # 삭제
    @_atomic_rewrite("file_path")
    def remove(self,name:str):
        if not self.exists(name):
            return None
        for cat in self.find_all():
            if cat.name != name:
                yield cat

    # def remove(self,name:str)-> bool:
    #     if not self.exists(name):
    #         return False
        
    #     def generate_remaining():
    #         for cat in self.find_all():
    #             if cat.name != name:
    #                 yield cat

    #     self._atomic_rewrite(generate_remaining())
    #     return True
    
    # def _atomic_rewrite(self,cat_generator)->None:
    #     temp_file = self.file_path.with_suffix(".tmp")

    #     with open(temp_file,"w",encoding="utf-8") as f:
    #         for cat in cat_generator:
    #             f.write(json.dumps(asdict(cat),ensure_ascii=False)+ "\n")
    #     os.replace(temp_file,self.file_path)

    def is_used(self,category_name:str,tx_repo:TransactionRepository) -> bool:
        for tx in tx_repo.find_all():
            if tx.category == category_name:
                return True
        return False

class BudgetRepository:
    def __init__(self,data_dir :str ="./data"):
        self.dir_path = Path(data_dir)
        self.file_path = self.dir_path / "budgets.jsonl"
        self._init_storage()
    
    def _init_storage(self):
        """ 폴더와 파일이 없으면 자동 생성 """
        self.dir_path.mkdir(parents=True,exist_ok=True)
        if not self.file_path.exists():
            self.file_path.touch()
    
    def find_all(self):
        """ 저장된 모든 월별 예산을 한 줄씩 스트리밍함 """
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return
        
        with open(self.file_path,"rt",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield Budget(**json.loads(line))
    
    def get_budget(self,ym:str) -> Optional[Budget]:
        """ 특정 월(YYYY-MM)의 예산 객체 조회 (없으면 NOne) 반환 """
        for b in self.find_all():
            if b.ym == ym:
                return b
        
        return None
    
    @_atomic_rewrite("file_path")
    def save(self,new_budget:Budget):
        """
        예산 저장 (Upsert : 기존에 해당 월이 있으면 갱신, 없으면 추가)
        데코레이터가 안전하게 임시파일 쓰기 및 os.replace 교체를 수행함
        """
        found = False
        # 내역을 검색해봄
        for b in self.find_all():
        # 입력한 Budget의 연월이 
            if b.ym == new_budget.ym:

                # 기존 월은 새로운 금액으로 교체

                yield new_budget
                found = True
            else:
                yield b

        # 파일에 없던 새로운 월이면 맨 뒤에 추가함
        if not found:
            yield new_budget