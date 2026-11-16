"""나만의 퀴즈 게임 (E1-2)

터미널에서 동작하는 콘솔 퀴즈 게임.
- Quiz      : 개별 퀴즈 1개를 표현 (문제/보기/정답)
- QuizGame  : 게임 전체를 관리 (메뉴, 풀기/추가/목록/점수, 파일 저장·불러오기)
데이터는 프로젝트 루트의 state.json(UTF-8)에 저장한다.
"""

import json
import os
import shutil

STATE_FILE = "state.json"       # 데이터 저장 파일 (프로젝트 루트)
BACKUP_FILE = "state.json.bak"  # 손상 파일 백업본

# 파일이 없는 첫 실행에 사용할 기본 퀴즈
# 주제: 파이썬 기초 문법 / 총 7문제 (요구 조건: 5문제 이상)
DEFAULT_QUIZZES = [
    {"question": "리스트 맨 뒤에 값을 추가하는 메서드는?",
     "choices": [".add()", ".append()", ".push()", ".insert()"], "answer": 2},
    {"question": "파이썬에서 한 줄 주석을 다는 기호는?",
     "choices": ["//", "/* */", "#", "--"], "answer": 3},
    {"question": "print(2 ** 3) 의 출력 결과는?",
     "choices": ["6", "8", "9", "5"], "answer": 2},
    {"question": "문자열 양쪽 공백을 제거하는 메서드는?",
     "choices": [".strip()", ".clear()", ".cut()", ".trim()"], "answer": 1},
    {"question": "딕셔너리를 만들 때 쓰는 기호는?",
     "choices": ["[]", "()", "{}", "<>"], "answer": 3},
    {"question": "range(3) 이 만드는 숫자는?",
     "choices": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"], "answer": 2},
    {"question": "\"같다\"를 비교하는 연산자는?",
     "choices": ["=", "==", "!=", "=>"], "answer": 2},
]


class Quiz:
    """개별 퀴즈 1개를 표현하는 클래스.

    속성:
        question (str) : 문제
        choices  (list): 보기 4개
        answer   (int) : 정답 번호 (1~4)
    """

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self, number=None):
        """문제와 보기를 출력한다. number가 주어지면 [문제 N] 형태로 표시."""
        title = f"[문제 {number}]" if number is not None else "[문제]"
        print(title)
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_number):
        """사용자가 고른 번호(int)가 정답이면 True."""
        return user_number == self.answer

    def to_dict(self):
        """JSON 저장용 dict로 변환."""
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        """JSON에서 읽은 dict를 Quiz 객체로 변환."""
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    """게임 전체를 관리하는 클래스.

    속성:
        quizzes    (list[Quiz]): 퀴즈 목록
        best_score (int)       : 최고 점수
        last_score (int)       : 가장 최근 점수
    """

    def __init__(self, quizzes=None, best_score=0):
        self.quizzes = quizzes if quizzes is not None else []
        self.best_score = best_score
        self.last_score = 0

    # ---------- 공통 입력/예외 처리 ----------
    def ask_int_in_range(self, prompt, min_value, max_value):
        """min_value~max_value 범위의 정수를 받을 때까지 재입력을 요구한다.

        처리 케이스: 앞뒤 공백 제거 / 빈 입력 / 숫자 변환 실패 / 범위 밖.
        Ctrl+C(KeyboardInterrupt)와 EOF(EOFError)는 상위로 전달하여 안전 종료 처리한다.
        """
        while True:
            raw = input(prompt).strip()
            if raw == "":
                print(f"⚠️ 빈 입력입니다. {min_value}~{max_value} 사이의 숫자를 입력하세요.")
                continue
            if not raw.lstrip("-").isdigit():
                print(f"⚠️ 숫자가 아닙니다. {min_value}~{max_value} 사이의 숫자를 입력하세요.")
                continue
            value = int(raw)
            if value < min_value or value > max_value:
                print(f"⚠️ 범위를 벗어났습니다. {min_value}~{max_value} 사이의 숫자를 입력하세요.")
                continue
            return value

    def ask_nonempty_text(self, prompt):
        """빈 문자열이 아닌 텍스트를 받을 때까지 재입력을 요구한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 빈 값은 입력할 수 없습니다. 다시 입력하세요.")
                continue
            return text

    # ---------- 메뉴 ----------
    def show_menu(self):
        print("\n========================================")
        print("           🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 점수 확인")
        print("  5. 종료")
        print("========================================")

    # ---------- 1. 퀴즈 풀기 ----------
    def play(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 '2. 퀴즈 추가'로 문제를 등록하세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        score = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            print("\n----------------------------------------")
            quiz.show(number)
            user_number = self.ask_int_in_range("정답 입력: ", 1, len(quiz.choices))
            if quiz.is_correct(user_number):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        self.last_score = score
        print("\n========================================")
        print(f"🏆 결과: {total}문제 중 {score}문제 정답! ({score}점)")

        # 최고 점수 갱신 및 저장
        if score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print("========================================")
        self.save()

    # ---------- 2. 퀴즈 추가 ----------
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.ask_nonempty_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choice = self.ask_nonempty_text(f"선택지 {i}: ")
            choices.append(choice)
        answer = self.ask_int_in_range("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("✅ 퀴즈가 추가되었습니다!")

    # ---------- 3. 퀴즈 목록 ----------
    def show_list(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("----------------------------------------")

    # ---------- 4. 점수 확인 ----------
    def show_score(self):
        if self.last_score == 0 and self.best_score == 0:
            print("\n아직 퀴즈를 풀지 않았습니다. '1. 퀴즈 풀기'를 먼저 해보세요.")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점")
        print(f"   최근 점수: {self.last_score}점")

    # ---------- 파일 저장 / 불러오기 ----------
    def save(self):
        """퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"⚠️ 저장에 실패했습니다. ({e})")

    @classmethod
    def load(cls):
        """state.json에서 데이터를 불러온다.

        - 파일이 없으면: 기본 퀴즈로 시작
        - 파일이 손상/오류: 손상본을 state.json.bak으로 백업한 뒤 기본 퀴즈로 복구
        """
        if not os.path.exists(STATE_FILE):
            print("📂 저장 파일이 없어 기본 퀴즈로 시작합니다.")
            quizzes = [Quiz.from_dict(d) for d in DEFAULT_QUIZZES]
            return cls(quizzes, 0)

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(d) for d in data["quizzes"]]
            best_score = data["best_score"]
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_score}점)")
            return cls(quizzes, best_score)
        except (json.JSONDecodeError, KeyError, TypeError, OSError) as e:
            print(f"⚠️ 저장 파일을 읽을 수 없습니다. ({e})")
            # 손상된 파일을 백업해 두고 기본 데이터로 복구
            try:
                shutil.copy(STATE_FILE, BACKUP_FILE)
                print(f"   손상된 파일을 {BACKUP_FILE}로 백업하고 기본 퀴즈로 복구합니다.")
            except OSError:
                print("   기본 퀴즈로 복구합니다.")
            quizzes = [Quiz.from_dict(d) for d in DEFAULT_QUIZZES]
            return cls(quizzes, 0)

    # ---------- 실행 루프 ----------
    def run(self):
        """메뉴 루프. Ctrl+C / EOF가 발생해도 저장 후 안전하게 종료한다."""
        try:
            while True:
                self.show_menu()
                choice = self.ask_int_in_range("선택: ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_list()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("\n프로그램을 종료합니다. 수고하셨습니다! 👋")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n입력이 중단되어 안전하게 종료합니다.")
        finally:
            self.save()


def main():
    game = QuizGame.load()
    game.run()


if __name__ == "__main__":
    main()
