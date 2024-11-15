# CubbySense

## Getting started

- Clone the repository using the following command:
```bash
git clone https://github.com/Mew463/UCSD-CSE-118-218-Team-Cubbysense
```


- Start the server by installing the dependencies using pipenv and running the server using the following commands:
```bash
cd server
pipenv install && pipenv run python -m uvicorn server.server:app --reload
```