import ast
import json

class Chatbot:
    def __init__(self):
        self.knowledge = {}
        self.answered_questions = set()

    def chatbot_response(self, input):
        input = input.lower()
        highest_similarity = 0
        response = "ChatBot : I'm sorry, I don't understand what you mean. Can you please rephrase your question?"
        for key, value in self.knowledge.items():
            similarity_score = self.similarity(input, key)
            if similarity_score > highest_similarity:
                highest_similarity = similarity_score
                response = value
        if highest_similarity > 0.1:
            return "ChatBot : " + response
        else:
            return "ChatBot : I'm sorry, I don't understand what you mean. Can you please rephrase your question?"

    def correct_chatbot(self, input, correct_response):
        input = input.lower()
        self.knowledge[input] = correct_response
        print("ChatBot : Thank you for correcting me. I have learned from my mistake.")
        with open('data.knowledge', 'w') as f:
            json.dump(self.knowledge, f)
    def import_knowledge(self, file):
        with open(file, 'r') as f:
            data = f.read()
            self.knowledge = ast.literal_eval(data)
        with open('data.knowledge', 'w') as f:
            json.dump(self.knowledge, f)
    @staticmethod
    def similarity(s1, s2):
        s1, s2 = s1.lower(), s2.lower()
        return sum(a == b for a, b in zip(s1, s2)) / len(s1)
    def main(self):
        self.import_knowledge('data.knowledge')
        while True:
            print("\nUser : ")
            user_input = input()
            if user_input.lower() == "exit":
                print("ChatBot : Goodbye!")
                break
            if user_input.lower() == "chatbot.get(knowledge)".lower():
                print("I'm always happy to give out my brains ;) ! Here's my current knowledge : ")
                print(self.knowledge)
            if user_input in self.answered_questions:
                print(self.chatbot_response(user_input))
                continue
            response = self.chatbot_response(user_input)
            print(response)
            correct = input("ChatBot : Is this correct? (yes/no)")
            if correct.lower() == "no":
                correct_response = input("ChatBot : What should the correct response be?\n")
                self.correct_chatbot(user_input, correct_response)
            else:
                self.answered_questions.add(user_input)

chatbot = Chatbot()
chatbot.main()
