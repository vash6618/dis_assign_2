# importing the requests library 
import requests 
import json
from datetime import datetime

  
# defining the api-endpoint  
API_ENDPOINT = "http://34.106.107.200:8080/"

buyer_id = 0

def pretty_print(li):
    for val in li:
        print(val)

while(True):
    print("=============")
    print(" ")
    if buyer_id == 0 or buyer_id is None:
        print("Buyer Menu")
        print("1. Create Account")
        print("2. Login")
        print("99. Quit Menu")
    else:
        print("Buyer Menu")
        print("1. Search Items for sale")
        print("2. Add Item to shopping cart")
        print("3. Remove Item from shopping cart")
        print("4. Clear shopping cart")
        print("5. Display shopping cart")
        print("6. Make purchase")
        print("7. Provide Feedback")
        print("8. Get seller rating")
        print("9. Get buyer history")
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
    if buyer_id == 0:
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
                #buyer_id = res_dict.get('buyer_id')
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
                buyer_id = res_dict.get('buyer_id')
                print('Successfully logged in')
    else: # buyer_id is present
        if inp == 1:
            category_inp = int(input("Enter item category :- "))
            keywords = input("Enter keywords(upto 5) :- ")

            curr_time = datetime.now()
            keywords = keywords.split(' ')
            data = {
                'buyer_id': buyer_id,
                'category': category_inp,
                'keywords': keywords
            }
            resp_message = requests.post(url = API_ENDPOINT+'search_items', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Search was not successful')
            else:
                res_dict = resp_message.json()
                print('Search Results :- ')
                pretty_print(res_dict)
        if inp == 2:
            item_id = int(input("Enter item id to add to cart :- "))
            quantity = int(input("Enter quantity :- "))

            curr_time = datetime.now()
            data = {
                'buyer_id': buyer_id,
                'item_id': item_id,
                'quantity': quantity
            }
            resp_message = requests.post(url = API_ENDPOINT+'add_to_cart', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful item addition')
            else:
                res_dict = resp_message.json()
                print('Successfully added items')
        if inp == 3:
            item_id = int(input("Enter item id to remove from cart :- "))
            quantity = int(input("Enter quantity :- "))

            curr_time = datetime.now()
            data = {
                'buyer_id': buyer_id,
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
                'buyer_id': buyer_id
            }
            resp_message = requests.post(url = API_ENDPOINT+'clear_cart', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful cart clear')
            else:
                res_dict = resp_message.json()
                print('Successfully cleared cart')
        if inp == 5:
            curr_time = datetime.now()
            data = {
                'buyer_id': buyer_id
            }
            resp_message = requests.post(url = API_ENDPOINT+'display_cart', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful in displaying cart')
            else:
                res_dict = resp_message.json()
                print('cart contains :- ')
                pretty_print(res_dict.get('items'))
        if inp == 6:
            credit_card_name = input("Enter name on credit card :- ")
            credit_card_number = input("Enter credit card number :- ")
            exp_date = input("Enter expiry date :- ")
            curr_time = datetime.now()
            data = {
                'buyer_id': buyer_id # add other once SOAP
            }
            resp_message = requests.post(url = API_ENDPOINT+'make_purchase', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful in purchasing items')
            else:
                res_dict = resp_message.json()
                print('Successfully purchased items')
        if inp == 7:
            item_id = int(input("Enter item id :- "))
            feedback = int(input("Enter feedback(0=DOWN, 1=UP) :- "))
            feedback = True if feedback == 1 else False
            curr_time = datetime.now()
            data = {
                'buyer_id': buyer_id,
                'item_id': item_id,
                'feedback': feedback
            }
            resp_message = requests.post(url = API_ENDPOINT+'provide_feedback', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful in providing feedback')
            else:
                res_dict = resp_message.json()
                print('Successfully provided feedback')
        if inp == 8:
            seller_id = int(input("Enter seller_id :- "))
            curr_time = datetime.now()
            data = {
                'buyer_id': buyer_id,
                'seller_id': seller_id
            }
            resp_message = requests.post(url = API_ENDPOINT+'get_seller_rating', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful in getting seller rating')
            else:
                res_dict = resp_message.json()
                print('Successful in getting seller_rating ', res_dict.get('rating'))
        if inp == 9:
            curr_time = datetime.now()
            data = {
                'buyer_id': buyer_id
            }
            resp_message = requests.post(url = API_ENDPOINT+'get_buyer_history', data = json.dumps(data))
            if resp_message.status_code != 200:
                print('Unsuccessful in getting purchase history')
            else:
                res_dict = resp_message.json()
                print('purchase history :- ')
                pretty_print(res_dict.get('items'))
        if inp == 10:
            curr_time = datetime.now()
            resp_message = requests.post(url = API_ENDPOINT+'logout')
            if resp_message.status_code == 200:
                res_dict = resp_message.json()
                buyer_id = res_dict.get('buyer_id')
                print('Successfully logged out')
            else:
                print('Unsuccessful in logging out')
        

# sending post request and saving response as response object 
# resp_message = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
# pastebin_url = r.text 
# print("The pastebin URL is:%s"%pastebin_url)