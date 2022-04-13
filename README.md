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
    cd ~/cs441_t6/basic
    python node1-listener.py
    ```
4. Run the other python files in separate ubuntu consoles:
    ```
    python node2-listener.py
    python node3-listener.py
    python router-nic1.py
    python router-nic2.py
    ```
    ### Ping Protocol Example (Node 1 Ping Node 3)
    **Note: Ping Protocol can ping all 3 nodes and router**  
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

?????????????????????????????????????????????????????????????

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

    Router 1 Console
    ```
    The packed received:
    Source MAC address: N1, Destination MAC address: R1

    Source IP address: 0x1A, Destination IP address: 0x2B

    Protocl: 0

    Data Length: 11

    Message: hello node3

    PACKET NOT FOR ME.
    Packet received for destination outside network...
    Forwarding to router-nic2...
    CURRENT SOURCE MAC ADDRESS: N1
    CURRENT DESTINATION MAC ADDRESS: R1
    CHANGING SOURCE MAC ADDRESS TO R1...
    CHANGING MAC ADDRESS TO R2...
    R1
    0x1A

    The packed received:
    Source MAC address: R2, Destination MAC address: R1

    Source IP address: 0x2B, Destination IP address: 0x1A

    Protocl: 0

    Data Length: 11

    Message: hello node3

    PACKET NOT FOR ME.
    Packet received for destination current network...
    Forwading to current network...
    CURRENT SOURCE MAC ADDRESS: R2
    CURRENT DESTINATION MAC ADDRESS: R1
    CHANGING SOURCE MAC ADDRESS TO R1...
    CHANGING MAC ADDRESS TO N1...
    ```

    Router 2 Console
    ```
    The packed received:
    Source MAC address: R1, Destination MAC address: R2

    Source IP address: 0x1A, Destination IP address: 0x2B

    Protocl: 0

    Data Length: 11

    Message: hello node3

    PACKET NOT FOR ME.
    Packet received for destination current network...
    Forwading to current network...
    CURRENT SOURCE MAC ADDRESS: R1
    CURRENT DESTINATION MAC ADDRESS: R2
    CHANGING SOURCE MAC ADDRESS TO R2...
    CHANGING MAC ADDRESS TO N3...
    R2
    0x1A

    The packed received:
    Source MAC address: N3, Destination MAC address: R2

    Source IP address: 0x2B, Destination IP address: 0x1A

    Protocl: 0

    Data Length: 11

    Message: hello node3

    PACKET NOT FOR ME.
    Packet received for destination outside network...
    Forwarding to router-nic1...
    CURRENT SOURCE MAC ADDRESS: N3
    CURRENT DESTINATION MAC ADDRESS: R2
    CHANGING SOURCE MAC ADDRESS TO R2...
    CHANGING MAC ADDRESS TO R1...
    ```

    ### Log Protocol (Node 1 to Node 3 Log Protocol)
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

    d. A node3.log log file would be created in the basic folder
    ![This is an image](https://github.com/wellsonah2019/cs441_t6/tree/main/images/node3_log.PNG)


    ### Kill Protocol

    ### Simple Messaging
    
    ### IP Filter/Firewall
    
    ### IP Spoofing

## 2. ARP Poisoning

## 3. TCP Session Hijacking MITM
