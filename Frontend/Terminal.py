import os
import sys
import subprocess
import pyfiglet


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def display_ascii_front_page():
    """Show the front page once."""
    clear_screen()

    title = pyfiglet.figlet_format("Git Secret Prevention", font="standard")

    print("=" * 60)
    print(title)
    print("=" * 60)
    print()
    print("  Version 1.0.0")
    print("  Welcome User!")
    print()
    print("=" * 60)
    print()
    print("Options:")
    print("  1) Continue ")
    print("  Q) Quit")
    print()


def run_main_py():
    """Run main.py as a separate process."""
    # Use the same Python executable and assume main.py is in same directory
    script_path = os.path.join(os.path.dirname(__file__), "main.py")
    if not os.path.isfile(script_path):
        print("main.py not found next to this script.")
        return

    # Call: python main.py
    subprocess.run([sys.executable, script_path])


def main():
    display_ascii_front_page()

    while True:
        choice = input("Enter choice: ").strip().upper()
        if choice == "1":
            clear_screen()
            run_main_py()
            break  # remove this if you want to come back to menu after main.py finishes
        elif choice == "Q":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1 or Q.\n")


if __name__ == "__main__":
    main()

