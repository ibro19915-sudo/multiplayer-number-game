questions = [
    ("What is the tallest building in the world?", "B",
     ["A) Eiffel Tower", "B) Burj Khalifa", "C) Big Ben", "D) CN Tower"]),

    ("What is the largest animal on Earth?", "B",
     ["A) Elephant", "B) Blue Whale", "C) Giraffe", "D) Shark"]),

    ("What is the highest mountain in the world?", "C",
     ["A) K2", "B) Nanga Parbat", "C) Mount Everest", "D) Kilimanjaro"]),

    ("What is the largest ocean?", "D",
     ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"]),

    ("Which planet is known as the Red Planet?", "A",
     ["A) Mars", "B) Venus", "C) Jupiter", "D) Mercury"]),

    ("How many continents are there?", "C",
     ["A) 5", "B) 6", "C) 7", "D) 8"]),

    ("Which continent is the largest?", "C",
     ["A) Africa", "B) Europe", "C) Asia", "D) Australia"]),

    ("What is the largest desert?", "A",
     ["A) Sahara", "B) Gobi", "C) Arabian", "D) Kalahari"]),

    ("Which country has the largest population?", "B",
     ["A) USA", "B) India", "C) Pakistan", "D) Brazil"]),

    ("What is the longest river traditionally taught in many quizzes?", "A",
     ["A) Nile", "B) Amazon", "C) Yangtze", "D) Mississippi"]),

    ("What is the capital of France?", "C",
     ["A) Rome", "B) Berlin", "C) Paris", "D) Madrid"]),

    ("Which is the smallest continent?", "D",
     ["A) Europe", "B) Africa", "C) South America", "D) Australia"]),

    ("Which gas do plants absorb?", "A",
     ["A) Carbon Dioxide", "B) Oxygen", "C) Nitrogen", "D) Hydrogen"]),

    ("What is Earth's natural satellite?", "B",
     ["A) Mars", "B) Moon", "C) Venus", "D) Sun"]),

    ("Which ocean is between Africa and Australia?", "B",
     ["A) Pacific", "B) Indian", "C) Arctic", "D) Atlantic"]),

    ("Which animal is known as the King of the Jungle?", "C",
     ["A) Tiger", "B) Elephant", "C) Lion", "D) Leopard"]),

    ("How many days are there in a leap year?", "D",
     ["A) 364", "B) 365", "C) 367", "D) 366"]),

    ("What is the fastest land animal?", "A",
     ["A) Cheetah", "B) Lion", "C) Horse", "D) Leopard"]),

    ("What is the largest planet in our solar system?", "C",
     ["A) Earth", "B) Saturn", "C) Jupiter", "D) Neptune"]),

    ("What color is chlorophyll?", "B",
     ["A) Blue", "B) Green", "C) Red", "D) Yellow"])
]

score1 = 0
score2 = 0

print("=" * 40)
print("EARTH QUIZ GAME - 2 PLAYERS")
print("=" * 40)

for i, (question, answer, options) in enumerate(questions):

    player = 1 if i % 2 == 0 else 2

    print("\n" + "=" * 40)
    print(f"Question {i+1}")
    print(f"Player {player}'s Turn")
    print("=" * 40)

    print(question)

    for option in options:
        print(option)

    while True:
        user_answer = input("Answer (A/B/C/D): ").upper()

        if user_answer in ["A", "B", "C", "D"]:
            break

        print("Please enter A, B, C, or D")

    if user_answer == answer:
        print("Correct!")

        if player == 1:
            score1 += 1
        else:
            score2 += 1
    else:
        print(f"Wrong! Correct answer: {answer}")

print("\n" + "=" * 40)
print("FINAL RESULTS")
print("=" * 40)

print(f"Player 1 Score: {score1}")
print(f"Player 2 Score: {score2}")

if score1 > score2:
    print("Player 1 Wins!")
elif score2 > score1:
    print("Player 2 Wins!")
else:
    print("It's a Draw!")