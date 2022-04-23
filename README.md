# How to Run the Project
**Note: Please run this project in ubuntu console**
## 1. Basic Network Emulation
1. Clone the project to ubuntu home -- git clone https://github.com/wellsonah2019/cs441_t6.git
2. Open ubuntu console and install python-is-python3:
    ```
    sudo apt-get install python-is-python3 -y
    ```
3. Open ubuntu console and run the commands below:
    ```
    cd ~/cs441_t6
    python node1-listener.py
    ```
4. Run the other python files in separate ubuntu consoles:
    ```
    python node2-listener.py
    python node3-listener.py
    python router-nic1.py
    python router-nic2.py
    ```
    ### Ping Protocol (Node 1 Ping Node 3 Example)
    **Note: Ping Protocol works for all 3 nodes and router**  
    a. Input 0 in the console where node1-listener.py is run and press Enter to choose Ping Protocol
    ```
    [Node 1]
    Please select what protocol you would like to use:
    0. Ping Protocol
    1. Log Protocol
    2. Kill Protocol
    3. Simple Messaging
    5. ARP Poisoning
    7. IP SPOOFING
    0
    ```
    
    b. Insert the destination (Node 3's IP address) and press Enter
    ```
    Please insert the destination: 0x2B
    ```
    
    c. Insert the message you want to send to node 3 and press Enter
    ```
    Please insert the message you want to send: hello node3
    ```

    Node 3 Console (Successful Ping from Node 1)
    ```
    ----------- [14:36:44] -----------

    The packet received:
    Source MAC address: R2, Destination MAC address: N3

    Source IP address: 0x1A, Destination IP address: 0x2B

    Protocol: Ping

    Data Length: 011

    Message: hello node3
    ----------------------------------
    Ping successful:  9.165
    ```
    
    Node 1 Console (Reply from Node 3)
    ```
     Reply from 0x2B
    -----------04/13/2022, 14:36:44-----------

    The packet received:
    Source MAC address: R1, Destination MAC address: N1

    Source IP address: 0x2B, Destination IP address: 0x1A

    Protocol: Ping

    Data Length: 11

    Message: hello node3

    Approximate round trip in ms: 24.05
    ----------------------------------
    ```

    Node 3 Console
    ```
    ----------- [14:36:44] -----------

    The packet received:
    Source MAC address: R2, Destination MAC address: N3

    Source IP address: 0x1A, Destination IP address: 0x2B

    Protocol: 0

    Data Length: 011

    Message: hello node3

    PACKET NOT FOR ME. DROPPING NOW...
    ----------------------------------
    packet received

    ----------- [14:36:44] -----------                              

    The packet received:
    Source MAC address: N3, Destination MAC address: R2

    Source IP address: 0x2B, Destination IP address: 0x1A

    Protocol: 0

    Data Length: 011

    Message: hello node3

    PACKET NOT FOR ME. DROPPING NOW...
    ----------------------------------
    packet received
    ```

    ### Log Protocol (Node 1 to Node 3 Log Protocol Example)
    **Note: Log Protocol works for all 3 nodes and router** 
    a. Input 1 in the console where node1-listener.py is run and press Enter to choose Ping Protocol
    ```
    [Node 1]
    Please select what protocol you would like to use:
    0. Ping Protocol
    1. Log Protocol
    2. Kill Protocol
    3. Simple Messaging
    5. ARP Poisoning
    7. IP SPOOFING
    1
    ```
    
    b. Insert the destination (Node 3's IP address) and press Enter
    ```
    Please insert the destination: 0x2B
    ```
    
    c. Insert the log details you want to send to node 3 and press Enter
    ```
    Please insert the log details: Hi node 3, I'm node 1 (Log Protocol)
    ```

    d. A node3.log log file would be created in the basic folder as shown below
    ![[alt text]](https://github.com/wellsonah2019/cs441_t6/blob/main/basic/images/node3_log.PNG)

    Node 3 Console
    ```
    ----------- [14:46:34] -----------

    The packet received:
    Source MAC address: R2, Destination MAC address: N3

    Source IP address: 0x1A, Destination IP address: 0x2B

    Protocol: Log

    Data Length: 57

    Message: 04/13/2022, 14:46:34 Hi node 3, I'm node 1 (Log Protocol)
    ----------------------------------
    Successfully written to log file!
    ```

    (This part is not confirmed)  
    Node 2 Console
    ```
    ----------- [14:46:34] -----------

    The packet received:
    Source MAC address: R2, Destination MAC address: N3

    Source IP address: 0x1A, Destination IP address: 0x2B

    Protocol: 1

    Data Length: 57

    Message: 04/13/2022, 14:46:34 Hi node 3, I'm node 1 (Log Protocol)

    PACKET NOT FOR ME. DROPPING NOW...
    ----------------------------------
    packet received
    ```

    ### Kill Protocol (Node 1 Kill Node 2 Example)
    **Note: Kill Protocol works for all 3 nodes and router**  
    a. Input 2 in the console where node1-listener.py is run and press Enter to choose Kill Protocol
    ```
    [Node 1]
    Please select what protocol you would like to use:
    0. Ping Protocol
    1. Log Protocol
    2. Kill Protocol
    3. Simple Messaging
    5. ARP Poisoning
    7. IP SPOOFING
    2
    ```
    
    b. Insert the destination (Node 2's IP address) and press Enter
    ```
    Please insert the destination: 0x2A
    ```

    Node 2 Console (Node 2 has been successfully killed)
    ```
    ----------- [15:10:19] -----------

    The packet received:
    Source MAC address: R2, Destination MAC address: N2

    Source IP address: 0x1A, Destination IP address: 0x2A

    Protocol: Kill

    Data Length: 0

    Message:
    ----------------------------------
    Kill protocol has been given. Will exit now...
    jesst@DESKTOP-0PJ69ED:~/network-simulator/cs441_t6/basic$
    ```
    (This part is not confirmed)  
    Node 3 Console
    ```
    ----------- [15:10:19] -----------

    The packet received:
    Source MAC address: R2, Destination MAC address: N2

    Source IP address: 0x1A, Destination IP address: 0x2A

    Protocol: 2

    Data Length: 0

    Message:

    PACKET NOT FOR ME. DROPPING NOW...
    ----------------------------------
    ```
    

    ### Simple Messaging (Node 2 Sends Simple Messaging to Node 1 Example)
    **Note: Simple Messaging works for all 3 nodes and router**  
    a. Input 3 in the console where node1-listener.py is run and press Enter to choose Simple Messaging Protocol
    ```
    [Node 2]
    Please select what protocol you would like to use:
    0. Ping Protocol
    1. Log Protocol
    2. Kill Protocol
    3. Simple Messaging
    5. ARP Poisoning
    6. TCP Connection
    7. IP SPOOFING
    3
    ```
    
    b. Insert the destination (Node 1's IP address) and press Enter
    ```
    Please insert the destination: 0x1A
    ```
    
    c. Insert the message you want to send to node 1 and press Enter
    ```
    Please insert the message you want to send: good morning node 1!
    ```

    Node 1 Console
    ```
    ----------- [15:22:56] -----------

    The packet received:
    Source MAC address: R1, Destination MAC address: N1

    Source IP address: 0x2A, Destination IP address: 0x1A

    Protocol: Simple Messaging

    Data Length: 020

    Message: good morning node 1!
    ----------------------------------
    ```

    (This part not confirmed)  
    Node 3 Console
    ```
    ----------- [15:22:56] -----------

    The packet received:
    Source MAC address: N2, Destination MAC address: R2

    Source IP address: 0x2A, Destination IP address: 0x1A

    Protocol: 3

    Data Length: 20

    Message: good morning node 1!

    PACKET NOT FOR ME. DROPPING NOW...
    ----------------------------------
    ```
    Router 2 Console
    ```
    The packed received:
    Source MAC address: N2, Destination MAC address: R2

    Source IP address: 0x2A, Destination IP address: 0x1A

    Protocl: 3

    Data Length: 20

    Message: good morning node 1!

    PACKET NOT FOR ME.
    Packet received for destination outside network...
    Forwarding to router-nic1...
    CURRENT SOURCE MAC ADDRESS: N2
    CURRENT DESTINATION MAC ADDRESS: R2
    CHANGING SOURCE MAC ADDRESS TO R2...
    CHANGING MAC ADDRESS TO R1...
    ```

    Router 1 Console
    ```
    The packed received:
    Source MAC address: R2, Destination MAC address: R1

    Source IP address: 0x2A, Destination IP address: 0x1A

    Protocl: 3

    Data Length: 20

    Message: good morning node 1!

    PACKET NOT FOR ME.
    Packet received for destination current network...
    Forwading to current network...
    CURRENT SOURCE MAC ADDRESS: R2
    CURRENT DESTINATION MAC ADDRESS: R1
    CHANGING SOURCE MAC ADDRESS TO R1...
    CHANGING MAC ADDRESS TO N1...
    received from outside network -- will pass to cable
    ```
    
    ### IP Filter/Firewall
    
    ### IP Spoofing

## 2. ARP Poisoning

## 3. TCP Session Hijacking MITM
