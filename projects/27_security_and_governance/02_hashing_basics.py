from passlib.context import CryptContext

# Creating a context utilizing the strongly uncrackable bcrypt hashing algorithm
pwd_context =CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the provided string matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a bcrypt hash from a plaintext string."""
    return pwd_context.hash(password)

if __name__ == "__main__":
    print("--- Demonstrating Encryption at Rest ---")
    
    plaintext_secret = "MySuperSecretPassword#123"
    print(f"Plaintext: {plaintext_secret}")
    
    # 1. Hash the password (simulating user registration)
    secure_hash = get_password_hash(plaintext_secret)
    print(f"Stored Hash (what goes in the DB): {secure_hash}")
    
    # 2. Verify login attempt (simulating user login)
    print(f"Login Attempt with correct password matches? {verify_password(plaintext_secret, secure_hash)}")
    print(f"Login Attempt with WRONG password matches? {verify_password('wrong_password', secure_hash)}")
