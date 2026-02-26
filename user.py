def is_palindrome(text):
    normalized_text = "".join(char.lower() for char in text if char.isalnum())
    return normalized_text == normalized_text[::-1]

user_input = input("Enter a string: ")

if is_palindrome(user_input):
    print(f"'{user_input}' is a palindrome.")
else:
    print(f"'{user_input}' is not a palindrome.")