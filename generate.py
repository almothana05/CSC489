import random


def is_prime(n, rounds=40):
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_safe_prime(bits=512):
    """
    Generate a safe prime p = 2q + 1 where both p and q are prime.
    q becomes the subgroup order used in Z_q arithmetic.
    """
    while True:
        # Generate a random prime q of (bits-1) size
        q = random.getrandbits(bits - 1)
        q |= (1 << (bits - 2))  # ensure high bit is set
        q |= 1                  # ensure odd

        if not is_prime(q):
            continue

        p = 2 * q + 1
        if is_prime(p):
            return p, q


def find_generator(p, q):
    """
    Find a generator g of the subgroup of order q in Z_p*.
    g must satisfy: g != 1 and g^q mod p == 1.
    """
    while True:
        h = random.randrange(2, p - 1)
        g = pow(h, 2, p)   # g = h^((p-1)/q) = h^2 since q = (p-1)/2
        if g != 1:
            return g


def generate_params(bits=512):
    """
    Generate and return group parameters (p, q, g).

    p  — safe prime
    q  — subgroup order (q = (p-1)/2)
    g  — generator of subgroup of order q in Z_p*
    """
    print(f"Generating {bits}-bit safe prime... (this may take a few seconds)")
    p, q = generate_safe_prime(bits)
    g = find_generator(p, q)
    print("Parameters generated.\n")
    return p, q, g
