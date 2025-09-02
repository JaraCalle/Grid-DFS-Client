def split_file(file_path: str, block_size: int):
    with open(file_path, "rb") as f:
        i = 0
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            yield i, chunk
            i += 1
