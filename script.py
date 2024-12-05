import os
import signal
import subprocess
import sys
import argparse
import time

# Global dictionary to keep track of process objects
processes = {}

def check_psql():
    """Check if PostgreSQL is running."""
    try:
        result = subprocess.run(['pgrep', '-x', 'postgres'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("PostgreSQL is running.")
        else:
            print("PostgreSQL is not running. Please start it and try again.")
            sys.exit(1)
    except FileNotFoundError:
        print("pgrep command not found. Ensure it's installed and try again.")
        sys.exit(1)

def setup_venv(directory=os.getcwd()):
    """Activate or create a Python virtual environment."""
    venv_path = os.path.join(directory, '.venv')
    activate_script = os.path.join(venv_path, 'bin', 'activate')
    
    if not os.path.exists(venv_path):
        print(f".venv not found in {directory}. Creating...")
        subprocess.run(['python3.11', '-m', 'venv', '.venv'], cwd=directory, check=True)
        print(".venv created.")
    
    print(f"Activating .venv in {directory}...")
    # Source the virtual environment and install requirements
    if os.path.exists(os.path.join(directory, 'Software/requirements.txt')):
        subprocess.run(['bash', '-c', f"source {activate_script} && pip install -r Software/requirements.txt"], cwd=directory, check=True)
        print("Dependencies installed.")
    else:
        print(f"No requirements.txt found in {directory}. Skipping dependency installation.")

def run_ngrok():
    """Run ngrok."""
    log_file = 'ngrok.log'
    print(f"Starting ngrok, logging to {log_file}...")
    process = subprocess.Popen(
        ['ngrok', 'http', '--url=complete-primate-simply.ngrok-free.app', '8080'],
        shell=True,
        stdout=open(log_file, 'w'),
        stderr=subprocess.STDOUT
    )
    processes['ngrok'] = process
    print(f"ngrok started with PID: {process.pid}")

def run_alexa_server():
    """Run the Alexa server."""
    log_file = 'alexa_server.log'
    print(f"Starting Alexa server, logging to {log_file}...")
    process = subprocess.Popen(
        ['bash', '-c', "source ../../.venv/bin/activate && cd python -m uvicorn CubbyGeminiAlexa:app --reload --host 0.0.0.0 --port 8080"],
        cwd='Software/alexa_server',
        shell=True,
        stdout=open(log_file, 'w'),
        stderr=subprocess.STDOUT
    )
    processes['alexa_server'] = process
    print(f"Alexa server started with PID: {process.pid}")

def run_file_server():
    """Run the file server."""
    log_file = 'file_server.log'
    print(f"Starting file server, logging to {log_file}...")
    process = subprocess.Popen(
        ['bash', '-c', "source ../../.venv/bin/activate && python -m uvicorn server:app --reload --host 0.0.0.0 --port 8081"],
        cwd='Software/file_server',
        shell=True,
        stdout=open(log_file, 'w'),
        stderr=subprocess.STDOUT
    )
    processes['file_server'] = process
    print(f"File server started with PID: {process.pid}")

def run_cam_server():
    """Run the Object Recognition server."""
    log_file = 'cam_server.log'
    print(f"Starting Object Recognition server, logging to {log_file}...")
    process = subprocess.Popen(
        ['bash', '-c', "source ../../.venv/bin/activate && python ObjectRecognition.py"],
        cwd='Software/camera_server',
        shell=True,
        stdout=open(log_file, 'w'),
        stderr=subprocess.STDOUT
    )
    processes['cam_server'] = process
    print(f"Camera server started with PID: {process.pid}")

def cleanup():
    """Kill all processes before exiting."""
    print("Cleaning up...")
    for name, process in processes.items():
        try:
            os.kill(process.pid, signal.SIGTERM)
            print(f"Terminated {name} with PID: {process.pid}")
        except ProcessLookupError:
            print(f"{name} with PID {process.pid} is already terminated.")
    print("Cleanup complete.")

def is_process_alive(process):
    """Check if a process is alive."""
    return process.poll() is None

def monitor_processes():
    """Monitor the status of all processes."""
    while True:
        for name, process in processes.items():
            status = "alive" if is_process_alive(process) else "terminated"
            print(f"{name} (PID: {process.pid}) is {status}")
        time.sleep(5)  # Adjust the interval as needed

def main():
    parser = argparse.ArgumentParser(description="Run servers with flags.")
    parser.add_argument('--check-psql', action='store_true', help="Check if PostgreSQL is running.")
    parser.add_argument('--ngrok', action='store_true', help="Run ngrok.")
    parser.add_argument('--alexa-server', action='store_true', help="Run the Alexa server.")
    parser.add_argument('--file-server', action='store_true', help="Run the File server.")
    parser.add_argument('--cam-server', action='store_true', help="Run the Camera server.")
    args = parser.parse_args()

    try:
        setup_venv()
        if args.check_psql:
            check_psql()
        if args.ngrok:
            run_ngrok()
        if args.alexa_server:
            run_alexa_server()
        if args.file_server:
            run_file_server()
        if args.cam_server:
            run_cam_server()

        # Monitor processes
        monitor_processes()
    except KeyboardInterrupt:
        print("\nMain script interrupted.")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
