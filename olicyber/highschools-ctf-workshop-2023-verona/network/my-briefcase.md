# My briefcase
| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Verona |
| **Category** | network |
| **Solves** | 218 |

## Overview
The challenge provides a `.pcapng` capture file. Using Wireshark's **File > Export Objects > HTTP**, two transferred files are visible: a `favicon.ico` and a `briefcase.zip` archive. The zip is the interesting one.

Extracting it gives a `briefcase/` folder with 100 files, `flag1.txt` to `flag100.txt`. Opening a few shows the same message:
```
Sorry, the flag is in another file.
```

## Solve
Hashing all files and counting occurrences shows 99 files share the same MD5, while one is different:
```
$ md5sum briefcase/*.txt | awk '{print $1}' | sort | uniq -c | sort -n | head -1
      1 fd0e35f8f81a07b372ed4b785d18adf5
```
Grepping for that hash gives the odd file out:
```
$ md5sum briefcase/*.txt | grep fd0e35f8f81a07b372ed4b785d18adf5
fd0e35f8f81a07b372ed4b785d18adf5  briefcase/flag49.txt
```
Reading it returns the flag.