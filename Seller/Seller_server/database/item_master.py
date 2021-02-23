import items_pb2_grpc, items_pb2
import grpc
import random
from config import DBConstants
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import and_


class ItemMasterServicer(items_pb2_grpc.ItemMasterServicer):
    """Implements ItemMaster protobuf service interface."""
    def print_request(self, request, context):
        print("request :", end=" ")
        print((request, context, type(request)))
        print("-------------------")

    @staticmethod
    def generate_rand_id():
        return random.randint(1, pow(2, 63) - 1)

    async def GetItem(self, request, context):
        """Retrieve a item from the database.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        # item = db.query(models.Item).get(request.id)
        self.print_request(request, context)

        from database import db_product
        item = await db_product.status(db_product.text('select * from items'))
        print(item)
        item = item[1][0]
        if item:
            item_pb = items_pb2.Item(name=item[0], category=item[1], id=item[2], condition=item[3],
                                     keywords=item[4], sale_price=item[5], quantity=item[6], seller_id=item[7])
            return items_pb2.GetItemResponse(item=item_pb)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item with id %s not found' % request.id)
            return items_pb2.GetItemResponse()

    async def AddItem(self, request, context):
        """Add an item to the database.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.items import Items
        self.print_request(request, context)
        item_id = ItemMasterServicer.generate_rand_id()
        item = await Items.create(id=item_id, name=request.item.name, category=request.item.category,
                                  condition=request.item.condition, keywords=request.item.keywords,
                                  sale_price=request.item.sale_price, quantity=request.item.quantity,
                                  seller_id=request.item.seller_id)
        print(item)
        if item:
            return items_pb2.AddItemResponse(id=item_id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item addition unsuccessful')
            return items_pb2.AddItemResponse()

    async def ChangeItem(self, request, context):
        """Change item sale price
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.items import Items
        self.print_request(request, context)
        change_val = await Items.update.values(sale_price=request.sale_price).where(and_(Items.id == request.id,
                                                                       Items.seller_id == request.seller_id)).\
            gino.status()
        if change_val[0] == DBConstants.Successful_update:
            return items_pb2.ChangeItemResponse(id=request.id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item sale price modification unsuccessful')
            return items_pb2.ChangeItemResponse()

    async def DisplayItem(self, request, context):
        """Display items from the database.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.items import Items
        self.print_request(request, context)
        items = await Items.query.where(Items.seller_id == request.seller_id).gino.all()
        if items:
            display_resp = []
            for item in items:
                display_resp.append(items_pb2.DisplayItem(name=item.name, category=item.category, id=item.id,
                                                          condition=item.condition, keywords=item.keywords,
                                                          sale_price=item.sale_price, quantity=item.quantity,
                                                          seller_id=item.seller_id))
            return items_pb2.DisplayItemResponse(items=display_resp)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No items found for this seller')
            return items_pb2.DisplayItemResponse()

    async def RemoveItem(self, request, context):
        """Remove item quantity
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.items import Items
        self.print_request(request, context)
        try:
            item = await Items.query.where(and_(Items.id == request.id,
                                                Items.seller_id == request.seller_id)).gino.first()
            diff = item.quantity - request.quantity
            if diff > 0:
                await item.update(quantity=diff).apply()
            elif diff == 0:
                await item.delete()
            return items_pb2.RemoveItemResponse(id=request.id)

        except Exception:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item quantity removal unsuccessful')
            return items_pb2.RemoveItemResponse()

    async def CreateAccount(self, request, context):
        """Remove item quantity
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.sellers import Sellers
        self.print_request(request, context)
        seller_id = ItemMasterServicer.generate_rand_id()
        try:
            seller = await Sellers.create(id=seller_id, name=request.name, user_name=request.user_name,
                                          password=request.password)
            if seller:
                return items_pb2.CreateAccountResponse(seller_id=seller_id)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Account creation unsuccessful')
                return items_pb2.CreateAccountResponse()
        except UniqueViolationError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Account creation unsuccessful - Seller with same username exists')
            return items_pb2.CreateAccountResponse()

    async def Login(self, request, context):
        """Remove item quantity
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.sellers import Sellers
        self.print_request(request, context)
        seller = await Sellers.query.where(and_(Sellers.user_name == request.user_name,
                                                Sellers.password == request.password)).gino.first()
        if seller:
            return items_pb2.LoginResponse(seller_id=seller.id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Seller not found')
            return items_pb2.LoginResponse()

    async def GetSellerRating(self, request, context):
        """Remove item quantity
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.sellers import Sellers
        self.print_request(request, context)
        seller = await Sellers.query.where(Sellers.id == request.seller_id).gino.first()
        if seller:
            rating = seller.feedback[0] - seller.feedback[1]
            return items_pb2.GetSellerRatingResponse(rating=rating)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Seller rating not found')
            return items_pb2.GetSellerRatingResponse()



