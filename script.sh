#!/bin/bash

#./script.sh --check-psql --ngrok --alexa-server --file-server --cam-server

# Global associative array to track PIDs
declare -A processes

# Function to check if PostgreSQL is running
check_psql() {
    echo "Checking if PostgreSQL is running..."
    if pgrep -x "postgres" > /dev/null; then
        echo "PostgreSQL is running."
    else
        echo "PostgreSQL is not running. Please start it and try again."
        exit 1
    fi
}

# Function to activate virtual environment and install dependencies
setup_venv() {
    echo "Setting up virtual environment..."
    venv_path="./.venv"
    activate_script="$venv_path/bin/activate"

    if [ ! -d "$venv_path" ]; then
        echo ".venv not found. Creating..."
        python3.11 -m venv .venv
        echo ".venv created."
    fi

    echo "Activating .venv..."
    source "$activate_script"

    if [ -f "Software/requirements.txt" ]; then
        pip install -r Software/requirements.txt
        echo "Dependencies installed."
    else
        echo "No requirements.txt found. Skipping dependency installation."
    fi
}

# Function to run ngrok
run_ngrok() {
    echo "Starting ngrok..."
    log_file="ngrok.log"
    ngrok http --url=complete-primate-simply.ngrok-free.app 8080 > "$log_file" 2>&1 &
    processes["ngrok"]=$!
    echo "ngrok started with PID: ${processes[ngrok]}"
}

# Function to run the Alexa server
run_alexa_server() {
    echo "Starting Alexa server..."
    log_file="alexa_server.log"
    (cd Software/alexa_server && source ../../.venv/bin/activate && python -m uvicorn CubbyGeminiAlexa:app --reload --host 0.0.0.0 --port 8080) > "$log_file" 2>&1 &
    processes["alexa_server"]=$!
    echo "Alexa server started with PID: ${processes[alexa_server]}"
}

# Function to run the File server
run_file_server() {
    echo "Starting File server..."
    log_file="file_server.log"
    (cd Software/file_server && source ../../.venv/bin/activate && python -m uvicorn server:app --reload --host 0.0.0.0 --port 8081) > "$log_file" 2>&1 &
    processes["file_server"]=$!
    echo "File server started with PID: ${processes[file_server]}"
}

# Function to run the Camera server
run_cam_server() {
    echo "Starting Camera server..."
    log_file="cam_server.log"
    (cd Software/camera_server && source ../../.venv/bin/activate && python ObjectRecognition.py) > "$log_file" 2>&1 &
    processes["cam_server"]=$!
    echo "Camera server started with PID: ${processes[cam_server]}"
}

# Function to clean up processes
cleanup() {
    echo "Cleaning up..."
    for name in "${!processes[@]}"; do
        pid=${processes[$name]}
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            echo "Terminated $name with PID: $pid"
        else
            echo "$name with PID $pid is already terminated."
        fi
    done
    echo "Cleanup complete."
}

# Monitor processes
monitor_processes() {
    while true; do
        for name in "${!processes[@]}"; do
            pid=${processes[$name]}
            if kill -0 "$pid" 2>/dev/null; then
                echo "$name (PID: $pid) is alive."
            else
                echo "$name (PID: $pid) has terminated."
            fi
        done
        sleep 5
    done
}

# Main script logic
main() {
    trap cleanup EXIT

    while [[ $# -gt 0 ]]; do
        case $1 in
            --check-psql)
                check_psql
                shift
                ;;
            --ngrok)
                run_ngrok
                shift
                ;;
            --alexa-server)
                run_alexa_server
                shift
                ;;
            --file-server)
                run_file_server
                shift
                ;;
            --cam-server)
                run_cam_server
                shift
                ;;
            *)
                echo "Unknown option $1"
                exit 1
                ;;
        esac
    done

    monitor_processes
}

main "$@"
