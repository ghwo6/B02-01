import json
from pathlib import Path
from typing import List , Optional
from dataclasses import asdict
from models import Transaction
from data_handle import generator_transactions_jsonl,trasaction_append

class TransactionRepository:
    def __init__(self,data_dir:str="./data"):
        self.dir_path = Path(data_dir)
        self.file_path = self.dir_path / "transactions.jsonl"
        self._init_storage()

    def _init_storage(self):
        """폴더와 파일이 없으면 자동 생성 (초기화)"""
        self.dir_path.mkdir(parents=True,exist_ok=True)
        if not self.file_path.exists():
            self.file_path.touch()

    def save(self,tx:Transaction) -> None:
        """새로운 거래 내역을 JSONL 맨 끝에 한 줄 추가 (Append)"""
        trasaction_append(asdict(tx))


    def find_all(self) -> List[Transaction]:
        """파일의 모든 줄을 읽어 Transaction 객체 리스트로 복원"""
        transactions = []
        generator_tx_file = generator_transactions_jsonl()
        for line in generator_tx_file:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            transactions.append(Transaction(**data))
        return transactions
    
    def find_by_id(self,tx_id:str) -> Optional[Transaction]:
        """특정 ID를 가진 거래 찾기"""
        for tx in self.find_all():
            if tx.id == tx_id:
                return tx
        return None
    