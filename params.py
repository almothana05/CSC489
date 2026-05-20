import random
import json
import os
from generate import generate_params


KEYS_FILE = "keys.txt"


def generate_keypair(p, q, g):
    x = random.randrange(1, q)
    y = pow(g, x, p)
    return x, y


def generate_group(n, p, q, g):
    private_keys, public_keys = [], []
    for _ in range(n):
        x, y = generate_keypair(p, q, g)
        private_keys.append(x)
        public_keys.append(y)
    return private_keys, public_keys


def _save_keys(filepath, p, q, g, private_keys, public_keys):
    data = {
        "p": p,
        "q": q,
        "g": g,
        "keypairs": [{"x": x, "y": y} for x, y in zip(private_keys, public_keys)]
    }
    with open(filepath, "w") as f:
        json.dump(data, f)


def _load_keys(filepath):
    """Returns (p, q, g, private_keys, public_keys) or None if file missing/invalid."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        p = data["p"]
        q = data["q"]
        g = data["g"]
        private_keys = [kp["x"] for kp in data["keypairs"]]
        public_keys  = [kp["y"] for kp in data["keypairs"]]
        return p, q, g, private_keys, public_keys
    except (KeyError, json.JSONDecodeError):
        return None


def load_or_generate_group(n, bits=512, filepath=KEYS_FILE):
    """
    Load params and keypairs from file if available.
    Generate any missing keypairs and save back to file.
    """
    loaded = _load_keys(filepath)

    if loaded:
        p, q, g, private_keys, public_keys = loaded
        print(f"Loaded parameters and {len(private_keys)} keypair(s) from {filepath}")

        # Generate any missing keypairs if n > what was saved
        if len(private_keys) < n:
            missing = n - len(private_keys)
            print(f"Generating {missing} additional keypair(s)...")
            for _ in range(missing):
                x, y = generate_keypair(p, q, g)
                private_keys.append(x)
                public_keys.append(y)
            _save_keys(filepath, p, q, g, private_keys, public_keys)
        else:
            # Use only the first n
            private_keys = private_keys[:n]
            public_keys  = public_keys[:n]
    else:
        # Nothing saved — generate everything from scratch
        params = generate_params(bits)
        p, q, g = params
        private_keys, public_keys = generate_group(n, p, q, g)
        _save_keys(filepath, p, q, g, private_keys, public_keys)
        print(f"Saved parameters and keypairs to {filepath}\n")

    return (p, q, g), private_keys, public_keys
