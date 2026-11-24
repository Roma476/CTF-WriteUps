# CTF Write-ups

<p align="center">
  <img alt="write-ups" src="https://img.shields.io/badge/write--ups-129-9B59B6?style=flat-square">
  <img alt="events" src="https://img.shields.io/badge/events-15-2ea043?style=flat-square">
  <img alt="categories" src="https://img.shields.io/badge/categories-11-1f6feb?style=flat-square">
</p>

<p align="center">
  Solutions and notes from the CTFs I play.<br>
  Written by <a href="https://github.com/Roma476">Roma476</a>: 17-year-old CS student and cybersecurity enthusiast.
</p>

> 129 write-ups from OliCyber, m0leCon, ITSOS CTF, Team Radium training and POCTF 2026, covering web, binary/pwn, crypto, network, misc, OSINT, exploitation, forensics, game hacking, reverse engineering and steganography.

## About

This repository is where I write down how I solved each challenge. I try to focus on the reasoning, not just the flag: how I read the challenge, what I tried, why it worked, and what I would do differently next time. Some write-ups are short because the challenge was short; the longer ones are the ones where I learned the most.

## At a glance

| | |
|---|---|
| Write-ups | 129 |
| Events | 15 (2021-2026) |
| Categories | web 33, binary/pwn 17, crypto 14, misc 14, OSINT 10, exploitation 8, forensics 8, reverse engineering 8, steganography 8, game hacking 5, network 4 |
| First blood | 1 - HTTP Cats (ITSOS CTF 2026) |

## Start here

If you only read a few, these are the ones I would pick:

| Write-up | Event | Category | Why start here |
|---|---|---|---|
| [HTTP Cats](team-radium-training/web/http-cats.md) | ITSOS CTF 2026 | web | First blood; the solution is hidden in HTTP status codes. |
| [mappa](olicyber/2026-territorial/binary/mappa.md) | OliCyber 2026 - Territorial selection | binary | Reversing a flag checker step by step. |
| [Following the Money](POCTF%202026/osint/following-the-money/following-the-money.md) | POCTF 2026 | osint | Hardest OSINT: combining image metadata, astrometry and a financial trail to recover the location. |
| [MIC](olicyber/2024-national/binary/MIC.md) | OliCyber 2024 - National final | binary | Binary exploitation at the national final, with mitigations enabled. |
| [Age Calculator Pro](olicyber/2024-territorial/binary/age-calculator-pro.md) | OliCyber 2024 - Territorial selection | pwn | Format string leak plus ret2win: a clean first pwn chain. |
| [Emergency Call](olicyber/olicyber-training/binary/emergency-call.md) | OliCyber Training | binary | Static binary, no libc, hand-written syscalls: a lesson in reading assembly. |

## Index

Every write-up, grouped by year and event. POCTF 2026 is grouped by wave, matching the challenge sections, with the hidden bonus challenge at the end. The text in parentheses next to each link is the category and the number of solves from the original event.

<table>
  <thead>
    <tr>
      <th align="center">Year</th>
      <th align="left">Event</th>
      <th align="left">Write-ups</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><b>2021</b></td>
      <td>m0leCon 2021 - Beginner CTF</td>
      <td><a href="olicyber/pwnthem0le/m0leCon%202021%20-%20Beginner%20CTF/how-lucky-you-are.md">how lucky you are</a> (binary, 181)</td>
    </tr>
    <tr>
      <td align="center" rowspan="8"><b>2023</b></td>
      <td>OliCyber 2023 - Training Camp 1</td>
      <td><a href="olicyber/2023-training-camp1/binary/runme.md">runme</a> (binary, 499)<br>
      <a href="olicyber/2023-training-camp1/web/gabibbo-says.md">Gabibbo Says</a> (web, 864)</td>
    </tr>
    <tr>
      <td>OliCyber 2023 - Training Camp 2</td>
      <td><a href="olicyber/2023-training-camp2/network/ssh-login.md">SSH login</a> (network, 427)</td>
    </tr>
    <tr>
      <td>OliCyber 2023 - Training Camp 3</td>
      <td><a href="olicyber/2023-training-camp3/binary/obbibag.md">obbibag</a> (binary, 317)<br>
      <a href="olicyber/2023-training-camp3/web/%C3%A8-tutto-solo-una-convenzione.md">È tutto solo una convenzione</a> (web, 470)</td>
    </tr>
    <tr>
      <td>OliCyber 2023 - Territorial selection</td>
      <td><a href="olicyber/2023-territorial/binary/frasi-basate.md">Frasi basate</a> (binary, 665)<br>
      <a href="olicyber/2023-territorial/web/gabibbo%27s-friend.md">Gabibbo's friend</a> (web, 675)<br>
      <a href="olicyber/2023-territorial/misc/gabibbo-innovazione-tecnologica.md">Gabibbo Innovazione Tecnologica</a> (misc, 331)</td>
    </tr>
    <tr>
      <td>HighSchools CTF Workshop 2023 - Bari</td>
      <td><a href="olicyber/highschools-ctf-workshop-2023-bari/web/cookiec%28tf%29liker1.md">CookieC(TF)liker1</a> (web, 656)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-bari/web/cookiec%28tf%29liker2.md">CookieC(TF)liker2</a> (web, 573)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-bari/web/itasec-shop-1mln-flag.md">ITASECshop - 1mln$ Flag</a> (web, 611)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-bari/web/itasec-shop-fridge-flag.md">ITASECshop - Fridge Flag</a> (web, 400)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-bari/crypto/hexacly-5-t1mes.md">HEXacly 5 t1mes</a> (crypto, 400)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-bari/crypto/x0rland1a.md">X0rland1a</a> (crypto, 267)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-bari/osint/suonano-al-citofono.md">Suonano al citofono...</a> (osint, 455)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-bari/osint/un-giro-sugli-alberi.md">Un giro sugli "alberi"</a> (osint, 293)</td>
    </tr>
    <tr>
      <td>HighSchools CTF Workshop 2023 - Perugia</td>
      <td><a href="olicyber/highschools-ctf-workshop-2023-perugia/web/calcolatrice.md">calcolatrice</a> (web, 253)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-perugia/web/trova-le-soluzioni.md">trova_le_soluzioni</a> (web, 437)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-perugia/web/trova-le-soluzioni-2.md">trova_le_soluzioni2</a> (web, 291)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-perugia/web/trova-le-soluzioni-3.md">trova_le_soluzioni3</a> (web, 216)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-perugia/network/bautiful-content.md">Bautiful Content</a> (network, 213)</td>
    </tr>
    <tr>
      <td>HighSchools CTF Workshop 2023 - Verona</td>
      <td><a href="olicyber/highschools-ctf-workshop-2023-verona/web/find-me.md">find-me</a> (web, 223)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-verona/web/weird-device.md">Weird Device</a> (web, 253)<br>
      <a href="olicyber/highschools-ctf-workshop-2023-verona/network/my-briefcase.md">My briefcase</a> (network, 218)</td>
    </tr>
    <tr>
      <td>m0leCon 2023 - Beginner CTF</td>
      <td><a href="olicyber/pwnthem0le/m0leCon%202023%20-%20Beginner%20CTF/the-wall.md">The Wall</a> (binary, 120)</td>
    </tr>
    <tr>
      <td align="center" rowspan="2"><b>2024</b></td>
      <td>OliCyber 2024 - Territorial selection</td>
      <td><a href="olicyber/2024-territorial/binary/age-calculator-pro.md">Age Calculator Pro</a> (pwn, 131)<br>
      <a href="olicyber/2024-territorial/binary/section31.md">section31</a> (pwn, 328)<br>
      <a href="olicyber/2024-territorial/web/pretty-please.md">Pretty please</a> (web, 889)</td>
    </tr>
    <tr>
      <td>OliCyber 2024 - National final</td>
      <td><a href="olicyber/2024-national/binary/MIC.md">MIC</a> (binary, 90)<br>
      <a href="olicyber/2024-national/web/guess-the-flag.md">Guess the Flag!</a> (web, 352)</td>
    </tr>
    <tr>
      <td align="center"><b>2025</b></td>
      <td>OliCyber 2025 - Territorial selection</td>
      <td><a href="olicyber/2025-territorial/binary/baity5.md">Baity5</a> (binary, 211)<br>
      <a href="olicyber/2025-territorial/web/la-pazienza-%C3%A8-la-virt%C3%B9-dei-forti.md">La pazienza è la virtù dei forti</a> (web, 617)<br>
      <a href="olicyber/2025-territorial/crypto/insecure-passphrase-generator.md">Insecure Passphrase Generator</a> (crypto, 235)</td>
    </tr>
    <tr>
      <td align="center" rowspan="3"><b>2026</b></td>
      <td>OliCyber 2026 - Territorial selection</td>
      <td><a href="olicyber/2026-territorial/binary/mappa.md">mappa</a> (binary, 54)<br>
      <a href="olicyber/2026-territorial/binary/trace-the-void.md">Trace the void</a> (binary, 93)<br>
      <a href="olicyber/2026-territorial/web/useless-login.md">Useless login</a> (web, 143)</td>
    </tr>
    <tr>
      <td>ITSOS CTF 2026</td>
      <td><a href="team-radium-training/web/http-cats.md">HTTP Cats (hard)</a> (web, 1, first blood)</td>
    </tr>
    <tr>
      <td>POCTF 2026</td>
      <td>
        <details>
          <summary>Wave 1 — 8 writeups</summary>
          <a href="POCTF%202026/crypto/letters-never-sent.md">Letters Never Sent</a> (crypto, 876)<br>
          <a href="POCTF%202026/exploitation/read-me-my-fortune.md">Read Me My Fortune</a> (exploitation, 586)<br>
          <a href="POCTF%202026/forensics/everything-left-open.md">Everything Left Open</a> (forensics, 801)<br>
          <a href="POCTF%202026/misc/the-apparatus-invocation.md">The Apparatus, Invocation</a> (misc, 633)<br>
          <a href="POCTF%202026/osint/where-the-light-fails-to-fall.md">Where the Light Fails to Fall</a> (osint, 516)<br>
          <a href="POCTF%202026/reverse%20engineering/excavation.md">Excavation</a> (reverse engineering, 459)<br>
          <a href="POCTF%202026/steganography/invisible-ink.md">Invisible Ink</a> (steganography, 583)<br>
          <a href="POCTF%202026/web/the-shape-of-a-query.md">The Shape of a Query</a> (web, 764)
        </details>
        <details>
          <summary>Wave 2 — 9 writeups</summary>
          <a href="POCTF%202026/crypto/the-apparatus-rapport.md">The Apparatus, Rapport</a> (crypto, 487)<br>
          <a href="POCTF%202026/exploitation/thirty-two-steps-down.md">Thirty-Two Steps Down</a> (exploitation, 383)<br>
          <a href="POCTF%202026/forensics/a-cabin-worth.md">A Cabin Worth</a> (forensics, 434)<br>
          <a href="POCTF%202026/game%20hacking/leap-of-faith.md">Leap of Faith</a> (game hacking, 352)<br>
          <a href="POCTF%202026/misc/frequency-and-consequence.md">Frequency and Consequence</a> (misc, 373)<br>
          <a href="POCTF%202026/osint/a-borrowed-name.md">A Borrowed Name</a> (osint, 467)<br>
          <a href="POCTF%202026/reverse%20engineering/the-disassembled-mind.md">The Disassembled Mind</a> (reverse engineering, 405)<br>
          <a href="POCTF%202026/steganography/commit-to-memory.md">Commit to Memory</a> (steganography, 376)<br>
          <a href="POCTF%202026/web/poisoned-well.md">Poisoned Well</a> (web, 579)
        </details>
        <details>
          <summary>Wave 3 — 8 writeups</summary>
          <a href="POCTF%202026/crypto/the-consulting-room.md">The Consulting Room</a> (crypto, 296)<br>
          <a href="POCTF%202026/exploitation/the-sandglass.md">The Sandglass</a> (exploitation, 342)<br>
          <a href="POCTF%202026/forensics/what-goes-unwritten.md">What Goes Unwritten</a> (forensics, 313)<br>
          <a href="POCTF%202026/misc/columns-of-holes.md">Columns of Holes</a> (misc, 261)<br>
          <a href="POCTF%202026/osint/strings-attached.md">Strings Attached</a> (osint, 292)<br>
          <a href="POCTF%202026/reverse%20engineering/panoptican.md">Panoptican</a> (reverse engineering, 333)<br>
          <a href="POCTF%202026/steganography/the-apparatus-the-rapping.md">The Apparatus, The Rapping</a> (steganography, 311)<br>
          <a href="POCTF%202026/web/no-structure-required.md">No Structure Required</a> (web, 340)
        </details>
        <details>
          <summary>Wave 4 — 9 writeups</summary>
          <a href="POCTF%202026/crypto/a-map-of-small-things.md">A Map of Small Things</a> (crypto, 320)<br>
          <a href="POCTF%202026/exploitation/a-few-seconds-either-way.md">A Few Seconds Either Way</a> (exploitation, 239)<br>
          <a href="POCTF%202026/forensics/a-quiet-home.md">A Quiet Home</a> (forensics, 281)<br>
          <a href="POCTF%202026/game%20hacking/health-is-a-social-construct.md">Health Is a Social Construct</a> (game hacking, 206)<br>
          <a href="POCTF%202026/misc/a-peculiar-game.md">A Peculiar Game</a> (misc, 215)<br>
          <a href="POCTF%202026/osint/the-apparatus-apport.md">The Apparatus, Apport</a> (osint, 274)<br>
          <a href="POCTF%202026/reverse%20engineering/an-invented-language.md">An Invented Language</a> (reverse engineering, 256)<br>
          <a href="POCTF%202026/steganography/velocity.md">Velocity</a> (steganography, 257)<br>
          <a href="POCTF%202026/web/the-logic-inside.md">The Logic Inside</a> (web, 262)
        </details>
        <details>
          <summary>Wave 5 — 9 writeups</summary>
          <a href="POCTF%202026/crypto/forty-measures-deep.md">Forty Measures Deep</a> (crypto, 168)<br>
          <a href="POCTF%202026/exploitation/what-the-heap-remembers.md">What the Heap Remembers</a> (exploitation, 178)<br>
          <a href="POCTF%202026/forensics/archaeology-of-mistakes.md">Archaeology of Mistakes</a> (forensics, 194)<br>
          <a href="POCTF%202026/game%20hacking/the-house-always-misses.md">The House Always Misses</a> (game hacking, 141)<br>
          <a href="POCTF%202026/misc/conditional-existence.md">Conditional Existence</a> (misc, 163)<br>
          <a href="POCTF%202026/osint/the-preserved-moment.md">The Preserved Moment</a> (osint, 138)<br>
          <a href="POCTF%202026/reverse%20engineering/the-oracles-weight.md">The Oracle's Weight</a> (reverse engineering, 116)<br>
          <a href="POCTF%202026/steganography/the-hidden-path.md">The Hidden Path</a> (steganography, 160)<br>
          <a href="POCTF%202026/web/the-apparatus-levitation.md">The Apparatus, Levitation</a> (web, 168)
        </details>
        <details>
          <summary>Wave 6 — 8 writeups</summary>
          <a href="POCTF%202026/crypto/noise-below-the-signal.md">Noise Below the Signal</a> (crypto, 195)<br>
          <a href="POCTF%202026/exploitation/the-interpreters-margin.md">The Interpreter's Margin</a> (exploitation, 174)<br>
          <a href="POCTF%202026/forensics/the-apparatus-ectograph.md">The Apparatus, Ectograph</a> (forensics, 183)<br>
          <a href="POCTF%202026/misc/the-tower-of-babel.md">The Tower of Babel</a> (misc, 159)<br>
          <a href="POCTF%202026/osint/what-was-exposed.md">What Was Exposed</a> (osint, 119)<br>
          <a href="POCTF%202026/reverse%20engineering/the-oxidized-archive.md">The Oxidized Archive</a> (reverse engineering, 161)<br>
          <a href="POCTF%202026/steganography/the-wrong-channel.md">The Wrong Channel</a> (steganography, 161)<br>
          <a href="POCTF%202026/web/the-interior-route.md">The Interior Route</a> (web, 148)
        </details>
        <details>
          <summary>Wave 7 — 9 writeups</summary>
          <a href="POCTF%202026/crypto/the-notarys-seal.md">The Notary's Seal</a> (crypto, 150)<br>
          <a href="POCTF%202026/exploitation/permission-slip.md">Permission Slip</a> (exploitation, 126)<br>
          <a href="POCTF%202026/forensics/structural-failure.md">Structural Failure</a> (forensics, 136)<br>
          <a href="POCTF%202026/game%20hacking/terms-and-condition-apply.md">Terms and Conditions Apply</a> (game hacking, 92)<br>
          <a href="POCTF%202026/misc/leave-no-trace.md">Leave No Trace</a> (misc, 104)<br>
          <a href="POCTF%202026/osint/the-view-from-above.md">The View from Above</a> (osint, 113)<br>
          <a href="POCTF%202026/reverse%20engineering/the-apparatus-dissolution.md">The Apparatus, Dissolution</a> (reverse engineering, 122)<br>
          <a href="POCTF%202026/steganography/the-geometry-of-secrets.md">The Geometry of Secrets</a> (steganography, 109)<br>
          <a href="POCTF%202026/web/between-the-lines.md">Between the Lines</a> (web, 121)
        </details>
        <details>
          <summary>Wave 8 — 9 writeups</summary>
          <a href="POCTF%202026/crypto/the-cipher-in-the-stars.md">The Cipher in the Stars</a> (crypto, 73)<br>
          <a href="POCTF%202026/exploitation/the-apparatus-manifestation.md">The Apparatus, Manifestation</a> (exploitation, 63)<br>
          <a href="POCTF%202026/forensics/the-accused.md">The Accused</a> (forensics, 67)<br>
          <a href="POCTF%202026/game%20hacking/client-side-truth.md">Client-Side Truth</a> (game hacking, 53)<br>
          <a href="POCTF%202026/misc/the-ancient-instruction.md">The Ancient Instruction</a> (misc, 66)<br>
          <a href="POCTF%202026/osint/following-the-money/following-the-money.md">Following the Money</a> (osint, 35)<br>
          <a href="POCTF%202026/reverse%20engineering/against-the-clock.md">Against the Clock</a> (reverse engineering, 61)<br>
          <a href="POCTF%202026/steganography/the-pattern-language.md">The Pattern Language</a> (steganography, 50)<br>
          <a href="POCTF%202026/web/the-state-of-trust.md">The State of Trust</a> (web, 62)
        </details>
        <details>
          <summary>Hidden — 1 writeup</summary>
          <a href="POCTF%202026/misc/ghostbuster.md">Ghostbuster</a> (misc, hidden bonus)
        </details>
      </td>
    </tr>
    <tr>
      <td align="center" rowspan="2"><b>N/A</b></td>
      <td>OliCyber Training</td>
      <td><a href="olicyber/olicyber-training/binary/emergency-call.md">Emergency Call</a> (binary, 216)<br>
      <a href="olicyber/olicyber-training/binary/formatted.md">Formatted</a> (binary, 420)<br>
      <a href="olicyber/olicyber-training/binary/hidden_variable.md">Hidden Variable</a> (binary, 1127)<br>
      <a href="olicyber/olicyber-training/binary/super_market.md">Super Market</a> (binary, 1177)<br>
      <a href="olicyber/olicyber-training/web/click-me.md">Click Me</a> (web, 3362)<br>
      <a href="olicyber/olicyber-training/web/flags-shop.md">Flag Shop</a> (web, 2156)<br>
      <a href="olicyber/olicyber-training/web/headache.md">Headache</a> (web, 3362)<br>
      <a href="olicyber/olicyber-training/web/no-robots-here.md">No Robots Here</a> (web, 3249)<br>
      <a href="olicyber/olicyber-training/web/password-changer-3000.md">Password Changer 3000</a> (web, 1838)<br>
      <a href="olicyber/olicyber-training/crypto/tutte-le-strade-portano-a-roma.md">Tutte le strade portano a Roma</a> (crypto, 2409)<br>
      <a href="olicyber/olicyber-training/network/g4tto.md">G4tto</a> (network, 2000)<br>
      <a href="olicyber/olicyber-training/misc/2048.md">2048</a> (misc, 1355)<br>
      <a href="olicyber/olicyber-training/misc/byte-flag.md">Byte-flag</a> (misc, 2600)</td>
    </tr>
    <tr>
      <td>Team Radium training</td>
      <td><a href="team-radium-training/binary/banca-benty.md">Banca Benty</a> (binary, 25)<br>
      <a href="team-radium-training/binary/binario-sus.md">Binario Sus</a> (binary, 8)<br>
      <a href="team-radium-training/crypto/il-solito-cifrario.md">Substitution Cipher</a> (crypto, 14)<br>
      <a href="team-radium-training/crypto/triumvirato.md">TRIUMVIRATO</a> (crypto, 6)<br>
      <a href="team-radium-training/misc/bit.md">BIT</a> (misc, 3)<br>
      <a href="team-radium-training/misc/sbsbsbsaskdjaksj-keamfefaf.md">sbsbsbsaskdjaksj keamfefaf</a> (misc, 16)<br>
      <a href="team-radium-training/web/includimi.md">Includimi</a> (web, 6)<br>
      <a href="team-radium-training/web/spaccami-easy.md">Spaccami Easy</a> (web, 29)</td>
    </tr>
  </tbody>
</table>

N/A marks the training collections, which are not tied to a single year.

## Repository structure

Each write-up lives at a predictable path:

```
<platform>/<event>/<category>/<challenge>.md
```

For example:

```
olicyber/2024-national/binary/MIC.md
team-radium-training/web/http-cats.md
```

The repository contains write-ups and small supporting assets. Original challenge binaries are not included.

## Write-up format

New write-ups follow this structure:

```markdown
# Challenge name

| | |
|---|---|
| **Section** | Event name |
| **Category** | web |
| **Solves** | 123 |

## Overview

What the challenge gives you and what it asks for.

## Solve

The reasoning, the commands, and the payloads, in the order I actually used them.

```

## Conventions

- **Solves** comes from the original challenge metadata and is kept for context, not as a ranking.
- **Flags** are intentionally omitted: some platforms may consider publishing them flag sharing.
- **Language:** write-ups are in English; some challenge titles are in Italian because that was the original name.

## Disclaimer

Everything here is for educational purposes. Do not use these techniques on systems you do not own or have permission to test.

## License

[MIT](LICENSE)

---

<p align="center">
  <a href="https://github.com/Roma476">GitHub</a> |
  <a href="https://www.linkedin.com/in/robert-gabriel-friciu/">LinkedIn</a> |
  <a href="https://pypi.org/project/ismypwdsafe/">IsMyPwdSafe</a>
</p>
