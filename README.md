Parent Onbaording System
For windows


1. To run the project simply git clone the repo by writing command:-
git clone <https link>

2. Make virtual environment in the directory by writing command in terminal:-
python -m venv myenv

3. Activate the virtual environment by writing command:-
myenv\Scripts\activate

4. Install the all necessary libraries used in the project to run the project by writing command:-
pip install -r requirements.txt   (make sure in which directory requirements.txt is run there only)

5. After installing libraries in the virtual environment, run the following commands to migrate the table schemas into the database:-
python manage.py makemigrations
python manage.py migrate
Run these 2 commands one by one and make sure to run this command in the directory where the manage.py file is.

6. After installing libraries in the virtual environment, simply in the root directory(where the manage.py file is there) run the project by simply running the command:- 

python manage.py runserver


7. now to test the apis go to the url http://127.0.0.1:8000/swagger/ running on your system

8. All the endpoints are there to test that simply click on arrow button in the right corner then click on try it out then where the Bearer is required provide the access token.

9. Acess token will get after the login.

10. To see the all data manipulation go to the admin panel through this link :- http://127.0.0.1:8000/admin/

11. For login the admin panel, run the following command:- 
python manage.py createsuperuser (make sure to run this command in the directory where manage.py file is, means in the same directory of manage.py)

now it will ask for credentials making
Email:- simply give any temp email. e.g- john@example.com
Name:- John
User type:- Mother or Father
Experience type:- First-time or Experienced
Password:- 
Password(again):- 

now login http://127.0.0.1:8000/admin/ here with the credentials 
Email:- john@example.com
Password:- 

 


 
