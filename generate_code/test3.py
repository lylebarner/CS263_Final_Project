def copy_bytes(dest: bytearray, src: bytearray, num_bytes: int) -> None:
    """
    Copies num_bytes from src to dest. Both dest and src must be bytearrays.
    Assumes the destination buffer is large enough (at least 256 bytes).
    """
    if num_bytes < 0:
        raise ValueError("num_bytes must be non-negative")
    if num_bytes > len(src):
        raise ValueError("Source does not have enough bytes to copy")
    if num_bytes > len(dest):
        raise ValueError("Destination buffer is too small")

    for i in range(num_bytes):
        dest[i] = src[i]

# Example usage
buffer = bytearray(256)  # destination
message = bytearray(b"Hello, world!")  # source
copy_bytes(buffer, message, len(message))

print(buffer[:len(message)])
