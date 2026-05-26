"""
auth.py - Authentication controller wrapping database.py queries and password hash validation.
"""

from database import hash_password, get_user, create_user

def authenticate_user(username: str, password_raw: str) -> dict:
    """
    Checks credentials. 
    Returns user details (dict) if valid, otherwise None.
    """
    user = get_user(username)
    if user:
        input_hash = hash_password(password_raw)
        if user["password_hash"] == input_hash:
            return user
    return None

def register_new_user(username: str, password_raw: str, role: str = "student") -> bool:
    """
    Registers a new user in the platform database.
    """
    if not username.strip() or not password_raw.strip():
        return False
    # Validate username length
    if len(username.strip()) < 3 or len(password_raw.strip()) < 6:
        return False
        
    pw_hash = hash_password(password_raw.strip())
    return create_user(username.strip(), pw_hash, role)
