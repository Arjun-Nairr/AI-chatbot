import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chatbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        userinp = input("You: ")

        if userinp.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        best_match: str | None = find_best_match(userinp, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Chatbot: {answer}")
        else:
            print("VhatBot: I dont know the answer can you provide it?")
            newans: str = input('Type the answer or type "skip" to skip:')

            if newans.lower() != "skip":
                knowledge_base["questions"].append({"question": userinp, "answer": newans})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Chatbot: thanks for teaching me!")

if __name__ == '__main__':
    chatbot()
