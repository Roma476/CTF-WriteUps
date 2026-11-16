# The Preserved Moment

| | |
|---|---|
| **Section** | wave 5 |
| **Category** | osint |
| **Solves** | 138 |

## Overview

The subject is Econo Foods, a small-town grocery banner that started as a cooperative of independently owned stores. When a larger distributor moved to buy the brand, each store decided for itself whether to accept, so the same name ended up under several owners, on several domains, across several years. The brief underlines the point: one brand, many stores, and an emphasis on the dates.

The question is a single number from 2006: how much time the Ham and Potatoes Au Gratin recipe claimed to save by using frozen ingredients. The page that answers it no longer exists on the live web, so this is an archive problem — and the two variables are the domain and the year.

## Solve

The banner has lived on more than one domain, and the name has also been used by unrelated companies in other countries, so the first move is to pin the 2006-era site rather than trust a search engine's favourite hit. For the mid-2000s the relevant site is `econofoods.com`.

Rather than clicking through the Wayback calendar month by month, enumerate what the archive actually holds. The CDX API returns every captured URL for a domain in a date range:

```
https://web.archive.org/cdx/search/cdx?url=econofoods.com&matchType=domain&from=20060101&to=20061231&fl=original&collapse=urlkey&limit=200
```

Among the results, the 2006 site exposes a recipes directory with one file per dish:

```
/recipes.html
/recipes/cass_hamhashb.htm
/recipes/cass_hamtatoesaugr.htm
/recipes/cass_maccheese.htm
/recipes/cass_reuben.htm
```

`cass_` is the casserole prefix, and `hamtatoesaugr` is the dish. Browsing the index is a dead end — the same handful of links is served in every capture — but the individual recipe files are separate URLs, and the CDX listing names them directly.

Fetch the raw capture, without the archive's toolbar:

```
https://web.archive.org/web/20060101000000id_/http://www.econofoods.com/recipes/cass_hamtatoesaugr.htm
```

The archived page lists the ingredients — diced frozen onions, shredded frozen hash browns, frozen peas and carrots — and closes with the line the challenge is quoting:

```
Time Saved Using Frozen Ingredients: 25 Minutes!
```

The lesson is that an archive is a URL list, not a website. Calendar browsing only shows what the index page linked to on the days someone happened to crawl it; the CDX API shows everything that was ever captured, including the leaf pages that the index quietly stopped linking.

The answer is **25 minutes**.