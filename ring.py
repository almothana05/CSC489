import random
from hash_utils import H


def sign(message, signer_index, private_key, public_keys, params):
    """
    Produce a ring signature.

    message       — string to sign
    signer_index  — position of the signer in public_keys list
    private_key   — signer's x
    public_keys   — list of all y_i (including signer's)
    params        — (p, q, g)

    Returns: list of (c_i, r_i) tuples, one per ring member
    """
    p, q, g = params
    n = len(public_keys)
    s = signer_index

    # Step 1 — random commitment for the signer
    u = random.randrange(1, q)
    L_s = pow(g, u, p)

    # Step 2 — simulate all non-signers
    c = [0] * n
    r = [0] * n
    L = [0] * n

    L[s] = L_s

    for i in range(n):
        if i == s:
            continue
        c[i] = random.randrange(1, q)
        r[i] = random.randrange(1, q)
        # L_i = g^(r_i) * y_i^(c_i) mod p
        L[i] = (pow(g, r[i], p) * pow(public_keys[i], c[i], p)) % p

    # Step 3 — compute signer's challenge
    h = H(message, L, q)
    sum_other_c = sum(c[i] for i in range(n) if i != s) % q
    c[s] = (h - sum_other_c) % q

    # Step 4 — compute signer's response
    r[s] = (u - c[s] * private_key) % q

    return list(zip(c, r))


def verify(message, signature, public_keys, params):
    """
    Verify a ring signature.

    message      — string that was signed
    signature    — list of (c_i, r_i) tuples
    public_keys  — list of all y_i
    params       — (p, q, g)

    Returns: True if valid, False otherwise
    """
    p, q, g = params
    n = len(public_keys)

    # Step 1 — recompute all L values
    L = []
    for i in range(n):
        c_i, r_i = signature[i]
        # L_i = g^(r_i) * y_i^(c_i) mod p
        L_i = (pow(g, r_i, p) * pow(public_keys[i], c_i, p)) % p
        L.append(L_i)

    # Step 2 — check the ring closes
    expected = H(message, L, q)
    actual = sum(c_i for c_i, _ in signature) % q

    return expected == actual
