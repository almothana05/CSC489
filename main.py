from params import load_or_generate_group
from ring import sign, verify


MEMBERS = ["Almothana", "Abdullah", "Esam", "You"]


def short(n):
    s = str(n)
    return s[:10] + "..." + s[-6:]


def print_signature(signature, members):
    for i, (c_i, r_i) in enumerate(signature):
        print(f"  {members[i]:12}  c={short(c_i)}  r={short(r_i)}")


def main():

    n = len(MEMBERS)
    params, private_keys, public_keys = load_or_generate_group(n, bits=512)
    p, q, g = params

    print("Group:", ", ".join(MEMBERS))
    print()

    # --- Demo 1: You sign a message ---
    message = "I like anonimity"
    signer_index = 3  # "You"

    print(f"Message : '{message}'")
    print(f"Signer  : {MEMBERS[signer_index]}\n")

    signature = sign(message, signer_index, private_keys[signer_index], public_keys, params)
    print("Signature:")
    print_signature(signature, MEMBERS)

    result = verify(message, signature, public_keys, params)
    print(f"\nVerification : {'VALID' if result else 'INVALID'}")

    # --- Tamper test ---
    c0, r0 = signature[0]
    tampered = [(c0 + 1, r0)] + list(signature[1:])
    tampered_result = verify(message, tampered, public_keys, params)
    print(f"Tamper test  : {'VALID' if tampered_result else 'INVALID'}  (flipped c_0 by 1)")

    # --- Anonymity demo ---
    sig_a1 = sign(message, 0, private_keys[0], public_keys, params)
    sig_a2 = sign(message, 0, private_keys[0], public_keys, params)
    sig_y1 = sign(message, signer_index, private_keys[signer_index], public_keys, params)
    sig_y2 = sign(message, signer_index, private_keys[signer_index], public_keys, params)

    cases = [
        (f"{MEMBERS[0]} (1st)", sig_a1),
        (f"{MEMBERS[0]} (2nd)", sig_a2),
        (f"You (1st)",          sig_y1),
        (f"You (2nd)",          sig_y2),
    ]

    print(f"\nAnonymity demo — same message, 4 signatures:")
    for label, sig in cases:
        v = verify(message, sig, public_keys, params)
        print(f"\n  [{label}] → {'VALID' if v else 'INVALID'}")
        print_signature(sig, MEMBERS)

    print("\n  Verifier cannot distinguish who signed.")


if __name__ == "__main__":
    main()
