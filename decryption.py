# Decryption Logic

def decrypt(img, msg_len):
    c = {}
    
    for i in range(255):
        c[i] = chr(i)  # to store dictionary of numbers with corresponding ascii character
    
    message = ""
    n = 0
    m = 0
    z = 0
    
    # extracting the stored message characters from the start of the image matrix 
    for i in range(msg_len):
        message = message + c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    
    return message  # returning the extracted message value