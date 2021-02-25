import buyer_pb2_grpc, buyer_pb2
import grpc
import random
from config import DBConstants
from asyncpg.exceptions import UniqueViolationError
from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy import and_


class BuyerMasterServicer(buyer_pb2_grpc.BuyerMasterServicer):
    """Implements ItemMaster protobuf service interface."""
    def print_request(self, request, context):
        print("request :", end=" ")
        print((request, context, type(request)))
        print("-------------------")

    @staticmethod
    def generate_rand_id():
        return random.randint(1, pow(2, 63) - 1)

    @staticmethod
    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d

    async def SearchItemCart(self, request, context):
        """search items from the database.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyer_cart import BuyerCart
        from models.items import Items
        from database import db_product as db
        self.print_request(request, context)
        keywords = request.keywords
        item_dict = {}
        for keyword in keywords:
            items = await db.status(db.text
                                    ('select * from items where category = :category and :keyword = any(keywords)'),
                                    {'category': request.category, 'keyword': keyword})
            print(items)
            for item in items[1]:
                # id is at index 2
                new_item = (item[0], item[1], item[2], item[3], item[4], float(item[5]), item[6], item[7])
                print((type(item[0]), type(item[1]), type(item[2]), type(item[3]), type(item[4]), type(item[5]),
                       type(item[6]), type(item[7])))
                item_dict[item[2]] = new_item
        print(item_dict)
        if item_dict:
            search_resp = []
            for key in item_dict:
                item = item_dict[key]
                search_resp.append(buyer_pb2.Item(
                    name=item[0], category=item[1], id = item[2],
                    condition=item[3], keywords=item[4],
                    sale_price=item[5], seller_id=item[6],
                    quantity=item[7]))
            return buyer_pb2.SearchItemCartResponse(items=search_resp)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No items found for this query')
            return buyer_pb2.SearchItemCartResponse()

    async def AddToCart(self, request, context):
        """Add item to cart.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyer_cart import BuyerCart
        from models.items import Items
        self.print_request(request, context)
        item = await Items.query.where(Items.id == request.item_id).gino.first()
        print(item)
        if item is None or item.quantity < request.quantity:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            if item is None:
                context.set_details('Item does not exist')
            else:
                context.set_details('Not enough Item quantity present')
            return buyer_pb2.AddToCartResponse()
        
        buyer_cart_exist = await BuyerCart.query.where(and_(BuyerCart.item_id == request.item_id,
                                                            BuyerCart.buyer_id == request.buyer_id,
                                                            BuyerCart.checked_out == False)).gino.first()
        print(buyer_cart_exist)
        if buyer_cart_exist:
            add_q = buyer_cart_exist.quantity + request.quantity
            if add_q > item.quantity:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Not enough Item quantity present - already item in cart')
                return buyer_pb2.AddToCartResponse()

            buyer_cart = await buyer_cart_exist.update(quantity=add_q).apply()
        else:
            buyer_cart = await BuyerCart.create(buyer_id=request.buyer_id, 
                                                item_id=request.item_id, 
                                                quantity=request.quantity)
        print(buyer_cart)
        if buyer_cart:
            return buyer_pb2.AddToCartResponse(buyer_id=request.buyer_id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Add to cart unsuccessful')
            return buyer_pb2.AddToCartResponse()

    async def RemoveItemFromShoppingCart(self, request, context):
        """Remove item from buyer cart.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyer_cart import BuyerCart
        self.print_request(request, context)
        buyer_cart_exist = await BuyerCart.query.where(and_(BuyerCart.item_id == request.item_id,
                                                            BuyerCart.buyer_id == request.buyer_id,
                                                            BuyerCart.checked_out == False)).gino.first()
        if buyer_cart_exist:
            diff = buyer_cart_exist.quantity - request.quantity
            if buyer_cart_exist.quantity > request.quantity:
                await buyer_cart_exist.update(quantity=diff).apply()
            elif buyer_cart_exist.quantity == request.quantity:
                await buyer_cart_exist.delete()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Not enough Item present in buyer cart')
                return buyer_pb2.RemoveItemFromShoppingCartResponse()
            return buyer_pb2.RemoveItemFromShoppingCartResponse(buyer_id=request.buyer_id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item not present in buyer cart')
            return buyer_pb2.RemoveItemFromShoppingCartResponse()

    async def ClearCart(self, request, context):
        """Clear buyer cart.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyer_cart import BuyerCart
        self.print_request(request, context)
        try:
            await BuyerCart.delete.where(and_(BuyerCart.buyer_id == request.buyer_id,
                                              BuyerCart.checked_out == False)).gino.status()
            return buyer_pb2.ClearCartResponse(buyer_id=request.buyer_id)
        except Exception:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Buyer cart removal unsuccessful')
            return buyer_pb2.ClearCartResponse()

    async def DisplayCart(self, request, context):
        """Display items from cart.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyer_cart import BuyerCart
        from models.items import Items
        self.print_request(request, context)
        buyer_cart = await BuyerCart.query.where(and_(BuyerCart.buyer_id == request.buyer_id,
                                                      BuyerCart.checked_out == False)).gino.all()
        if buyer_cart:
            display_resp = []
            for cart_item in buyer_cart:
                ts = Timestamp()
                ts.FromDatetime(cart_item.updated_at)
                item = await Items.query.where(Items.id == cart_item.item_id).gino.first()
                display_resp.append(buyer_pb2.DisplayItemsInCart(
                    buyer_id=cart_item.buyer_id, item_id=cart_item.item_id, 
                    quantity=cart_item.quantity, name=item.name, category=item.category,
                    condition=item.condition, keywords=item.keywords,
                    sale_price=item.sale_price, seller_id=item.seller_id, 
                    updated_at=ts))
            return buyer_pb2.DisplayCartResponse(items=display_resp)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No cart items found for this buyer')
            return buyer_pb2.DisplayCartResponse()

    async def CreateAccount(self, request, context):
        """Create account.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyers import Buyers
        self.print_request(request, context)
        buyer_id = BuyerMasterServicer.generate_rand_id()
        try:
            buyer = await Buyers.create(id=buyer_id, name=request.name, 
                                         user_name=request.user_name, password=request.password)
            if buyer:
                return buyer_pb2.CreateAccountResponse(buyer_id=buyer_id)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Account creation unsuccessful')
                return buyer_pb2.CreateAccountResponse()
        except UniqueViolationError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Account creation unsuccessful - Buyer with same username exists')
            return buyer_pb2.CreateAccountResponse()

    async def Login(self, request, context):
        """Login with username.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyers import Buyers
        self.print_request(request, context)
        buyer = await Buyers.query.where(and_(Buyers.user_name == request.user_name,
                                              Buyers.password == request.password)).gino.first()
        if buyer:
            return buyer_pb2.LoginResponse(buyer_id=buyer.id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Buyer not found')
            return buyer_pb2.LoginResponse()

    async def MakePurchase(self, request, context):
        """Make purchase of all items in cart.
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyer_cart import BuyerCart
        from models.items import Items
        from models.sellers import Sellers

        # check from SOAP call that credit card payment is success
        # send name, number, exp

        self.print_request(request, context)
        buyer_cart = await BuyerCart.query.where(and_(BuyerCart.buyer_id == request.buyer_id,
                                                      BuyerCart.checked_out == True)).gino.all()
        if buyer_cart:
            # get item entry for each item in cart
            # check quantity, proceed only if enough quantity available in Item db
            # make sufficient item quantity as purchased
            # update seller num_items_sold count
            # remove insuffient items from cart
            for cart_item in buyer_cart:
                item = await Items.query.where(Items.id == cart_item.item_id).gino.first()
                seller = await Sellers.query.where(Sellers.id == item.seller_id).gino.first()
                if item and item.quantity >= cart_item.quantity:
                    diff = item.quantity - cart_item.quantity
                    await item.update(quantity=diff).apply()
                    await cart_item.update(checked_out=True).apply()
                    await seller.update(num_items_sold=seller.num_items_sold+cart_item.quantity).apply()
                else:
                    await cart_item.delete()

            return buyer_pb2.MakePurchaseResponse(buyer_id=request.buyer_id, transaction_status=True)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Cart is empty.')
            return buyer_pb2.MakePurchaseResponse()          

    async def ProvideFeedback(self, request, context):
        """Provide feedback for all checkout items
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyer_cart import BuyerCart, review_type
        from models.sellers import Sellers
        from models.items import Items
        from database import db_customer as db
        self.print_request(request, context)
        buyer_cart = await BuyerCart.query.where(and_(BuyerCart.item_id == request.item_id, 
                                                    BuyerCart.buyer_id == request.buyer_id,
                                                    BuyerCart.checked_out == True)).gino.first()

        #BuyerCart.seller_review == review_type.NA.name
        print(buyer_cart)
        if buyer_cart:
            item = await Items.query.where(Items.id == request.item_id).gino.first()
            if item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Feedback update failed - item not available')
                return buyer_pb2.ProvideFeedbackResponse()
            seller = await Sellers.query.where(Sellers.id == item.seller_id).gino.first()
            if seller is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Feedback update failed - seller not available')
                return buyer_pb2.ProvideFeedbackResponse()
            try:
                async with db.transaction():
                    if request.feedback == True:
                        await buyer_cart.update(seller_review=review_type.UP.name).apply()
                        await seller.update(feedback=(seller.feedback[0]+1, seller.feedback[1])).apply()
                    else:
                        await buyer_cart.update(seller_review=review_type.DOWN.name).apply()
                        await seller.update(feedback=(seller.feedback[0], seller.feedback[1]+1)).apply()
            except Exception:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Feedback update failed')
                return buyer_pb2.ProvideFeedbackResponse()
            return buyer_pb2.ProvideFeedbackResponse(buyer_id=request.buyer_id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No item in buyer cart')
            return buyer_pb2.ProvideFeedbackResponse()

    async def GetSellerRating(self, request, context):
        """Get seller rating
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.sellers import Sellers
        self.print_request(request, context)
        seller = await Sellers.query.where(Sellers.id == request.seller_id).gino.first()
        if seller:
            rating = seller.feedback[0] - seller.feedback[1]
            return buyer_pb2.GetSellerRatingResponse(rating=rating)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Seller rating not found')
            return buyer_pb2.GetSellerRatingResponse()

    async def GetBuyerHistory(self, request, context):
        """Get Buyer History
        Args:
            request: The request value for the RPC.
            context (grpc.ServicerContext)
        """
        from models.buyer_cart import BuyerCart
        from models.items import Items
        self.print_request(request, context)
        buyer_cart = await BuyerCart.query.where(and_(BuyerCart.buyer_id == request.buyer_id,
                                                      BuyerCart.checked_out == True)).gino.all()
        if buyer_cart:
            display_resp = []
            for cart_item in buyer_cart:
                ts = Timestamp()
                ts.FromDatetime(cart_item.updated_at)
                item = await Items.query.where(Items.id == cart_item.item_id).gino.first()
                display_resp.append(buyer_pb2.PurchaseHistory(
                    buyer_id=cart_item.buyer_id, item_id=cart_item.item_id, 
                    quantity=cart_item.quantity, name=item.name, category=item.category,
                    condition=item.condition, keywords=item.keywords,
                    sale_price=item.sale_price, seller_id=item.seller_id, 
                    seller_review=cart_item.seller_review.name, updated_at=ts))
            return buyer_pb2.GetBuyerHistoryResponse(items=display_resp)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Buyer history is empty')
            return buyer_pb2.GetBuyerHistoryResponse()



