from dataclasses import dataclass,asdict,field
from typing import Optional
import json

@dataclass
class Category:
    type : str
    name : str


DEFAULT_CATEGORIES : list[Category] = [
    # 지출
    Category("expense","식비"),
    Category("expense","교통"),
    Category("expense","주거"),
    Category("expense","통신"),
    Category("expense","쇼핑"),
    Category("expense","여가"),
    Category("expense","의료"),
    Category("expense","기타"),
    # 수입
    Category("income","급여"),
    Category("income","부수입"),
    Category("income","금융수입"),
    Category("income","기타수입")
]

def init_categories_file(filepath:str):
    with open(filepath,'wt',encoding="utf-8") as f:
        for cat in DEFAULT_CATEGORIES:
            # astype(cat) 를 이용해서 파일에 jsonl형식으로 저장하자.
            # ensure_ascii = False 로 해야 한글이 안깨진다고 함 
            line = json.dumps(asdict(cat),ensure_ascii=False)
            f.write(line + "\n")

# 카테고리 연동 안됨 -> Categories로 설정 해놨는데 적절했는지 궁금함 -> str 로 변경
# category: Category -> category:str
# 카테고리를 생성할때와는 다르게
# 서비스를 이용하는 고객이 search로 카테고리를 선정해 검색해 볼때는 중첩 구조가 복잡해지게됨
@dataclass
class Transaction:
    id : str
    type : str              ## income | expense
    date : str              ## 'YYYY-MM-DD'
    amount : int
    category : str          ## 카테고리 이름(참조 키만 보관)
    memo : Optional[str] = None
    tags : list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

# tags는 여러개가 들어갈수 있으니 str보다는 list[str]이 더 낫다고 함 Gemini

@dataclass
class Budget:
    ym : str
    budget : int


if __name__ =="__main__":
    ...