from dataclasses import dataclass
from typing import Optional

@dataclass
class Caterogies:
    name : str

# 카테고리 연동 안됨 -> Categories로 설정 해놨는데 적절했는지 궁금함
@dataclass
class Transactions:
    id : str
    type : str
    date : str
    amount : int
    category : Caterogies
    memo : Optional[str] = None
    tags : Optional[str] = None



@dataclass
class Budgets:
    ym : str
    budget : int

