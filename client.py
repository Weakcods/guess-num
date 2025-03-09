import socket

HOST = "127.0.0.1"
PORT = 12345

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("🎮 Connected to the game server!")

            # Receive and display server banner
            banner = s.recv(1024).decode()
            print(banner)

            while True:
                # Choose difficulty level
                difficulty_choice = input("Choose difficulty level (a/b/c): ")
                s.sendall(difficulty_choice.encode())

                # Receive prompt to enter guess
                guess_prompt = s.recv(1024).decode()
                print(guess_prompt)

                # Guessing loop
                while True:
                    user_guess = input("🎯 Enter your guess: ")
                    s.sendall(user_guess.encode())

                    # Receive response from server
                    response = s.recv(1024).decode()
                    print(response)

                    if "Congratulations" in response:
                        break

                # Get name and send to server
                name = input("👤 Enter your name: ")
                s.sendall(name.encode())

                msg = s.recv(1024).decode()
                print(msg)
                try_again = input("🔄 Would you like to play again? [y/n]: ")
                s.sendall(try_again.encode())

                dummy = s.recv(1024).decode()
                print(dummy)

                if try_again.lower() != 'y':
                    break
        except ConnectionRefusedError:
            print("❌ Unable to connect to the server. Please make sure the server is running.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

def client():
    try:
        main()
    except ConnectionRefusedError:
        print("❌ Unable to connect to the server. Please make sure the server is running.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        print("👋 Thanks for playing! See you next time!")

if __name__ == "__main__":
    client()