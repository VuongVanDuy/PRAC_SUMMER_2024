import secrets

def generate_secure_token(length=64):
    """Tạo một token an toàn với độ dài xác định."""
    return secrets.token_hex(length)

print(generate_secure_token())