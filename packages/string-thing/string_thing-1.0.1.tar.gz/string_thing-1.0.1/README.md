# StringThing

StringThing is a lightweight library for encoding and decoding strings using various patterns.

## Installation

StringThing has no external dependencies, so it can be installed from source or directly from PyPI:

```sh
pip install string-thing
```

## Usage

StringThing provides an API for encoding and decoding strings. To use it, import the StringThing class and create a new instance with an array of patterns in the order you want to use them:

```python
from string_thing import StringThing

my_string = 'This is my string'

# Create a new instance of StringThing with default pattern (['split-halves', 'reverse', 'shift', 'swap-case', 'rotate'])
my_string_thing = StringThing()

# Encode the string
encoded = my_string_thing.encode(myString)

# Output the encoded string
print(encoded) # "ZN!TJ!TJIuHOJSUT!"

# Decode the string
decoded = my_string_thing.decode(encoded)

# Output the decoded string
print(decoded) # "This is my string"
```

## Patterns

StringThing patterns currently support the following operations:

- `split-halves`: Splits the string into two halves and swaps them.
	- `Abcd12` => `d12Abc`
- `reverse`: Reverses the order of the characters in the string.
	- `Abcd12` => `21dcbA`
- `shift`: Shifts the characters in the string up by 1 in the ASCII table.
	- `Abcd12` => `Bcde23`
- `swap-case`: Swaps uppercase & lowercase characters in the string.
	- `Abcd12` => `aBCD12`
- `rotate`:  Shifts the string 1 position to the right.
	- `Abcd12` => `2Abcd1`

To use a specific pattern, pass it as an argument to the StringThing constructor:

```python
from string_thing import StringThing

my_string_thing_1 = StringThing(['split-halves', 'shift', 'reverse', 'shift', 'swap-case', 'rotate'])

# OR

string_thing_pattern = ['split-halves', 'shift', 'reverse', 'shift', 'swap-case', 'rotate']
my_string_thing_2 = StringThing(string_thing_pattern)
```

## Example: Encoding Passwords for Secure Storage

StringThing can be used to encode passwords before hashing them and storing them in a database, making it more difficult for an attacker to retrieve the original password even if they gain access to the database.

Here's an example of how to use StringThing to encode a password before hashing it with bcrypt when working with passwords in a database:

#### Create User:

```python
import bcrypt
from string_thing import StringThing

string_thing_pattern = ['split-halves', 'shift', 'reverse', 'shift', 'swap-case', 'rotate']

# Generate a salt for the bcrypt hash
salt = bcrypt.gensalt()

# The original password to be encoded and hashed
password = 'myPassword123'

# Encode the password using StringThing
encoded_password = StringThing(string_thing_pattern).encode(password)

# Hash the encoded password with bcrypt
hashed_password = bcrypt.hashpw(encoded_password, salt)

# Add the hashed password to a user object for storage in a database
user = {
  'username': 'johndoe',
  'email': 'johndoe@example.com',
  'password': hashed_password,
  # other user data...
}

# Add the user object to the database
my_database.add_user(user)
```

#### Authenticate User:

```python
import bcrypt
from string_thing import StringThing

string_thing_pattern = ['split-halves', 'shift', 'reverse', 'shift', 'swap-case', 'rotate']

# Retrieve the user's hashed password from the database
user = my_database.get_user_by_username('johndoe')
hashed_password = user.password

# The password entered by the user attempting to log in
password_attempt = 'myPassword123'

# Encode the password attempt using StringThing
encoded_password_attempt = StringThing(string_thing_pattern).encode(password_attempt)

# Compare the encoded password attempt to the stored hashed password
if bcrypt.checkpw(encoded_password_attempt, hashed_password):
  # Passwords match - login successful!
else:
  # Passwords do not match - login failed
```
