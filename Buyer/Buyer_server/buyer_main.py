import logging
import asyncio
import grpc
import buyer_pb2_grpc
import database
from database.buyer_master import BuyerMasterServicer


async def serve() -> None:
    server = grpc.aio.server()
    await database.connect_db()
    buyer_master_servicer = BuyerMasterServicer()
    buyer_pb2_grpc.add_BuyerMasterServicer_to_server(servicer=buyer_master_servicer, server=server)
    listen_addr = '127.0.0.1:5001'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())