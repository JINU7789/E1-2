import json
import os

STATE_FILE = "state.json"

DEFAULT_QUIZZES = [
    {
        "question": "리스트 맨 뒤에 값을 추가하는 메서드는?",
        "choices": [".add()", ".append()", ".push()", ".insert()"],
        "answer": 2
    },
    {
        "question": "파이썬에서 한 줄 주석을 다는 기호는?",
        "choices": ["//", "/* */", "#", "--"],
        "answer": 3
    },
    {
        "question": "print(2 ** 3) 의 출력 결과는?",
        "choices": ["6", "8", "9", "5"],
        "answer": 2
    },
    {
        "question": "문자열 양쪽 공백을 제거하는 메서드는?",
        "choices": [".strip()", ".clear()", ".cut", ".trim()"],
        "answer": 1
    },
    {
        "question": "딕셔너리를 만들 때 쓰는 기호는?",
        "choices": ["[]", "()", "{}", "<>"],
        "answer": 3
    },
]

def load_state():
    if not os.path.exists(STATE_FILE):
        print("저장 파일이 없어 기본 데이터로 시작합니다.")
        return DEFAULT_QUIZZES, 0

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["quizzes"], data["best_score"]
    except (json.JSONDecodeError, KeyError, OSError) as e:
        print(f"파일을 읽을 수 없어 기본 데이터로 시작합니다. ({e})")
        return DEFAULT_QUIZZES, 0


last_score = 0
best_score = 0


def show_menu():
    print("\n==== 퀴즈게임 ====")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("==================")


def main():
    while True:
        show_menu()
        choice = input("번호를 선택하세요: ").strip()

        if choice == "1":
            start_quiz()
        elif choice == "2":
            add_quiz()
        elif choice == "3":
            show_quiz_list()
        elif choice == "4":
            show_score()
        elif choice == "5":
            print("프로그램을 종료 합니다. 수고하셨습니다.")
            break
        else:
            print("⚠️ 1~5 사이의 번호만 입력해 주세요.")


def start_quiz():
    global last_score
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

    print("총", len(quiz_list), "문제 중", score, "개를 맞혔습니다.")
    last_score = score

    if score > best_score:
        best_score - score
        print("최고 점수예요!")


def show_score():
    print("최근 점수는", last_score, "점입니다.")
    print("최고 점수는", best_score, "점입니다.")


def add_quiz():
    global quiz_list
    question = input("문제를 입력하세요: ")

    options = []
    for i in range(4):
        option = input(f"{i + 1}번 보기를 입력하세요: ")
        options.append(option)

    answer = int(input("정답 번호를 입력해주세요(1~4): "))

    quiz_list.append({"question": question, "choices": options, "answer": answer})
    print("문제가 추가되었어요! 👍")


def show_quiz_list():
    print("\n==== 퀴즈 목록 ====")
    for quiz in quiz_list:
        print(quiz["question"])
    print("==================")

def save_state(quizzes, best_score):
    data = {
        "quizzes": quizzes,
        "best_score": best_score
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("저장 완료! 💾")
    except OSError as e:
        print(f"저장에 실패했습니다. ({e})")


if __name__ == "__main__":
    global_quizzes, global_best = load_state()
    quiz_list = global_quizzes
    best_score = global_best
    main()
    save_state(quiz_list, best_score)