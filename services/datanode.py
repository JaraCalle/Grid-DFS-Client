import grpc
from modules.grpc.generated import datanode_pb2, datanode_pb2_grpc

def upload_block(datanode_host: str, datanode_port: int, block_id: str, data: bytes):
    channel = grpc.insecure_channel(f"{datanode_host}:{datanode_port}")
    stub = datanode_pb2_grpc.DataNodeServiceStub(channel)
    request = datanode_pb2.UploadBlockRequest(block_id=block_id, data=data) # type: ignore
    response = stub.UploadBlock(request)
    return response.message

def download_block(datanode_host: str, datanode_port: int, block_id: str):
    channel = grpc.insecure_channel(f"{datanode_host}:{datanode_port}")
    stub = datanode_pb2_grpc.DataNodeServiceStub(channel)
    request = datanode_pb2.DownloadBlockRequest(block_id=block_id) # type: ignore
    response = stub.DownloadBlock(request)
    return response.data
