def is_palindrome(s):
    """Checks if a given string is a palindrome."""
    # A string is a palindrome if it reads the same forwards and backwards.
    # This solution directly compares the string with its reverse.
    return s == s[::-1]

# Example Usage:
# print(is_palindrome("madam"))    # True
# print(is_palindrome("racecar"))  # True
# print(is_palindrome("hello"))    # False
# print(is_palindrome(""))        # True (empty string is a palindrome)