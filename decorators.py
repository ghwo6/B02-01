import sys
import os,json
# functools에 @functools.wraps 내용을 쓸수 있음
import functools
import time

from pathlib import Path
from dataclasses import asdict


def handle_errors(hint:str="입력 옵션 및 데이터를 다시 확인해 주세요."):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except Exception as e:
                print(f"\n[오류] {e}")
                print(f"[힌트] {hint}")
                sys.exit(1)
        return wrapper
    
    return decorator

# 성능 입증용 데코레이터 구현만 해둠
def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        # time.perf_count 초단위로 계산하는데 정밀도는 1ns
        start = time.perf_counter()
        result = func(*args,**kwargs)
        elapsed = time.perf_counter() - start

        print(f"⏱️ [{func.__name__}] 소요 시간: {elapsed:.8f} 초")

        return result
    return wrapper

def _atomic_rewrite(target_file_attr:str = "file_path"):

    """메서드가 yield하는 데이터들을 임시 파일에 안전하게 쓴 뒤,
    os.replace로 원자적 교체(덮어쓰기)를 수행하는 데코레이터
    """
    def decorator(func):
        def wrapper(self,*args,**kwargs):
            file_path:Path = getattr(self,target_file_attr)
            temp_file = file_path.with_suffix(".tmp")

            # 메서드가 반환한 제너레이터 실행
            item_generator = func(self,*args,**kwargs)
            if item_generator is None:
                return False
            
            with open(temp_file,"w",encoding="utf-8") as f:
                for item in item_generator:
                    if hasattr(item,"__dataclass_fields__"):
                        line = json.dumps(asdict(item),ensure_ascii=False)
                    else:
                        line = json.dumps(item,ensure_ascii=False)
                    f.write(line + "\n")
            
            # 안전하게 교체
            os.replace(temp_file,file_path)
            return True
        return wrapper
    return decorator

def report_count(title:str = "조회"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            result_count = func(*args,**kwargs)
            if isinstance(result_count,int):
                print("-"*50)
                print(f"[{title} 결과] 총 {result_count}건이 처리되었습니다.")

        return wrapper
    return decorator