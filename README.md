# Smart-Eyebrow-Embroidery-System
## Manual Set-up

To run the Smart Eyebrow Embroidery System, you must have installed the following requirements:

- Python 3.6.8
- OpenCV - Python
- dlib
- numpy
- imutils
- shape_predictor_68_face_landmarks.dat (you can get the trained model file from http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2.)

Once the requirements have been installed, to run the system, open the command prompt and change the directory to where you have stored the Smart Eyebrow Embroidery folder. Then, simply run the command 

`python manage.py runserver`.

To access the website, go to localhost:8000 or http://127.0.0.1:8000/ by using any web browser. 

## Admin Authorization

Call the following command, in the same directory as manage.py, to create the superuser. 
You will be prompted to enter a username, email address, and strong password. 

`python manage.py createsuperuser`. 

Once this command completes a new superuser will have been added to the database.
