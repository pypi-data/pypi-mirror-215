import random
import json
import pkg_resources

class RandomData:
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, user_agent, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.user_agent = user_agent
        self.email = email

def get_random_data():
    data_dir = pkg_resources.resource_filename('mypiprandomdata', 'data')

    with open(data_dir + '/data.json', 'r') as file:
        data = json.load(file)

    random_generator = random.randint(0, len(data) - 1)
    addresses = data[random_generator]['addresses']

    random_generator2 = random.randint(0, len(addresses) - 1)

    random_data = {
        "address": addresses[random_generator2]['street'],
        "city": addresses[random_generator2]['city'],
        "state": addresses[random_generator2]['state'],
        "zip_code": addresses[random_generator2]['zipcode'],
        "phone_number": addresses[random_generator2]['phone_number']
    }

    first_name = get_random_name_from_file(data_dir, 'FirstName.txt', split_by=',')
    last_name = get_random_name_from_file(data_dir, 'LastName.txt', split_by=',')
    user_agent = get_random_name_from_file(data_dir, 'UserAgent.txt', split_by='\n')
    email = f"{first_name.lower()}{last_name.lower()}{random.randint(999, 9999)}{random.choice(['@gmail.com', '@yahoo.com'])}"

    random_data = RandomData(first_name, last_name, random_data['address'], random_data['city'],
                             random_data['state'], random_data['zip_code'], random_data['phone_number'], user_agent, email)

    return random_data

def get_random_name_from_file(directory, filename, split_by=None):
    file_path = directory + '/' + filename
    with open(file_path, 'r') as file:
        names = file.read().strip().split(split_by) if split_by else file.readlines()
    return random.choice(names).strip().strip('",')

def main():
    random_data = get_random_data()
    print("Randomly Generated Data:")
    print("First Name:", random_data.first_name)
    print("Last Name:", random_data.last_name)
    print("Email:", random_data.email)
    print("Address:", random_data.address)
    print("City:", random_data.city)
    print("State:", random_data.state)
    print("Zip Code:", random_data.zip_code)
    print("Phone Number:", random_data.phone_number)
    print("User Agent:", random_data.user_agent)

if __name__ == '__main__':
    main()
