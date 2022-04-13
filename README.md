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
    Node 1 Console
    ```
    [Node 1]
    Please select what protocol you would like to use:
    0. Ping Protocol
    1. Log Protocol
    2. Kill Protocol
    3. Simple Messaging
    5. ARP Poisoning
    0
    Please insert the destination: 0x2B
    Please insert the message you want to send: hello node2
    0.163626
    Reply from 0x2B
    -----------04/07/2022, 19:09:31-----------

    The packet received:
    Source MAC address: R1, Destination MAC address: N1

    Source IP address: 0x2B, Destination IP address: 0x1A

    Protocol: Ping

    Data Length: 11

    Message: hello node2

    Approximate round trip in ms: 163.63
    ----------------------------------
    ```

    Node 3 Console
    ```
    ----------- [19:09:31] -----------

    The packet received:
    Source MAC address: R2, Destination MAC address: N3

    Source IP address: 0x1A, Destination IP address: 0x2B

    Protocol: Ping

    Data Length: 011

    Message: hello node2
    ----------------------------------
    Ping successful:  129.441
    ```

    ### Log Protocol

    ### Kill Protocol

    ### Simple Messaging
    
    ### IP Filter/Firewall
    
    ### IP Spoofing

## 2. ARP Poisoning

## 3. TCP Session Hijacking MITM
