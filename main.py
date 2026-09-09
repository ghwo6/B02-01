import sys

PROGRAM_END_POINT = "./main.py"
USAGE_LIST = ["add","list","update","delete","search","summary","budget","category","import","export"]

def defalut_use_print():
    print(f"python {PROGRAM_END_POINT} [usage]")
    print("[usage]는 다음과 같습니다.")
    print_usage()
    return

def print_usage():
    print()
    print(*USAGE_LIST[0:len(USAGE_LIST)//2])
    print(*USAGE_LIST[len(USAGE_LIST)//2:])
    print()

    return

def route(func,args:list):
    ...

# 일단은 매개변수가 있으면 출력하는 기능으로 구현함
def parser():
    if len(sys.argv) >1 :
        if sys.argv[1] == "--h":

            defalut_use_print()

            # print("add , list , update , delete , search")
            # print("summary , budget , category , import , export")

            
        else:
            # 라우팅 하는 부분
            if sys.argv[1] in USAGE_LIST:
                print("ok")
            else:
                print("사용 방법을 확인해주세요.")


        # 실습을 위해 출력해봄
        # for v in sys.argv[1:]:
        #     print(v)
    else:
        print("arg가 입력되지 않았습니다.")
        print("사용법이 필요하시면 --help를 입력해주세요.")

if __name__ == "__main__":
    print()
    parser()
    print()