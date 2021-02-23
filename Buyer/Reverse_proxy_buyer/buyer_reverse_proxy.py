"""The Python AsyncIO implementation of the GRPC helloworld.Greeter client."""
import grpc

import buyer_pb2
import buyer_pb2_grpc
from aiohttp import web
import json
from google.protobuf.timestamp_pb2 import Timestamp


def parse_params(request):
    query_string = request.query_string
    params = query_string.split('&')
    return params


# async def get_item_handler(request):
#     params = parse_params(request)
#     id = int(params[0].split('=')[1])
#     async with grpc.aio.insecure_channel('localhost:5001') as channel:
#         stub = buyer_pb2_grpc.BuyerMasterStub(channel)
#         response = await stub.GetItem(buyer_pb2.GetItemRequest(id=id))
#     buyer_request = response.item
#     dict_resp = {'name': item.name, 'category': item.category, 'condition': item.condition,
#                  'keywords': list(item.keywords), 'sale_price': item.sale_price, 'quantity': item.quantity,
#                  'seller_id': item.seller_id}
#     print(dict_resp)
#     return web.Response(text=json.dumps(dict_resp))

async def add_to_cart_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.AddToCart(buyer_pb2.AddToCartRequest(
                                buyer_id=buyer_request.get('buyer_id'),
                                item_id=buyer_request.get('item_id'),
                                quantity=buyer_request.get('quantity')))
    add_to_cart_resp = {'buyer_id': response.buyer_id}
    return web.Response(text=json.dumps(add_to_cart_resp))


async def remove_item_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.RemoveItemFromShoppingCart(buyer_pb2.RemoveItemFromShoppingCartRequest(
                                buyer_id=buyer_request.get('buyer_id'),
                                item_id=buyer_request.get('item_id'),
                                quantity=buyer_request.get('quantity')))
    remove_item_resp = {'buyer_id': response.buyer_id}
    return web.Response(text=json.dumps(remove_item_resp))


async def clear_cart_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.ClearCart(buyer_pb2.ClearCartRequest(buyer_id=buyer_request.get('buyer_id')))
    
    clear_cart_resp = {'buyer_id': response.buyer_id}
    return web.Response(text=json.dumps(clear_cart_resp))


async def display_cart_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.DisplayCart(buyer_pb2.DisplayCartRequest(buyer_id=buyer_request.get('buyer_id')))
    cart_items = response.items
    cart_list = []
    for item in cart_items:
        cart_list.append({'buyer_id':item.buyer_id, 'item_id':item.item_id, 
                          'quantity':item.quantity,'name': item.name, 'category': item.category, 
                          'condition': item.condition, 'keywords': list(item.keywords), 
                          'sale_price': item.sale_price, 'seller_id': item.seller_id,
                          'updated_at': Timestamp().ToDatetime(item.updated_at).isoformat()})

    display_cart_resp = {'items': cart_list}
    return web.Response(text=json.dumps(display_cart_resp))

async def create_account_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.CreateAccount(buyer_pb2.CreateAccountRequest(
                                name=buyer_request.get('name'),
                                user_name=buyer_request.get('user_name'),
                                password=buyer_request.get('password')))
    create_account_resp = {'buyer_id': response.buyer_id}

    return web.Response(text=json.dumps(create_account_resp))


async def login_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.Login(buyer_pb2.LoginRequest(
                                user_name=buyer_request.get('user_name'),
                                password=buyer_request.get('password')))
    
    login_resp = {'buyer_id': response.buyer_id}
    return web.Response(text=json.dumps(login_resp))


async def logout_handler(request):
    logout_resp = {'buyer_id': 0}
    return web.Response(text=json.dumps(logout_resp))

async def make_purchase_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.MakePurchase(buyer_pb2.MakePurchaseRequest(
                                buyer_id=buyer_request.get('buyer_id')))

    make_purchase_resp = {'buyer_id': response.buyer_id, 'transaction_status': response.transaction_status}
    return web.Response(text=json.dumps(make_purchase_resp))

# async def provide_feedback(request):
#     buyer_request = json.loads(await request.text())
#     async with grpc.aio.insecure_channel('localhost:5001') as channel:
#         stub = buyer_pb2_grpc.BuyerMasterStub(channel)
#         response = await stub.DisplayCart(buyer_pb2.DisplayCartRequest(buyer_id=buyer_request.get('buyer_id')))
#     cart_items = response.items
#     cart_list = []
#     for item in cart_items:
#         cart_list.append({'buyer_id':item.buyer_id, 'item_id':item.item_id, 
#                           'quantity':item.quantity,'name': item.name, 'category': item.category, 
#                           'condition': item.condition, 'keywords': list(item.keywords), 
#                           'sale_price': item.sale_price, 'seller_id': item.seller_id})

#     display_cart_resp = {'items': cart_list}
#     return web.Response(text=json.dumps(display_cart_resp))

async def get_seller_rating_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.GetSellerRating(buyer_pb2.GetSellerRatingRequest(seller_id=item.get('seller_id')))
    
    get_seller_rating_resp = {'rating': response.rating}
    return web.Response(text=json.dumps(get_seller_rating_resp))

async def get_buyer_history_handler(request):
    buyer_request = json.loads(await request.text())
    async with grpc.aio.insecure_channel('localhost:5001') as channel:
        stub = buyer_pb2_grpc.BuyerMasterStub(channel)
        response = await stub.GetBuyerHistory(buyer_pb2.GetBuyerHistoryRequest(buyer_id=buyer_request.get('buyer_id')))
    cart_items = response.items
    cart_list = []
    for item in cart_items:
        print("***", Timestamp().ToDatetime(item.updated_at))
        cart_list.append({'buyer_id':item.buyer_id, 'item_id':item.item_id, 
                          'quantity':item.quantity,'name': item.name, 'category': item.category, 
                          'condition': item.condition, 'keywords': list(item.keywords), 
                          'sale_price': item.sale_price, 'seller_id': item.seller_id, 
                          'seller_review': item.seller_review, 'updated_at': Timestamp().ToDatetime(item.updated_at).isoformat()})

    purchase_history_resp = {'items': cart_list}
    return web.Response(text=json.dumps(purchase_history_resp))


app = web.Application()
# app.router.add_get('/get_item', get_item_handler)
app.router.add_post('/add_to_cart', add_to_cart_handler)
app.router.add_post('/remove_item', remove_item_handler)
app.router.add_post('/clear_cart', clear_cart_handler)
app.router.add_post('/display_cart', display_cart_handler)
app.router.add_post('/create_account', create_account_handler)
app.router.add_post('/login', login_handler)
app.router.add_post('/logout', logout_handler)
app.router.add_post('/make_purchase', make_purchase_handler)
# app.router.add_post('/provide_feedback', provide_feedback_handler)
app.router.add_post('/get_seller_rating', get_seller_rating_handler)
app.router.add_post('/get_buyer_history', get_buyer_history_handler)

web.run_app(app)