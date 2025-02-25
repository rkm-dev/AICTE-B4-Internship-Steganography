# Encryption Logic

def encypt(img, secret):
    d = {}  # to store dictionary of ascii characters with corresponding numerals
    c = {}  # to store dictionary of numbers with corresponding ascii character
    
    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)
    
    # image matrix values
    m = 0
    n = 0
    z = 0
    
    # inserting converted message ascii characters at the start of the matrix
    for i in range(len(secret)):
        img[n, m, z] = d[secret[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    
    return img # returing the updated image matrix