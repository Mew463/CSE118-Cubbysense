# Alexa Gemini Server

## Starting Server

To start the server, run the following command:
Use 0.0.0.0 for global access of local ip.

```bash
python3 -m uvicorn CubbyGeminiAlexa:app --reload --host 0.0.0.0 --port 8080
```

To host it:

```bash
ngrok http --url=complete-primate-simply.ngrok-free.app 8080
```

## Interactions with File Server

Fetching items:
```bash
response = requests.get("http://localhost:8081/items")
```