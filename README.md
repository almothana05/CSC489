# Ring Signature — Anonymous Group Proof

A Python implementation of a **non-cyclic ring signature scheme** based on the Schnorr protocol. It allows any member of a group to sign a message on behalf of the group, proving that *someone* in the group signed — without revealing *who*.

---

## What is a Ring Signature?

A ring signature is a cryptographic primitive where:
- A signer proves they belong to a group of N members
- The verifier is convinced someone in the group signed
- The verifier **cannot determine which member** signed
- Other group members **do not need to participate or even know**

This is the mechanism behind anonymous voting, whistleblowing systems, and privacy coins like Monero.

---

## How It Works

### Setup
Each member independently generates a keypair:
```
private key:  x  ∈ Z_q       (random, kept secret)
public key:   y  = g^x mod p  (shared openly)
```

Group parameters `(p, q, g)` are public: `p` is a safe prime, `q = (p-1)/2`, and `g` is a generator of the subgroup of order `q`.

### Signing
The signer at index `s` with private key `x_s`:

1. Pick random `u`, compute `L_s = g^u mod p`
2. For every non-signer `i`: pick random `c_i, r_i`, compute `L_i = g^(r_i) · y_i^(c_i) mod p`
3. Compute signer's challenge: `c_s = H(m, L_0..L_n) - Σ c_i  mod q`
4. Compute signer's response: `r_s = u - c_s · x_s  mod q`
5. Output: `{ (c_i, r_i) for all i }`

### Verification
Given the signature and all public keys:

1. Recompute: `L_i = g^(r_i) · y_i^(c_i) mod p` for all `i`
2. Check: `H(m, L_0..L_n) == Σ c_i  mod q`

If equal → valid. The ring closes only if one member used their private key to construct it.

### Why It Is Anonymous
All `L_i` values — both simulated (non-signers) and real (signer) — are computationally indistinguishable from random. The verifier sees only that the sum constraint holds, which is symmetric across all members.

---

## Project Structure

```
ring_signature/
├── generate.py     — safe prime generation (Miller-Rabin) and generator finding
├── params.py       — keypair and group generation
├── hash_utils.py   — hash function H: outputs integer in Z_q
├── ring.py         — sign() and verify()
└── main.py         — demo
```

---

## Setup

No external libraries required. Uses Python's standard library only.

**Requirements:**
- Python 3.7+

**Install:**
```bash
git clone <repo>
cd ring_signature
```

---

## Usage

### Run the demo
```bash
python3 main.py
```

The demo will:
1. Generate a 512-bit safe prime (takes a few seconds)
2. Create a group of 4 members: Alice, Bob, Carol, You
3. Sign a message as `You`
4. Verify the signature → VALID
5. Tamper with the signature → INVALID
6. Show Alice signing the same message → both valid and indistinguishable

### Use the API directly

```python
from generate import generate_params
from params import generate_group
from ring import sign, verify

# Generate parameters
params = generate_params(bits=512)
p, q, g = params

# Create a group of 4 members
private_keys, public_keys = generate_group(4, p, q, g)

# Member at index 2 signs a message
message = "hello world"
signer_index = 2

signature = sign(message, signer_index, private_keys[signer_index], public_keys, params)

# Anyone can verify
is_valid = verify(message, signature, public_keys, params)
print(is_valid)  # True
```

---

## Security Notes

- **Bit size:** Default is 512-bit for demo speed. Use 2048-bit for real security.
- **No linkability:** This implementation does not include key images, so the same member can sign multiple messages without being linked. Add key images (as in Monero's LSAG) for linkability.
- **No trusted setup:** Group members never share private keys or interact during signing.
- **Non-signer consent:** A member can be added to a ring using only their public key — no consent or interaction required.

---

## Example Output

```
============================================================
       Ring Signature Demo — Non-Cyclic Version
============================================================
Generating 512-bit safe prime... (this may take a few seconds)
Parameters generated.

Group members: Alice, Bob, Carol, You
Message: 'I vote YES'
Signer:  You (index 3)

Verification result: VALID

Tamper test: flip c_0 by 1
Tampered verification: INVALID

Anonymity demo: Alice signs the same message
  Alice's sig: VALID
  Your sig:    VALID

The verifier cannot tell which member signed — both signatures
are structurally identical. This is anonymity.
============================================================
```

---

## References

- Rivest, R., Shamir, A., Tauman, Y. (2001). *How to Leak a Secret.* ASIACRYPT 2001.
- Schnorr, C. P. (1991). *Efficient Signature Generation by Smart Cards.* Journal of Cryptology.
- Noether, S. (2015). *Ring Signature Confidential Transactions for Monero.* IACR ePrint.
