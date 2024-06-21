import random
import string
import requests
from faker import Faker

fake = Faker()

def random_string(length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_user_profiles(n=200):
    for _ in range(n):
        username = random_string()
        first_name = fake.first_name()
        last_name = fake.last_name()
        password = fake.password()
        email = fake.email()

        data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "email": email
        }

        response = requests.post('http://localhost:8000/users/infos/users/', json=data)

        if response.status_code != 201:
            print(f"Failed to create user: {response.text}")

if __name__ == "__main__":
    create_user_profiles()