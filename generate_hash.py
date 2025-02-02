from werkzeug.security import generate_password_hash

# Input the password you want to hash
password = 'your_password_here'

# Generate the hashed password
hashed_password = generate_password_hash(password)

# Print the hashed password
print("Hashed password:", hashed_password)
