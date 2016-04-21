from random import SystemRandom

def generateKey(key_length):
    "Generates a random key of given length"
    key = ""
    character = SystemRandom()
    for i in range(key_length):
        #Key is a string, so adds a character in a string
        #Split turns '0xa' to 'a'
        key = key + hex(character.randrange(16)).split('x')[1]
    return key

def encrypt(message, key):
    "Encrypts a given message by adding given key to the message character by character"
    if len(message) > len(key):
        print "ERROR"
        print "Key too short."
        return -1
    messageList = list(message)
    keyList = list(key)
    #An array for crypted message
    cryptedList = []
    for i in range(len(message)):
        #Makes sure the ASCII character is printable
        #After 126 comes 32
        temp = 32 + (ord(messageList[i]) + int(keyList[i], 16) - 32) % 94
        cryptedList.append(chr(temp))
    return ''.join(cryptedList)

def decrypt(crypted_msg, key):

    if len(crypted_msg) > len(key):
        print "ERROR"
        print "Key too short."
        return -1
    cryptedList = list(crypted_msg)
    keyList = list(key)
    #An array for clear text message
    messageList = []
    for i in range(len(crypted_msg)):
        #Makes sure the ASCII character is printable
        #After 126 comes 32
        temp = 32 + (ord(cryptedList[i]) - int(keyList[i], 16) - 32) % 94
        messageList.append(chr(temp))
    return ''.join(messageList)

if __name__ == "__main__":
    key = generateKey(64)
    print key
    crypted_msg = encrypt("Hello world!", key)
    print crypted_msg
    message = decrypt(crypted_msg, key)
    print message
