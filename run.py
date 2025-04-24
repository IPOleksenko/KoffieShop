import os
import subprocess
import sys
import signal

def load_env(dotenv_directory='env', dotenv_files=['frontend.env', 'backend.env']):
    """
    Loads environment variables from multiple .env files located in a specified directory.
    """
    for dotenv_file in dotenv_files:
        dotenv_path = os.path.join(dotenv_directory, dotenv_file)
        try:
            with open(dotenv_path, encoding='utf-8') as f:
                print(f"Loading: {dotenv_path}")
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())
        except FileNotFoundError:
            print(f"File not found: {dotenv_path}")

load_env()

def run_command(command, cwd):
    """Runs a command in a new terminal window and keeps it open on error."""
    is_windows = sys.platform.startswith("win")
    
    if is_windows:
        return subprocess.Popen(
            ["cmd", "/k", command],  # /k keeps the window open
            cwd=cwd,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        # Check for available terminal emulator
        terminal = None
        for term in ["gnome-terminal", "konsole", "xfce4-terminal", "lxterminal", "x-terminal-emulator"]:
            if subprocess.call(f"command -v {term}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                terminal = term
                break
        
        if not terminal:
            raise RuntimeError("No supported terminal emulator found!")

        return subprocess.Popen(
            f"{terminal} -- bash -c '{command}; echo \"Press Enter to exit...\"; read'", 
            cwd=cwd, 
            shell=True
        )

# Directory paths
backend_path = os.path.abspath("backend")
frontend_path = os.path.abspath("frontend")

# Commands
django_cmd = "pipenv run python manage.py runserver"
npm_cmd = "pipenv run npm start"
stripe_cli = "stripe listen --forward-to localhost:8000/api/payment/stripe/webhook/"

# Start processes in separate windows
django_process = run_command(django_cmd, backend_path)
npm_process = run_command(npm_cmd, frontend_path)
stripe_process = run_command(stripe_cli, backend_path)

try:
    django_process.wait()
    npm_process.wait()
    stripe_process.wait()
except KeyboardInterrupt:
    print("Stopping servers...")
    django_process.terminate()
    npm_process.terminate()
    stripe_process.terminate()
    try:
        django_process.wait(timeout=5)
        npm_process.wait(timeout=5)
        stripe_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        django_process.kill()
        npm_process.kill()
        stripe_process.kill()
