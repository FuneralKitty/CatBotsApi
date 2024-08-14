<<<<<<< HEAD
Getting started
This project is a solution for the next test task
https://github.com/itc-code/test-assignments/tree/main/backend-cats-api
## Installation
1. Clone the repo
   ```sh
   git clone https://github.com/yourusername/repo.git
   ```
   Go to the repository 
   ``` sh
   cd CatBotsApi
   ```

    To install the package enter the following command 
    ```
   pip3 install -r requirements.txt
    ```
Now u can proceed with the following commands 

To run first and second quest just run the main.py with command
   #Cделать аскинему   
   ```
   python main.py
   ```
To run the third quest
   ```
   python3 src/Third_quest.py
   ```

Таски:
добавить в requirements нужные либы
add 
pip install pytest pytest-flask pytest-mock

дописать тесты на cats и postgresql


оставить пока на месте.
TO ADD A CAT FORM
curl -X POST http://localhost:8080/cat -H "Content-Type: application/json" \
-d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"
