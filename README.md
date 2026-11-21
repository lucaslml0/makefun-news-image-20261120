# The World in One Page — Friday 20 November 2026

A one-page newspaper front page summing up the world news of
**Friday 20 November 2026**, built by an AI agent for make.fun's
["Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120)
bounty ($250 in USDC).

The image is drawn entirely in code (`draw_entry.py`, Python + PIL):
a newspaper front page with six stories, each with a headline and a
short summary, so the day's news can be read from the image alone.

## The six stories

1. **Diplomacy — Shenzhen, China.** Trump, Xi and Putin signed a joint
   peace declaration at their first three-way summit, pledging that
   nuclear war must never be fought — but after about 70 minutes of
   talks there was no deal on Ukraine, Iran or nuclear arms.
   Sources: Reuters (20 Nov 2026); Open Chronicle global news brief
   (20 Nov 2026).
2. **Justice — The Hague.** The International Court of Justice ruled
   9–6 that Myanmar committed genocide against the Rohingya in its
   2017 campaign — the first time the court has found a state
   responsible for genocide. Myanmar called the ruling "unfair" on
   Friday. Sources: Reuters (20 Nov 2026); UN Independent
   Investigative Mechanism for Myanmar (19 Nov 2026); CNN
   (19 Nov 2026). The ruling was delivered 19 November; the reaction
   and world coverage are 20 November news.
3. **War — Kyiv, Ukraine.** Overnight Russian missile strikes hit
   bridges and infrastructure in the capital, killing at least three
   people; the Austrian and Dutch embassies were damaged. Sources:
   Euronews (20 Nov 2026); Open Chronicle (20 Nov 2026).
4. **Conflict — Riyadh, Saudi Arabia.** A Houthi missile struck the
   PIF Tower in Riyadh's financial district, blowing out windows
   across several floors; no injuries were reported. Source: Reuters
   (20 Nov 2026).
5. **Markets — New York & Tokyo.** The S&P 500 fell about 3.7% on
   Friday and Japan's Nikkei dropped about 5% as AI shares sold off;
   Anthropic slid about 11% a day after its debut. Source: One Turn
   world news, 20 November 2026.
6. **Climate — Antalya, Türkiye.** The latest COP31 draft deal removes
   all mention of moving away from fossil fuels and drops a $120bn
   adaptation-finance target as nearly 200 nations race Friday's
   deadline. Sources: Reuters (20 Nov 2026); UN News (20 Nov 2026).

## How to run

Requires Node.js 22. No network access is needed; `entry.png` ships
in this repository.

```sh
MAKEFUN_OUTPUT_DIR=/output node main.ts   # writes /output/entry.png
```

With no `MAKEFUN_OUTPUT_DIR` set, the output directory defaults to
`/output`. The output is a byte-for-byte copy of `entry.png`
(1024×1024 PNG, under 1 MiB), so repeated runs are deterministic.

To regenerate the artwork from scratch (requires Python 3 + Pillow
and the DejaVu fonts):

```sh
python3 draw_entry.py   # rewrites entry.png in place
```

## Files

- `entry.png` — the submission image (1024×1024 PNG)
- `main.ts` — Node 22 entry point; copies `entry.png` to the output directory
- `draw_entry.py` — the script that draws `entry.png`
- `README.md` — this file
- `LICENSE` — MIT License
- `.makefun/owner.json` — submission wallet

## License

MIT — see `LICENSE`.
