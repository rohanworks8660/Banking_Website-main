# Banking Website
The Online Bank System has the following functionalities :
- Login/Logout
     -  Login as existing user or new user .
     -  Existing user logs in with username and password.
     -  While new user creates a username and password.

- Home Page – active navbar with various tabs that redirect to their respective pages.

- Services made available  :-
  - Check User Balance
  - Deposit Money
  - Withdraw Money
  - Transaction History
  - Transfer Money (to different account)
  
- Logout -  successfully upon completion of all required tasks.

- Account Management : For new users , on account creation - a random account number is generated and provided.


- Statement Generation : based on specified criteria (credit transactions, debit transactions)


---------------------
##  Steps to follow while setting up first time:

1. Run in cmd : 
     ```
     pip install -r Requirements.txt
     ```
2. Setup mysql using ```sqlqueries.txt```
     1. Create a DB in MYSQL with name:- ```Bank_DB```
     2. ```Use bank_db```

3. Double click ```setup.bat``` to get ```bank_db``` up to date and start the server. Contains   
     ```
     python manage.py makemigrations
     python manage.py migrate
     python manage.py runserver
     ```
4. Double click ```runserver.bat``` to just start the server without migrations. Contains  
     ```
     python manage.py runserver
     ```

5. Go to browser and run url - Online Bank -  http://127.0.0.1:8000/

---------------------


