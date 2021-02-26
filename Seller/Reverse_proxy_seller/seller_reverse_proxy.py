"""The Python AsyncIO implementation of the GRPC helloworld.Greeter client."""
import grpc

import items_pb2
import items_pb2_grpc
from aiohttp import web
import json
from config import grpc_server
grpc_server_port = grpc_server.host_and_port


def parse_params(request):
    query_string = request.query_string
    params = query_string.split('&')
    return params


async def get_item_handler(request):
    params = parse_params(request)
    id = int(params[0].split('=')[1])
    async with grpc.aio.insecure_channel(grpc_server_port) as channel:
        stub = items_pb2_grpc.ItemMasterStub(channel)
        response = await stub.GetItem(items_pb2.GetItemRequest(id=id))
    item = response.item
    dict_resp = {'name': item.name, 'category': item.category, 'condition': item.condition,
                 'keywords': list(item.keywords), 'sale_price': item.sale_price, 'quantity': item.quantity,
                 'seller_id': item.seller_id}
    print(dict_resp)
    return web.Response(text=json.dumps(dict_resp))

async def add_item_handler(request):
    item = json.loads(await request.text())
    async with grpc.aio.insecure_channel(grpc_server_port) as channel:
        stub = items_pb2_grpc.ItemMasterStub(channel)
        item_obj = items_pb2.Item(name=item.get('name'), category=item.get('category'),
                                  condition=item.get('condition'),
                                  keywords=item.get('keywords'),
                                  sale_price=item.get('sale_price'),
                                  quantity=item.get('quantity'),
                                  seller_id=item.get('seller_id'))
        response = await stub.AddItem(items_pb2.AddItemRequest(item=item_obj))
    add_item_resp = {'item_id': response.id}
    return web.Response(text=json.dumps(add_item_resp))


async def change_item_handler(request):
    item = json.loads(await request.text())
    async with grpc.aio.insecure_channel(grpc_server_port) as channel:
        stub = items_pb2_grpc.ItemMasterStub(channel)
        response = await stub.ChangeItem(items_pb2.ChangeItemRequest(id=item.get('item_id'),
                                                                     seller_id=item.get('seller_id'),
                                                                     sale_price=item.get('sale_price')))
    change_item_resp = {'item_id': response.id}
    return web.Response(text=json.dumps(change_item_resp))


async def display_item_handler(request):
    item = json.loads(await request.text())
    async with grpc.aio.insecure_channel(grpc_server_port) as channel:
        stub = items_pb2_grpc.ItemMasterStub(channel)
        response = await stub.DisplayItem(items_pb2.DisplayItemRequest(seller_id=item.get('seller_id')))

    items = response.items
    item_list = []
    for item in items:
        item_list.append({'name': item.name, 'category': item.category, 'id': item.id, 'condition': item.condition,
                         'keywords': list(item.keywords), 'sale_price': item.sale_price, 'quantity': item.quantity,
                         'seller_id': item.seller_id})

    display_item_resp = {'items': item_list}
    return web.Response(text=json.dumps(display_item_resp))


async def remove_item_handler(request):
    item = json.loads(await request.text())
    async with grpc.aio.insecure_channel(grpc_server_port) as channel:
        stub = items_pb2_grpc.ItemMasterStub(channel)
        response = await stub.RemoveItem(items_pb2.RemoveItemRequest(id=item.get('item_id'),
                                                                     seller_id=item.get('seller_id'),
                                                                     quantity=item.get('quantity')))
    remove_item_resp = {'item_id': response.id}
    return web.Response(text=json.dumps(remove_item_resp))

async def create_account_handler(request):
    item = json.loads(await request.text())
    async with grpc.aio.insecure_channel(grpc_server_port) as channel:
        stub = items_pb2_grpc.ItemMasterStub(channel)
        response = await stub.CreateAccount(items_pb2.CreateAccountRequest(name=item.get('name'),
                                                                           user_name=item.get('user_name'),
                                                                           password=item.get('password')))
    create_account_response = {'seller_id': response.seller_id}

    return web.Response(text=json.dumps(create_account_response))


async def login_handler(request):
    item = json.loads(await request.text())
    async with grpc.aio.insecure_channel(grpc_server_port) as channel:
        stub = items_pb2_grpc.ItemMasterStub(channel)
        response = await stub.Login(items_pb2.LoginRequest(user_name=item.get('user_name'),
                                                           password=item.get('password')))
    login_response = {'seller_id': response.seller_id}

    return web.Response(text=json.dumps(login_response))


async def logout_handler(request):
    logout_response = {'seller_id': 0}
    return web.Response(text=json.dumps(logout_response))


async def get_seller_rating_handler(request):
    item = json.loads(await request.text())
    async with grpc.aio.insecure_channel(grpc_server_port) as channel:
        stub = items_pb2_grpc.ItemMasterStub(channel)
        response = await stub.GetSellerRating(items_pb2.GetSellerRatingRequest(seller_id=item.get('seller_id')))
    get_seller_rating_response = {'rating': response.rating}

    return web.Response(text=json.dumps(get_seller_rating_response))


app = web.Application()
app.router.add_get('/get_item', get_item_handler)
app.router.add_post('/add_item', add_item_handler)
app.router.add_post('/change_item', change_item_handler)
app.router.add_post('/display_item', display_item_handler)
app.router.add_post('/remove_item', remove_item_handler)
app.router.add_post('/create_account', create_account_handler)
app.router.add_post('/login', login_handler)
app.router.add_post('/logout', logout_handler)
app.router.add_post('/get_seller_rating', get_seller_rating_handler)

web.run_app(app)