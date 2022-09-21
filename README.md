# RUDP Chat app

> Made by Nerya Bigon  

IRC Group Chat with Reliable UDP File Transfer  

In this project we implemented a chat application that consists of:
1. Basic messaging and file transfer over TCP.
2. Transfer of files over UDP using the [RUDP](https://en.wikipedia.org/wiki/Reliable_User_Datagram_Protocol) protocol.
3. Managing users, files and messaging with [Firebase](https://firebase.google.com/).
4. Gui for the client side is made with the [Kivy](https://kivy.org/#aboutus) and [KivyMD](https://github.com/kivymd/KivyMD) frameworks.


## The RUDP algorithm
for the reliable UDP I've implemented something close to [selective repeat](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ) congestion control.   
in addition to flow control which is similar to the [cubic](https://en.wikipedia.org/wiki/CUBIC_TCP) algorithm.    
1.	Client send file request to the server.
2.	Three-way handshake is established over UDP.
3.	Starting with windows size of 3, load the pockets into the window and send them one by one.
4.	Wait for ACKs. 
5.	The algorithm will resend any pockets that hasn't received an ACK.
6.	After all the packets in the window received ACK the window's size is increased by two times ([slow start](https://en.wikipedia.org/wiki/TCP_congestion_control#Slow_start)) only until reaching half of the last maximal window size.
7.	Using flow control to increase and decrease the window size in the event of duplicate ACK we decrease the window size by half and continuing sending the packets.
8.	In the event of a timeout we consider this as very serious event and decrease window size to one, and start a slow start all over again.  

//TODO: add a state diagram

## UML
//TODO: add UML diagram


# How To Run

Download this repository and follow this steps:
* Make sure that the correct IP addresses are in both the server file and in the client file.

1. open a terminal window in the folder with the `server_main.py` file.
2. run the following command:  

```
python3 server_main.py
```

3. open a second terminal window, in the root folder.
4. run the folowing comand:  

```
python3 main.py
```

5. Since we used a database, you first have to register or else you wont be able to login.
7. After you successfully lodged in you can send messages freely.

## Prerequisites
Kivy - see [here](https://kivy.org/doc/stable/gettingstarted/installation.html) for installation instructions.  
KivyMD - see [here](https://kivymd.readthedocs.io/en/latest/getting-started/) for installation instructions.

## GUI screenshots
//TODO: add screenshots of the GUI