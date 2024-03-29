# Programming Assignment 2
# People involved in the assignment :- 
# Vasu Sharma and Manan Khasgiwale


# Product database 
        This particular database is hosted in Cloud SQL. Below are tables stored in the database :-
        1) Items
                                                            Table "public.items"
            Column   |          Type          | Collation | Nullable | Default | Storage  | Stats target | Description
         ------------+------------------------+-----------+----------+---------+----------+--------------+-------------
         name       | character varying(32)  |           | not null |         | extended |              |
         category   | smallint               |           | not null |         | plain    |              |
         id         | bigint                 |           | not null |         | plain    |              |
         condition  | boolean                |           | not null |         | plain    |              |
         keywords   | character varying(8)[] |           |          |         | extended |              |
         sale_price | numeric                |           | not null |         | main     |              |
         quantity   | integer                |           | not null |         | plain    |              |
         seller_id  | bigint                 |           | not null |         | plain    |              |


# Customer database
        This particular database is hosted in Cloud SQL. Below are the tables stored in the database :-
        1) Buyers
        2) Sellers
        3) Buyer Cart

                                                         Table "public.buyers"
               Column        |         Type          | Collation | Nullable | Default | Storage  | Stats target | Description
         ---------------------+-----------------------+-----------+----------+---------+----------+--------------+-------------
         name                | character varying(32) |           | not null |         | extended |              |
         id                  | bigint                |           | not null |         | plain    |              |
         num_items_purchased | integer               |           |          | 0       | plain    |              |
         user_name           | character varying(32) |           | not null |         | extended |              |
         password            | character varying(32) |           | not null |         | extended |              |
         Indexes:
            "buyers_pkey" PRIMARY KEY, btree (id)
         Access method: heap



                                                         Table "public.sellers"
            Column     |         Type          | Collation | Nullable |  Default  | Storage  | Stats target | Description
         ----------------+-----------------------+-----------+----------+-----------+----------+--------------+-------------
         name           | character varying(32) |           | not null |           | extended |              |
         id             | bigint                |           | not null |           | plain    |              |
         feedback       | seller_feedback       |           |          | ROW(0, 0) | extended |              |
         num_items_sold | integer               |           |          | 0         | plain    |              |
         user_name      | character varying(32) |           | not null |           | extended |              |
         password       | character varying(32) |           | not null |           | extended |              |
         Indexes:
            "sellers_pkey" PRIMARY KEY, btree (id)
            "user_name_seller_index" UNIQUE, btree (user_name)
         Access method: heap

                                                         Table "public.buyer_cart"
            Column     |            Type             | Collation | Nullable |      Default      | Storage | Stats target | Description
         ---------------+-----------------------------+-----------+----------+-------------------+---------+--------------+-------------
         buyer_id      | bigint                      |           | not null |                   | plain   |              |
         item_id       | bigint                      |           | not null |                   | plain   |              |
         quantity      | integer                     |           |          |                   | plain   |              |
         checked_out   | boolean                     |           | not null |                   | plain   |              |
         seller_review | review_type                 |           |          | 'NA'::review_type | plain   |              |
         updated_at    | timestamp without time zone |           | not null | now()             | plain   |              |
         Indexes:
            "buyer_cart_pkey" PRIMARY KEY, btree (buyer_id, item_id, checked_out, updated_at)
         Access method: heap


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
      2) There are currently five separate lightweight server components in the system that run as separate microservices on cloud.
         Each of the services are running as containerized applications on the cloud.
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
            1) Create Seller Account: 464.261 ms
            2) Login using Seller Account: 215.585 ms
            3) Logout: 145.294 ms
            4) Put an item for sale: 422.679 ms
            5) Change the sale price of an item: 228.51 ms
            6) Remove an item for sale: 288.625 ms
            7) Display items currently on sale put up by this seller: 215.904 ms
            8) Get seller rating: 211.828 ms

        Buyer APIs
             1) Create Buyer Account: 404.968 ms
             2) Login using Buyer Account: 221.506 ms
             3) Logout: 140.996 ms
             4) Search items for sale: 526.507 ms
             5) Add item to the shopping cart: 471.546 ms
             6) Remove item from the shopping cart: 444.972 ms
             7) Clear the shopping cart: 208.482 ms
             8) Display the shopping cart: 258.078 ms
             9) Make purchase: 792.865 ms
            10) Provide feedback: 467.861 ms
            11) Get Seller rating: 185.848 ms
            12) Get Purchase history: 267.284 ms


# Extensibility of the current system
        1) All the servers are running as separate containers on cloud and can be scaled according to the usage.
        2) The databases are running as separate instances and can have different configuration for scalability and 
           replication 
        3) We have individual microservices for each bounded context. If new unrelated functionality arises we can 
           write that up as a different service and deploy it in a separate container to maintain isolation and cater
           different scalability needs.
        4) The request callbacks can be extended to include new or update existing client requests in the future.