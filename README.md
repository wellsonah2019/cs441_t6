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
    
    ### IP Filter/Firewall (only for node3)
    
    a. Input 4 in the console where node3-listener.py is run and press Enter to choose Configure Firewall
    ```
    [Node 3]
    Please select what protocol you would like to use:
    0. Ping Protocol
    1. Log Protocol
    2. Kill Protocol
    3. Simple Messaging
    4. Configure Firewall
    5. ARP Poisoning
    6. TCP Connection
    7. IP SPOOFING
    4
    ```
    
    b. Input the IP to be blocked
    
    ```
    Current firewall configuration:
    Blocked IPs: []
    Please enter the IP address to be blocked, or [exit]: 0x2A
    ```
    
    c. 0x2A is now blocked.
    
    ### IP Spoofing
    a. Input 7 in the console where node3-listener.py is run and press Enter to choose Simple Messaging Protocol
    ```
    [Node 3]
    Please select what protocol you would like to use:
    0. Ping Protocol
    1. Log Protocol
    2. Kill Protocol
    3. Simple Messaging
    4. Configure Firewall
    5. ARP Poisoning
    6. TCP Connection
    7. IP SPOOFING
    7
    ```
    
    b.  Input the destination IP, fake IP to spoof, and the message
    ```
    Please insert the destination: 0x2A
    FAKE IP TO SPOOF: 0x21
    Please insert the message you want to send: dkjsdfjklkjsdf
    ```
    c. Node 2 (0x2A) will now receive a packet from IP 0x21 (router's IP) and MAC N3 (Node3's MAC)
    ```
    ----------- [13:39:15] -----------

    The packet received:
    Source MAC address: N3, Destination MAC address: N2

    Source IP address: 0x21, Destination IP address: 0x2A

    Protocol: Simple Messaging

    Data Length: 5

    Message: hello
    ----------------------------------
    packet received
    ```
    
## 2. ARP Poisoning
1. Input 5 in node2-listener.py to choose ARP Poisoning
2. Input the destination IP and the fake IP
    ```
    5
    Please insert the destination: 0x2B
    Please insert your fake IP: 0x21
    ```
3. Node 3 (0x2B)'s ARP Table now has been modified (notice how 0x21 is pointing to N2 instead of R2)
    ```
    {   
    "0x21": "N2", 
    "0x2A": "N2", 
    "0x2C": "N4"
    }
    ```
    
## 3. TCP Session Hijacking MITM
Note: this only works between node2-listener and node3-listener and attacker-node-listener needs to be run for hijacking
1. In node2-listener.py, input 6 to choose TCP connection
2. The TCP handshake and MITM hijacking will be done automatically
3. To prove the attack is successful, attacker can send another TCP packet
    a. In attacker-node-listener.py, input 6 to choose TCP Connection
    b. Enter destination as 0x2A and input any arbitrary random message
    ```
    Please insert the destination: 0x2A
    Enter message please: helllooo
    ```
    c. Node 2 will now accept the packet, thinking that it is from Node3 (with the correct SEQ and ACK, and the spoofed IP and MAC)
    ```
    The packet received:
    Source MAC address: N3, Destination MAC address: N2

    Source IP address: 0x2B, Destination IP address: 0x2A

    Protocol: TCP

    Data Length: 008

    TCP Control Flag: ACK

    Seq: 51

    Ack: 22

    Message: helllooo
    ----------------------------------
    0x2B
    dest ip in local arp table
    packet received
    ```
    d. Node 2 can also send TCP packets (by doing the same as step b. and c.) to Node 3, but Node 3 will drop the packet because the SEQ and ACK numbers are invalid
    ```
    The packet received:
    Source MAC address: N2, Destination MAC address: N3

    Source IP address: 0x2A, Destination IP address: 0x2B

    Protocol: TCP

    Data Length: 008

    TCP Control Flag: ACK

    Seq: 60

    Ack: 51

    Message: helloooo
    [!] Invalid TCP Packet, Packet has been dropped.
    ```
    e. Attacker node, however, will accept this packet
    
    ```
    The packet received:
    Source MAC address: N2, Destination MAC address: N3

    Source IP address: 0x2A, Destination IP address:

    Protocol: TCP

    Data Length: 008

    TCP Control Flag: ACK

    Seq: 60

    Ack: 51

    Message: helloooo
    ----------------------------------
    packet received
    ```
    

