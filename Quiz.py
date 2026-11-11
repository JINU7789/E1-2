quiz_list = [
    {
        "question": "문제",
        "choices": ["o", "o", "o", "x"],
        "answer": 4
    },
    {
        "question": "문제",
        "choices": ["x", "o", "o", "o"],
        "answer": 1
    }
]

def show_menu():
    print("\n====퀴즈게임====")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=================")


def main():
    while True:
        show_menu()
        choice = input("번호를 선택하세요: ").strip()

        if choice == "1":
            start_quiz()
        elif choice == "2":
            print("[퀴즈 추가] 기능은 아직 준비 중이에요.")
        elif choice == "3":
            print("[퀴즈 목록] 기능은 아직 준비 중이에요.")
        elif choice == "4":
            print("[점수 확인] 기능은 아직 준비 중이에요.")
        elif choice == "5":
            print("프로그램을 종료 합니다. 수고하셨습니다.")
            break
        else:
            print("⚠️ 1~5 사이의 번호만 입력해 주세요.")


def start_quiz():
    score = 0

    for quiz in quiz_list:
        print(quiz["question"])
        
        for i in range(len(quiz["choices"])):
            print(i + 1, quiz["choices"][i])
        
        user_answer = input("정답 번호를 입력하세요: ").strip()
        
        if user_answer == str(quiz["answer"]):
            print("⭕ 정답입니다!")
            score = score + 1
        else:
            print("❌ 틀렸습니다! 정답은", quiz["answer"], "번입니다.")

    print("총", len(quiz_list), "문제 중", score, "개를 맞혔읍니다.")


if __name__ == "__main__":
    main()