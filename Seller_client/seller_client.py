# importing the requests library 
import requests 
import json
from datetime import datetime

  
# defining the api-endpoint  
API_ENDPOINT = "http://localhost:8080/"

seller_id = 0

def pretty_print(li):
    for val in li:
        print(val)

while(True):
    print("=============")
    print(" ")
    if seller_id == 0 or seller_id is None:
        print("Seller Menu")
        print("1. Create Account")
        print("2. Login")
        print("99. Quit Menu")
    else:
        print("Buyer Menu")
        print("1. Add Item")
        print("2. Change Item")
        print("3. Remove Item")
        print("4. Display Item")
        print("5. Get seller rating")
        print("10. Logout")
        print("99. Quit Menu")
        print(" ")
    print("=============")
    inp = int(input("Enter selection :- "))
    print("=============")


    if inp == 99:
        break

    data = {}
    resp_message = ""
    if seller_id == 0:
        if inp == 1:
            name = input("Enter name :- ")
            user_name = input("Enter user_name :- ")
            password = input("Enter password :- ")
            data = {
                'name': name,
                'user_name': user_name,
                'password': password
            }
            resp_message = requests.post(url = API_ENDPOINT+'create_account', data = json.dumps(data))
            if resp_message.status_code == 200:
                res_dict = resp_message.json()
                #seller_id = res_dict.get('seller_id')
                print('Successfully created account')
            else:
                print('Account creation unsuccessful')
        if inp == 2:
            user_name = input("Enter user_name :- ")
            password = input("Enter password :- ")
            data = {
                'user_name': user_name,
                'password': password
            }
            resp_message = requests.post(url = API_ENDPOINT+'login', data = json.dumps(data))
            print(resp_message)
            if resp_message.status_code != 200:
                print('Unsuccessful log in')
            else:
                res_dict = resp_message.json()
                seller_id = res_dict.get('seller_id')
                print('Successfully logged in')
    else: # seller_id is present
        if inp == 1:
            name = input("Enter item name :- ")
            category = int(input("Enter item category :- "))
            keywords = input("Enter keywords(upto 5) :- ")
            keywords = keywords.split(' ')
            condition = int(input("Enter item condition(0=OLD, 1=NEW) :- "))
            sale_price = int(input("Enter item sale price :- "))
            quantity = int(input("Enter item quantity :- "))

            curr_time = datetime.now()
            data = {
                'name': name,
                'category': category,
                'condition': condition,
                'keywords': keywords,
                'sale_price': sale_price,
                'quantity': quantity,
                'seller_id': seller_id
            }
            resp_message = requests.post(url = API_ENDPOINT+'add_item', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Item addition was not successful')
            else:
                res_dict = resp_message.json()
                print('Successfully added items')
        if inp == 2:
            item_id = int(input("Enter item id :- "))
            sale_price = int(input("New sale price :- "))

            curr_time = datetime.now()
            data = {
                'seller_id': seller_id,
                'item_id': item_id,
                'sale_price': sale_price
            }
            resp_message = requests.post(url = API_ENDPOINT+'change_item', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful item sale price change')
            else:
                res_dict = resp_message.json()
                print('Successfully changed items')
        if inp == 3:
            item_id = int(input("Enter item_id :- "))
            quantity = int(input("Enter quantity :- "))

            curr_time = datetime.now()
            data = {
                'seller_id': seller_id,
                'item_id': item_id,
                'quantity': quantity
            }
            resp_message = requests.post(url = API_ENDPOINT+'remove_item', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful item removal')
            else:
                res_dict = resp_message.json()
                print('Successfully removed item')
        if inp == 4:
            curr_time = datetime.now()
            data = {
                'seller_id': seller_id
            }
            resp_message = requests.post(url = API_ENDPOINT+'display_item', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful in displaying cart')
            else:
                res_dict = resp_message.json()
                print('cart contains :- ')
                pretty_print(res_dict.get('items'))
        if inp == 5:
            curr_time = datetime.now()
            data = {
                'seller_id': seller_id
            }
            resp_message = requests.post(url = API_ENDPOINT+'get_seller_rating', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful in getting seller rating')
            else:
                res_dict = resp_message.json()
                print('Successful in getting seller_rating ', res_dict.get('rating'))
        if inp == 10:
            curr_time = datetime.now()
            resp_message = requests.post(url = API_ENDPOINT+'logout')
            if resp_message.status_code == 200:
                res_dict = resp_message.json()
                seller_id = res_dict.get('seller_id')
                print('Successfully logged out')
            else:
                print('Unsuccessful in logging out')