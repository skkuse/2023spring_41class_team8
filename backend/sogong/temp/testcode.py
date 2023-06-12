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