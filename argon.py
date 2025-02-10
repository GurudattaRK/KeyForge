import argon2

# Create a password hasher
ph = argon2.PasswordHasher(type=argon2.low_level.Type.I)
# Hashing a password
password = input("Enter string:")
ph = argon2.PasswordHasher(
    time_cost=5,        # Number of iterations
    memory_cost=65536,  # Memory usage in KB
    parallelism=1,      # Number of threads
    hash_len=32,        # Length of the hash
    salt_len=10        # Length of the salt
)
hash = ph.hash(password)




def decode_argon2_hash(hash_value):
    # Argon2 hash format: $argon2<type>$v=<version>$m=<memory>,t=<iterations>,p=<parallelism>$<salt>$<hash>
    parts = hash_value.split('$')
    
    print("\nHash Breakdown:")
    print("1. Hash Type:      ", parts[1])
    print("2. Version:        ", parts[2])
    print("3. Parameters:")
    
    # Parse parameters
    params = parts[3].split(',')
    for param in params:
        print(f"   - {param}")
    
    print("4. Salt:           ", parts[4])
    print("5. Derived Key:    ", parts[5])
    
    # Additional info
    print("\nHash Length:       ", len(parts[5]), "characters")
    print("Salt Length:       ", len(parts[4]), "characters")

print(decode_argon2_hash(hash))
