from generate import generate_params
from params import generate_group
from ring import sign, verify


MEMBERS = ["Alice", "Bob", "Carol", "You"]


def print_signature(signature, members):
    print("  Signature (c_i, r_i) per member:")
    for i, (c_i, r_i) in enumerate(signature):
        print(f"    [{members[i]}]  c={c_i}  r={r_i}")


def main():
    print("=" * 60)
    print("       Ring Signature Demo — Non-Cyclic Version")
    print("=" * 60)

    # --- Setup ---
    params = generate_params(bits=512)
    p, q, g = params

    n = len(MEMBERS)
    private_keys, public_keys = generate_group(n, p, q, g)

    print("Group members:", ", ".join(MEMBERS))
    print("Public keys:")
    for i, name in enumerate(MEMBERS):
        print(f"  {name}: y = {str(public_keys[i])[:40]}...")
    print()

    # --- Demo 1: You sign a message ---
    message = "I vote YES"
    signer_index = 3  # "You"

    print(f"Message: '{message}'")
    print(f"Signer:  {MEMBERS[signer_index]} (index {signer_index})\n")

    signature = sign(message, signer_index, private_keys[signer_index], public_keys, params)
    print_signature(signature, MEMBERS)
    print()

    result = verify(message, signature, public_keys, params)
    print(f"Verification result: {'VALID' if result else 'INVALID'}")
    print()

    # --- Demo 2: Tamper with the signature ---
    print("-" * 60)
    print("Tamper test: flip c_0 by 1")
    c0, r0 = signature[0]
    tampered = [(c0 + 1, r0)] + list(signature[1:])
    tampered_result = verify(message, tampered, public_keys, params)
    print(f"Tampered verification: {'VALID' if tampered_result else 'INVALID'}")
    print()

    # --- Demo 3: Anonymity — Alice also signs the same message ---
    print("-" * 60)
    print("Anonymity demo: Alice signs the same message\n")

    alice_index = 0
    sig_alice = sign(message, alice_index, private_keys[alice_index], public_keys, params)
    sig_you   = sign(message, signer_index, private_keys[signer_index], public_keys, params)

    print("Alice's signature:")
    print_signature(sig_alice, MEMBERS)
    print()
    print("Your signature:")
    print_signature(sig_you, MEMBERS)
    print()

    print("Both valid?")
    print(f"  Alice's sig: {'VALID' if verify(message, sig_alice, public_keys, params) else 'INVALID'}")
    print(f"  Your sig:    {'VALID' if verify(message, sig_you,  public_keys, params) else 'INVALID'}")
    print()
    print("The verifier cannot tell which member signed — both signatures")
    print("are structurally identical. This is anonymity.")
    print("=" * 60)


if __name__ == "__main__":
    main()
