# Secure_Communication_Between_IOT_Devices_Using_RSA
Here we encrypt the messages sent from client to the iot server using RSA encryption. The password is encrypted and stored in the MongoDB Database, Below is the link to download the MongoDB Software 
https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.7-signed.msi

Below is the Screenshots of the Project
## 1) Entering Username and Password after running hash.py file
<img width="958" alt="hash" src="https://github.com/Rav-Kiran123/Secure_Communication_Between_IOT_Devices_Using_RSA/assets/89346194/8264190b-87ed-46f5-9f29-b7506adcb6cc">

## 2) Checking if the username and password got stored in the MongoDB Database(Note the password will be in Encrypted Form
<img width="959" alt="image" src="https://github.com/Rav-Kiran123/Secure_Communication_Between_IOT_Devices_Using_RSA/assets/89346194/09ff1915-0438-4b0d-9ffa-6b137a02dd2b">

## 3) Now we run the Client.py file and Iot.py file simultaneoulsy and in the Client.py terminal you will get an Output like this
<img width="822" alt="Client py1" src="https://github.com/Rav-Kiran123/Secure_Communication_Between_IOT_Devices_Using_RSA/assets/89346194/295a8375-31f6-4e3b-9bf3-0560f1f992f1">

## 4) Enter Y and then enter your Username and Password you had given before and then enter whatever message you want to send to the IOT Server
<img width="926" alt="clientm" src="https://github.com/Rav-Kiran123/Secure_Communication_Between_IOT_Devices_Using_RSA/assets/89346194/c31b69ac-c0da-4391-b55b-ab549cf79514">

## 5) We see that the server which is the iot device recives the message. We can also send the message from the iot device to the client. 
<img width="960" alt="iotr" src="https://github.com/Rav-Kiran123/Secure_Communication_Between_IOT_Devices_Using_RSA/assets/89346194/86b6052c-0233-43c1-b099-5bc92eb7f950">
