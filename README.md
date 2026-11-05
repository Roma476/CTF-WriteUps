# CTF Write-ups

<p align="center">
  <img alt="write-ups" src="https://img.shields.io/badge/write--ups-55-9B59B6?style=flat-square">
  <img alt="events" src="https://img.shields.io/badge/events-14-2ea043?style=flat-square">
  <img alt="categories" src="https://img.shields.io/badge/categories-6-1f6feb?style=flat-square">
</p>

<p align="center">
  Solutions and notes from the CTFs I play.<br>
  Written by <a href="https://github.com/Roma476">Roma476</a>: 17-year-old CS student and cybersecurity enthusiast.
</p>

> 55 write-ups across web, binary/pwn, crypto, network, misc and OSINT, from OliCyber, m0leCon, ITSOS CTF and Team Radium training.

## About

This repository is where I write down how I solved each challenge. I try to focus on the reasoning, not just the flag: how I read the challenge, what I tried, why it worked, and what I would do differently next time. Some write-ups are short because the challenge was short; the longer ones are the ones where I learned the most.

## At a glance

| | |
|---|---|
| Write-ups | 55 |
| Events | 14 (2021-2026) |
| Categories | web 25, binary/pwn 17, crypto 4, network 4, misc 3, OSINT 2 |
| First blood | 1 - HTTP Cats (ITSOS CTF 2026) |

## Start here

If you only read a few, these are the ones I would pick:

| Write-up | Event | Category | Why start here |
|---|---|---|---|
| [HTTP Cats](team-radium-training/web/http-cats.md) | ITSOS CTF 2026 | web | First blood; the solution is hidden in HTTP status codes. |
| [mappa](olicyber/2026-territorial/binary/mappa.md) | OliCyber 2026 - Territorial selection | binary | Longest write-up: reversing a flag checker step by step. |
| [MIC](olicyber/2024-national/binary/MIC.md) | OliCyber 2024 - National final | binary | Binary exploitation at the national final, with mitigations enabled. |
| [Age Calculator Pro](olicyber/2024-territorial/binary/age-calculator-pro.md) | OliCyber 2024 - Territorial selection | pwn | Format string leak plus ret2win: a clean first pwn chain. |
| [Emergency Call](olicyber/olicyber-training/binary/emergency-call.md) | OliCyber Training | binary | Static binary, no libc, hand-written syscalls: a lesson in reading assembly. |

## Index

Every write-up, grouped by year and event. The text in parentheses next to each link is the category and the number of solves from the original event.

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
      <td align="center" rowspan="2"><b>2026</b></td>
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

The repository contains write-ups only. No challenge binaries or files.

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
