# Programming Assignment 2
# People involved in the assignment :- 
# Vasu Sharma and Manan Khasgiwale


# Product database 
        This particular database is hosted in Cloud SQL. Below are tables stored in the database :-
        1. Items

# Customer database
        This particular database is hosted in Cloud SQL. Below are the tables stored in the database :-
        1) Buyers
        2) Sellers
        3) Buyer Cart

# Search Semantics
        We have an indexing of items per category grouping and have used atleast one keyword matching as 
        the search criteria. We extract the search results as objects of model Items from the database


# Components on the server side
    1) GRPC seller server :- Hosted on Google compute engine. This acts as grpc interface to the database which works on the
       seller requests.
    2) REST seller server :- Hosted on Google compute engine. This acts as a rest interface for the seller client.
    3) GRPC buyer server :- Hosted on Google compute engine. This acts as grpc interface to the database which works on the 
       buyer requests.
    4) REST buyer server :- Hosted on Google compute engine. This acts as a rest interface for the seller client.
    5) Financial transactions SOAP server :- Hosted on Google compute engine. This acts as a payment gateway which is used 
       to help with making the purchase for items in the buyers' cart.
    6) Cloud SQL :- This is google managed PostgresSQL database which we are using for product and customer databases. Both these 
       databases run on separate instances and can be scaled independently. 



# Current state of the system
        1) All the APIs are implemented.
        2) There are currently five separate server components in the system that run as separate microservices on cloud.
        3) The two database run on separate instances in Cloud SQL.  
        4) Seller server can handle multiple sellers simultanously.
        5) Buyer server can handle multiple buyers simultaneously.
        6) The database can also process concurrent buyer and seller requests.
        7) Buyer client is used to emulate the functionality of a buyer.
        8) Seller client is used to emulate the functionality of a seller.
        9) Both buyer and seller clients have an interactive UI.
        10) The search function is performed via indexing of items by category.
        11) All the server components are asynchronous in nature.


# Assumptions
        1) In make purchase while checking out the items if the item availability is less than the quantity in 
           buyer cart then we are removing that item from the current cart. We will bill the other items while 
           making purchase and exclude this item.
        2) We are taking item_id and feedback from the buyer for provide_feedback api. We only allow one item feedback 
           per api call. If the buyer wants to provide feedback for other items then the buyer will use the same api
           again.
        3) We don't update the state of the system if the operations lead to illogical state which makes the system 
           fault tolerant.


# How to run
        1) All the server side microservices are running on Google Cloud behind reserved static IP addresses.
        2) The client side uses a terminal menu to communicate the rest server microservices in the cloud.
        4) Run the seller_client which will connect REST Seller_server
        5) Use the interactive menu to perform seller side operations.
        6) Run the Buyer_client and use the interactive menu to perform buyer side operations.
        7) Perform the client side operations in any order and the system would handle it without breaking.
        8) Commands to start all the processes in order :-
            d) python3 Seller_client/seller_client.py
            e) python3 Buyer_client/buyer_client.py


# Round trip latencies for APIs
        Client and server are running on same host.

        Seller APIs
            1) Create Seller Account
            2) Login using Seller Account
            3) Logout
            4) Put an item for sale: 0.567 ms
            5) Change the sale price of an item: 1.107 ms
            6) Remove an item for sale: 1.030 ms
            7) Display items currently on sale put up by this seller: 0.510 ms
            8) Get seller rating

        Buyer APIs
            1) Create Buyer Account
            2) Login using Buyer Account
            3) Logout
            4) Search items for sale: 0.581 ms
            5) Add item to the shopping cart: 0.560 ms
            6) Remove item from the shopping cart: 1.503 ms
            7) Clear the shopping cart: 0.531 ms
            8) Display the shopping cart: 0.621 ms
            9) Make purchase
            10) Provide feedback
            11) Get Seller rating
            12) Get Purchase history


# Extensibility of the current system
        1) All the servers are running as separate containers on cloud and can be scaled according to the usage.
        2) The databases are running as separate instances and can have different configuration for scalability and 
           replication 
        3) We have individual microservices for each bounded context. If new unrelated functionality arises we can 
           write that up as a different service and deploy it in a separate container to maintain isolation and cater
           different scalability needs.
        4) The request callbacks can be extended to include new or update existing client requests in the future.