import hashlib


def H(message, L_list, q):
    """
    Hash function that outputs a number in Z_q.

    Concatenates message and all L values into one string,
    SHA256 hashes it, then reduces mod q.
    """
    data = message + "".join(str(L) for L in L_list)
    digest = hashlib.sha256(data.encode()).hexdigest()
    return int(digest, 16) % q
