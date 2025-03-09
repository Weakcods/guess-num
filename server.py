import socket
import random
import json


difficulty = 'a'
last_difficulty = 'a'
host = '127.0.0.1'
port = 12345
banner = """
🎮 Welcome to the Number Guessing Game! 🎮

Please select your difficulty level:
🟢 a - Easy (Numbers between 1-50)
🟡 b - Medium (Numbers between 1-100)
🔴 c - Hard (Numbers between 1-500)

Type a, b, or c to begin: """

def generate_random_int(difficulty):
    if difficulty == 'a':
        return random.randint(1, 50)
    elif difficulty == 'b':
        return random.randint(1, 100)
    elif difficulty == 'c':
        return random.randint(1, 500)

def update_leaderboard(name, score, difficulty, leaderboard):
    leaderboard.append({"name": name, "score": score, "difficulty": difficulty})
    leaderboard.sort(key=lambda x: x["score"])
    return leaderboard[:10]

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def filter_leaderboard_by_difficulty(leaderboard, difficulty):
    return [entry for entry in leaderboard if entry["difficulty"] == difficulty]

def format_leaderboard(leaderboard):
    formatted = "🏆 Top Players 🏆\n"
    for i, entry in enumerate(leaderboard, 1):
        formatted += f"{i}. Player: {entry['name']}, Attempts: {entry['score']}\n"
    return formatted


def main():
    # Initialize the socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    print(f"🚀 Server is running on {host}:{port}")
    guessme = 0
    conn = None
    leaderboard = load_leaderboard()


    while True:
        if conn is None:
            print("waiting for connection..")
            conn, addr = s.accept()
            print(f"new client: {addr[0]}")
            conn.sendall(banner.encode('utf-8'))
        else:
            client_input = conn.recv(1024).decode('utf-8').strip()
            if client_input in ['a', 'b', 'c']:
                difficulty = client_input
                last_difficulty = difficulty
                guessme = generate_random_int(difficulty)
                conn.sendall("\n".encode('utf-8'))
                tries = 0
            elif client_input.isdigit():
                guess = int(client_input)
                print(f"User guess attempt: {guess}")
                tries += 1
                if guess == guessme:
                    conn.sendall("🎉 Congratulations! You got it right!\nPlease enter your name: ".encode('utf-8'))
                    name = conn.recv(1024).decode('utf-8').strip()
                    score = tries
                    update_leaderboard(name, score, difficulty, leaderboard)
                    save_leaderboard(leaderboard)
                    conn.sendall("\n".encode('utf-8'))
                    try_again = conn.recv(1024).decode('utf-8').strip()
                    if try_again == 'y':
                        conn.sendall("Continuing".encode('utf-8'))
                    elif try_again == 'n':
                        conn.sendall("\nLeaderboard:\n" + format_leaderboard(filter_leaderboard_by_difficulty(leaderboard, difficulty)).encode('utf-8'))
                        conn.close()
                        print("Connection closed.")
                    else:
                        conn.sendall("Invalid input!".encode('utf-8'))
                elif guess > guessme:
                    conn.sendall("📉 Too high! Try a lower number: ".encode('utf-8'))
                    continue
                elif guess < guessme:
                    conn.sendall("📈 Too low! Try a higher number: ".encode('utf-8'))
                    continue
            elif client_input == "":
                print("❌ Empty Input received.")
            else:
                conn.sendall("❌ Invalid input!\nPlease enter a number or choose difficulty (a/b/c): ".encode('utf-8'))

def server():
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    if WindowsError:
        print("Windows Error.")



if __name__ == "__main__":
    server()