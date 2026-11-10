# TRIUMVIRATO

| | |
|---|---|
| **Section** | Crypto |
| **Category** | crypto |
| **Solves** | 6 |

## Overview

The challenge description is just a link to `https://html.file.ax/9srd.html`. The page contains a long Base64-looking ciphertext, a short explanation ("three stages of encryption"), and three hints on separate pages. The goal is to identify the mechanisms the hints point to and peel the layers off to recover the flag.

The three hints are:

- **Hint #1:** "Il PRIMO imperatore ROMANO vince un JACKPOT. CRAZYYYYYYY!!!!"
- **Hint #2:** "La coda del MESSAGGIO ci dice tanto."
- **Hint #3:** "QUATTRO livelli di SHA 4^4."

## Solve

The ciphertext ends with `==`, which is Base64 padding, and Hint #2 explicitly points at the tail of the message. Hint #1 mixes "first Roman emperor" with "jackpot": the first Roman emperor is Caesar, and a jackpot is a wall of `777`, so the first stage is a **Caesar cipher with key 7** (ROT7). Hint #3 gives `4^4 = 256`, so the last stage is **SHA-256**, used on **four** pieces.

The ciphertext is not plain Base64, though. A direct decode produces non-printable garbage, because the Base64 alphabet itself was Caesar-shifted before encoding. The shift is applied only to letters, preserving case and leaving digits and `=` untouched.

Undo ROT7 on the letters, then decode:

```python
import base64

cipher = (
    "HWT3SWUfRfGaSMwcGZBrFWNqHZJ0SWz1GcR0ScR4FcUaRPSdScdsGcXpGWXrFfF1FWvsSMv3GWKcGWScGZB4"
    "GrTpFcYfRcN5GfKbHWYeGfJpFfCfF2JrGMz2SPNsHMzqSfN1FMefFcv1RsUaRsecRMv2RfCcScCeRfB0FWd3"
    "SWd2Vcv5SMR0SWKaFcv3RcFsScT2SPNrFcv2GsJsSWKaSZN5FsJrRcJ3FsX1HZF1GcdqFWz0ScR1SWKdFWwe"
    "SPFsSWNDSWXpRcF2RPX3GZX1HPCcScKaHWzqHWN4FswfGcN4RPSaScF2GWSeSfRrRfBqGfFsHMB4SWUeHMFsGPN5"
    "GWOdFz=="
)

def rot(c, k=7):
    if c.isupper():
        return chr((ord(c) - 65 + k) % 26 + 65)
    if c.islower():
        return chr((ord(c) - 97 + k) % 26 + 97)
    return c

shifted = ''.join(rot(c) for c in cipher)
print(base64.b64decode(shifted).decode())
```

The output is four SHA-256 digests, separated by whitespace:

```
807d0fbcae7c4b20518d4d85664f6820aafdf936104122c5073e7744c46c4b87
021fb596db81e6d02bf3d2586ee3981fe519f275c0ac9ca76bbcf2ebb4097d96
79e64d4a277b33f06ee2276743d4ade9342b473158c5691084f65d4d07eec3d5
d10b36aa74a59bcf4a88185837f658afaf3646eff2bb16c3928d0e9335e945d2
```

SHA-256 cannot be decrypted, so the four "levels" are not an iterated hash chain. Trying `SHA256(h1) == h2` fails: each digest is an independent hash of one short fragment of the flag. Since the preimages are short, they can be recovered by brute force over printable ASCII (with the obvious word `flag` included):

```python
import hashlib, itertools, string

targets = {
    "807d0fbcae7c4b20518d4d85664f6820aafdf936104122c5073e7744c46c4b87",
    "021fb596db81e6d02bf3d2586ee3981fe519f275c0ac9ca76bbcf2ebb4097d96",
    "79e64d4a277b33f06ee2276743d4ade9342b473158c5691084f65d4d07eec3d5",
    "d10b36aa74a59bcf4a88185837f658afaf3646eff2bb16c3928d0e9335e945d2",
}

for n in range(1, 4):
    for t in itertools.product(string.printable[:95], repeat=n):
        w = ''.join(t)
        if hashlib.sha256(w.encode()).hexdigest() in targets:
            print(repr(w), hashlib.sha256(w.encode()).hexdigest())
```

The digests resolve to the four fragments of the flag, in the order they appear: the literal `flag`, the opening brace `{`, a short middle fragment, and the closing brace `}`. Concatenating them gives the flag.

The dead ends are informative. Decoding the original string as Base64 gives binary garbage, because the Caesar layer is applied to the Base64 alphabet and must be undone first. Shifting over the full 64-character Base64 alphabet (including digits) also fails; the shift is case-preserving and only touches letters. Treating the four hashes as a chain, or trying to "decrypt" SHA-256, goes nowhere: the four levels are four independent hashes of short plaintext fragments, so the correct move is cracking the preimages, not inverting the hash.

The challenge printed its flag:

```
flag{████…}
```