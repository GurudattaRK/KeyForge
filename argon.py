from argon2 import low_level, Type
import time
import base64

# Fixed salt (16 bytes)
FIXED_SALT = b'salt1234salt1234'

def hash_password(password, time_cost, memory_cost, parallelism, hash_length):
    """
        password: The password to hash
        time_cost: Number of iterations
        memory_cost: Memory usage in KiB
        parallelism: Number of parallel threads
        hash_length: Desired length of the hash in bytes
    """
    password_bytes = password.encode('utf-8')
    
    # Generate the hash using low-level function to specify fixed salt
    hash_bytes = low_level.hash_secret(
        secret=password_bytes,
        salt=FIXED_SALT,
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=hash_length,
        type=Type.I,  # Argon2i (data-independent)
        version=19    # Latest Argon2 version
    )
    
    # Decode the full hash string
    hash_str = hash_bytes.decode('utf-8')
    
    # Extract the base64 hash value (last part after $)
    base64_hash = hash_str.split('$')[-1]
    
    # Add padding if necessary
    # Base64 strings should have a length that's a multiple of 4
    missing_padding = len(base64_hash) % 4
    if missing_padding:
        base64_hash += '=' * (4 - missing_padding)
    
    # Convert base64 to bytes, then to hex
    # Use urlsafe_b64decode since Argon2 uses URL-safe base64
    hash_bytes = base64.urlsafe_b64decode(base64_hash)
    hex_hash = hash_bytes.hex()
    
    return hash_str, hex_hash

key = "bruh"
start_time = time.time()
example1_full, example1_hash = hash_password(key, 10, 1048576, 1, 16)
end_time = time.time()
elapsed_time1 = end_time - start_time

start_time = time.time()
example2_full, example2_hash = hash_password(key, 10, 1048576, 1, 32)
end_time = time.time()
elapsed_time2 = end_time - start_time

start_time = time.time()
example3_full, example3_hash = hash_password(key, 10, 1048576, 1, 64)
end_time = time.time()
elapsed_time3 = end_time - start_time

start_time = time.time()
example4_full, example4_hash = hash_password(key, 10, 1048576, 1, 128)
end_time = time.time()
elapsed_time4 = end_time - start_time

print("16 bytes:")
print("Full Hash:", example1_full)
print("Hex Hash:", example1_hash)
print(f"Time: {elapsed_time1} seconds")

print("\n32 bytes::")
print("Full Hash:", example2_full)
print("Hex Hash:", example2_hash)
print(f"Time: {elapsed_time2} seconds")

print("\n64 bytes:")
print("Full Hash:", example3_full)
print("Hex Hash:", example3_hash)
print(f"Time: {elapsed_time3} seconds")

print("\n128 bytes:")
print("Full Hash:", example4_full)
print("Hex Hash:", example4_hash)
print(f"Time: {elapsed_time4} seconds")