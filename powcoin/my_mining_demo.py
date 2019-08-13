import hashlib
import time


def get_proof(header, nonce):
    preimage = f"{header}:{nonce}".encode()
    proof_hex = hashlib.sha256(preimage).hexdigest()

    return int(proof_hex, 16)


def mine(header, target, nonce):
    nonce = 0
    while get_proof(header, nonce) >= target:
        nonce += 1
    return nonce


def mining_demo(header):
    previous_nonce = -1
    for difficulty_bits in range(1, 30):
        target = 2 ** (256 - difficulty_bits)
        start_time = time.time()
        nonce = mine(header, target, previous_nonce)
        proof = get_proof(header, nonce)
        elapesed_time = time.time() - start_time

        target_sci_not = f"{target:.0e}"
        elapesed_time_sci_no = f"{target:.0e}" if nonce != previous_nonce else ""
        bin_proof_str = f"{proof:0256b}"[:50]
        print(
            f"bits:{difficulty_bits:>3} target:{target_sci_not:>7} elapsed:{elapesed_time_sci_no:>7} nonce:{nonce:>10} proof:{bin_proof_str}...")

        previous_nonce = nonce


if __name__ == "__main__":
    header = "hello"
    # number of leading zeroes we require
    # difficulty_bits = 20
    # target = 2 ** (256 - difficulty_bits)
    nonce = mining_demo(header)
    print(nonce)
    # for nonce in range(10):
    #     proof = get_proof(header, nonce)
    #     print(proof)
    #     print(f"does have 4 leading zeroes {proof < target }")
