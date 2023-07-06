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

## 4) Enter Y and then enter your Username and Password you had given before and then enter whatever message you want to send to the IOT Server. The message gets encrypted using RSA
<img width="791" alt="clientm" src="https://github.com/Rav-Kiran123/Secure_Communication_Between_IOT_Devices_Using_RSA/assets/89346194/a7d73663-4f66-4bdf-a609-22848d6af485">

## 5) We see that the server which is the iot device receives the decrypted message. This way we can send encrypted messages to the IOT device
<img width="785" alt="iotr" src="https://github.com/Rav-Kiran123/Secure_Communication_Between_IOT_Devices_Using_RSA/assets/89346194/bc2cad3b-1f0c-4fec-8674-d9beb4c5b3e0">
