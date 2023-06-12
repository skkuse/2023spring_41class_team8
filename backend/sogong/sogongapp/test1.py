import sys
import io

case_input = '''10
6 3 2 10 10 10 -10 -10 7 3
8
10 9 -5 2 3 4 5 -10'''
sys.stdin = io.StringIO(case_input) 
orginal = sys.stdout
sys.stdout = io.StringIO() 
exec('''
from collections import Counter

# 입력 처리 함수
def process_input():
    N = int(input())  # 상근이가 가지고 있는 숫자 카드의 개수
    cards = list(map(int, input().split()))  # 숫자 카드에 적힌 정수들
    M = int(input())  # 구해야 할 숫자 카드의 개수
    targets = list(map(int, input().split()))  # 구해야 할 숫자 카드들
    
    return N, cards, M, targets

# 메인 함수
def main():
    N, cards, M, targets = process_input()
    
    # 숫자 카드 개수를 세는 Counter 객체 생성
    card_counter = Counter(cards)
    
    # 각 숫자 카드 개수 출력
    for target in targets:
        count = card_counter[target]
        print(count, end=' ')

if __name__ == "__main__":
    main() 
''')
output=sys.stdout.getvalue()
sys.stdout = orginal
if output == '3 0 0 1 2 0 0 2 ':
    print(output)
