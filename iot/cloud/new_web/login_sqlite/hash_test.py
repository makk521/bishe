from werkzeug.security import generate_password_hash, check_password_hash

password = "123456"

p_hash = generate_password_hash(password)
print(p_hash)

ret = check_password_hash(p_hash, password)
print(ret)