import random
from generate import generate_params


def generate_keypair(p, q, g):
    """
    Generate a keypair for one ring member.

    private key x  — random integer in {1, ..., q-1}
    public key  y  — g^x mod p
    """
    x = random.randrange(1, q)
    y = pow(g, x, p)
    return x, y


def generate_group(n, p, q, g):
    """
    Generate keypairs for a group of n members.
    Returns two lists: private_keys, public_keys
    """
    private_keys = []
    public_keys = []
    for _ in range(n):
        x, y = generate_keypair(p, q, g)
        private_keys.append(x)
        public_keys.append(y)
    return private_keys, public_keys
