# Car Complaint Portal
This project is the part of Sqaudcast assignment.

## PROBLEM STATEMENT
A small website reporting stolen cars


## Instruction to run the application

### You can start this application in three ways:

* Method 1
```
1.Get inside the application directory. 
2.Run this command: pip install --no-cache-dir -r requirements.txt
3.Run: python main.py
```
* Method 2
```
1. Run this command: docker pull piyush7248/complaint:1
2. Now: docker run -p 5000:5000 -it complaint:1
3. Docker must be install in your system.
```
* Method 3
```
1. Move to the directory where deployment.yaml file located.
2. Run: kubectl create -f deployment.yaml
3. Kubernetes cluster will required to step.
```
## Documentation

### /complaint
* Add complaint to the database. It will take name, address, phone, email, complaint from the user.

### /login
* Login portal for policeman to mark the complaint as done status
* user= admin
* pass= 1234

### /display
* Display all the complaint that have pending till now and policeman working on it.

### /delete
* Done button added to the display port so that policeman mark himself available as case is close for now.

### /status
* Automatic synchronization system is created so that as soon as police person is free new complaint assign to them. 
* It display complain left and policeman left. BackgroundSchedular is added to do this.

## Some snaps of UI created

![WorkFlow](./Readme/1.png)

![WorkFlow](./Readme/2.png)

![WorkFlow](./Readme/3.png)

![WorkFlow](./Readme/4.png)

![WorkFlow](./Readme/5.png)
