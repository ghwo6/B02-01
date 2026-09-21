import json,os
from pathlib import Path
from typing import List , Optional
from dataclasses import asdict
from models import Transaction
from collections import deque
from models import init_categories_file


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
        
        with open(self.file_path, "rt", encoding="utf-8") as f:
            # 파일의 맨 끝 1줄만 메모리에 가져옴
            last_line = deque(f, maxlen=1)
            if last_line:
                data = json.loads(last_line[0])
                return int(data["id"].replace("TX-", ""))
        return 0
    def generate_new_id(self) ->str:
        self.current_id +=1
        return f"TX-{self.current_id:06d}"
    
    def save(self,tx:Transaction) -> None:
        """새로운 거래 내역을 JSONL 맨 끝에 한 줄 추가 (Append)"""
        with open(self.file_path,"a",encoding="utf-8") as f:
            line = json.dumps(asdict(tx),ensure_ascii=False)
            f.write(line + "\n")

    def find_all(self):
        for data_dict in self._load_json_safe():
            yield Transaction(**data_dict)

    def find_latest(self,limit:int):
        for data_dict in self._load_json_safe(reverse=True, limit=limit):
            yield Transaction(**data_dict)
    
    def find_by_id(self,tx_id:str) -> Optional[Transaction]:
        """특정 ID를 가진 거래 찾기"""
        for tx in self.find_all():
            if tx.id == tx_id:
                return tx
        return None
    
    def _load_json_safe(self,reverse=False,limit=None):
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

        except UnicodeDecodeError:
            print(f"{self.file_path.name} 파일을 utf-8로 읽을 수 없습니다.")