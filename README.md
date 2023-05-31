# Database
Go to pgAdmin 4 (you need to use postgresql 15) <br>
1-Create a new database named : VoiceStory


![image](https://github.com/mamoune123/cloning_test_1/assets/128436550/6d570fe8-788e-4e31-9097-4b82af1409ab)

2-Then you ll need to restore it the VoiceStory.sql in it 

![image](https://github.com/mamoune123/cloning_test_1/assets/128436550/0ff2cdf5-b6e3-405f-b8ce-9cb7743aecab)
 

3-Finally you ll need to change the password and owner  in the flask_test.py check in your server info (line 89 - 93) : 


![image](https://github.com/mamoune123/cloning_test_1/assets/128436550/841457cf-12a6-42e5-a41b-144d2d1e7fab)

4-This should be on your tables when its restored : 

![image](https://github.com/mamoune123/cloning_test_1/assets/128436550/dd13aaa5-7196-448e-96c2-89a27e71eb83)





# cloning_test_1
execute using env
```python 
source flasky/bin/activate
```
run the website
```python
python3 flask_test.py
```
# IF ERRORS IN IMPORTS
make sure your select this interpreter by using Ctrl+Shft+P (Windows or Linux) or Cmd+Shft+P (MacOs)

![Capture d’écran 2023-05-22 à 10 22 47](https://github.com/mamoune123/cloning_test_1/assets/128436550/05c80042-8779-406b-800b-3b45f11d625a)
