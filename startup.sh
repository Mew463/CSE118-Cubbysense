ngrok http --url=complete-primate-simply.ngrok-free.app 8080
python3.11 -m uvicorn alexa_server/CubbyGeminiAlexa:app --reload  --host 0.0.0.0 --port 8080

python3.11 -m uvicorn file_server/server:app --reload --host 0.0.0.0 --port 8081

