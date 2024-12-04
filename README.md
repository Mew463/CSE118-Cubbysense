# CubbySense

## Getting started

- Clone the repository using the following command:
```bash
git clone https://github.com/Mew463/UCSD-CSE-118-218-Team-Cubbysense
```

- Start the server by installing the dependencies using pipenv and running the server using the following commands:
```bash
cd Software/file_server
pipenv install && pipenv run python -m uvicorn server.server:app --reload
```


## **Directory Structure**

```plaintext
project/
├── hardware/                 # Hardware-related configurations and documentation
│   ├── schematics/           # Electrical diagrams and PCB designs
│   ├── firmware/             # Microcontroller code for hardware control
│   └── README.md             # Documentation for hardware setup
├── software/                 # Software modules and servers
│   ├── alexa_server/         # Alexa server for interacting with the file server
│   │   ├── intents/          # Alexa skill intents and configurations
│   │   ├── handlers/         # Request handlers for Alexa interactions
│   │   └── README.md         # Documentation for setting up the Alexa server
│   ├── opencv_server/        # OpenCV server for image processing
│   │   ├── modules/          # Image and video processing modules
│   │   └── README.md         # Documentation for OpenCV server setup
│   ├── file_server/          # Centralized file storage and access server
│   │   ├── storage/          # Stored files accessible to other servers
│   │   ├── api/              # API for file read/write operations
│   │   └── README.md         # Documentation for file server setup
│   └── README.md             # General documentation for all software components
├── requirements.txt          # Python dependencies for the software components
└── README.md                 # Main project documentation
```

Ports:
```
--port 8080 (AlexaGemini)
--port 8081 (FileServer)
--port 8082 (OpenCV)
--port 8083 (CabinetController)
-- ssh port 8022 (public facing port)
```

In each readme, provide how to call or run your service.