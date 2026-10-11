# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

A user types a plain-language query like `"vintage graphic tee under $30, size M"`. FitFindr searches the mock listings in `data/listings.json` for items matching the description, and narrows by size and price when the query specifies them. It picks the top-ranked listing, asks the model for an outfit suggestion that pairs the item with pieces already in the user's wardrobe (or general styling advice if the wardrobe is empty), and then asks the model to write a short fit-card caption for the find. The user gets back the selected item, the outfit suggestion, and the caption — or, if nothing in the data matches, a message explaining what to change about the search instead.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the mock listings dataset for items matching a text description, an optional size, and an optional price ceiling, and returns the best matches ranked by keyword overlap.
- **Inputs:** `description` (str) — keywords describing what the user wants, e.g. `"vintage graphic tee"`; `size` (str or None) — a size string to filter by case-insensitively, or `None` to skip size filtering; `max_price` (float or None) — maximum price, inclusive, or `None` to skip price filtering.
- **Returns:** A list of listing dicts, best match first, at most `config.SEARCH_RESULT_LIMIT` of them. Each dict has: `id` (str), `title` (str), `description` (str), `category` (str: one of tops, bottoms, outerwear, shoes, accessories), `style_tags` (list[str]), `size` (str), `condition` (str: excellent, good, or fair), `price` (float), `colors` (list[str]), `brand` (str or None), `platform` (str: depop, thredUp, or poshmark).
- **Empty case:** Returns `[]` (an empty list) when nothing matches — never `None` and never an exception.

### `suggest_outfit`

- **What it does:** Calls the model to suggest one or two outfits pairing a candidate listing with the pieces already in the user's wardrobe.
- **Inputs:** `new_item` (dict) — a listing dict from `search_listings` (same fields as above); `wardrobe` (dict) — a wardrobe dict with an `items` key holding a list of wardrobe item dicts (`id` str, `name` str, `category` str, `colors` list[str], `style_tags` list[str], `notes` str or None); `wardrobe["items"]` may be empty.
- **Returns:** A non-empty string containing the outfit suggestion(s).
- **Empty case:** When `wardrobe["items"]` is empty, still returns a non-empty string — general styling advice for the item rather than an item-pairing suggestion. It never raises and never returns `""`.

### `create_fit_card`

- **What it does:** Calls the model to write a short, two-to-four sentence social-post-style caption for a thrifted find, based on the outfit suggestion and the item's own details.
- **Inputs:** `outfit` (str) — the outfit suggestion string returned by `suggest_outfit`; `new_item` (dict) — the listing dict for the item (same fields as in `search_listings`).
- **Returns:** A string containing a two-to-four sentence caption that mentions the item, its price, and its platform once each.
- **Empty case:** If `outfit` is empty or whitespace-only, returns a descriptive message string explaining that no outfit was available, rather than raising an exception.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` explaining that nothing matched (naming what the user could change, e.g. loosen the price or size) and stop — do not call `suggest_outfit` or `create_fit_card`, and leave `session["selected_item"]`, `session["outfit_suggestion"]`, and `session["fit_card"]` as `None`. Otherwise, take `search_results[0]` as `session["selected_item"]` and continue to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::_parse_query`. One pattern pulls out `under $30`-style phrases for `max_price`; another pulls out `size M`-style phrases for `size`; whatever text is left over, with those matched pieces stripped out and whitespace collapsed, becomes `description`.

**What moves through the session:** `query` → `parsed` (description/size/max_price) → `search_results` (list from `search_listings`) → `selected_item` (one dict from `search_results`) → `outfit_suggestion` (string from `suggest_outfit`, given `selected_item` and `wardrobe`) → `fit_card` (string from `create_fit_card`, given `outfit_suggestion` and `selected_item`). `error` is set instead of the remaining fields if the branch stops early.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I gave Claude my Milestone 2 Tool Inventory spec and asked it to implement `search_listings`, `suggest_outfit`, and `create_fit_card` in `tools.py` to match it, without touching anything else.
- *What came back:* For sizes, Claude didn't do a plain substring check — it pointed out that `"s" in "us 9"` and `"l" in "xl"` are both `True`, so it split each listing's size string into tokens (on anything that isn't a letter/digit) and matched the query size against those tokens instead. `search_listings` also scores by word overlap and caps results at `config.SEARCH_RESULT_LIMIT`, and `create_fit_card` returns a plain string without calling the model when `outfit` is empty/whitespace.
- *What I changed:* I ran the three terminal tests from the docstrings myself, plus the empty-list/empty-wardrobe/empty-outfit cases, and they all matched my spec, so I didn't change the implementation.

**Moment 2**

- *What I asked for:* I asked Claude to wire `run_agent()` in `agent.py` using my Milestone 2 branch rule, with the requirement that every tool's result gets written into `session[...]` and read back out before the next call (not passed straight from one function call into the next).
- *What came back:* Claude added a small regex helper, `_parse_query()`, to split a query like `"graphic tee under $30"` into `description`/`size`/`max_price`, then wrote `run_agent` so it stores into `session["search_results"]`, `session["selected_item"]`, `session["outfit_suggestion"]`, and `session["fit_card"]` one at a time, reading each back before the next call. It kept the session key `outfit_suggestion` (not `outfit`) since that's the key `new_session()` already defines.
- *What I changed:* I ran the happy-path query and the impossible query myself and checked `session["selected_item"] is session["search_results"][0]` directly — it was `True` — and confirmed the empty-search path left `outfit_suggestion` and `fit_card` as `None` without calling the model. Both matched what I wanted, so I kept it as is.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

Produced by `python run_eval.py --label before`, saved at
`results/run_2026-10-11_1449_before.md` (committed as the evidence this
actually ran — full output for every scenario, every try, is in that file).

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops early | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Size and price constraints | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions item, price, platform | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Correct tool-call order | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output, one try per criterion**, from `results/run_2026-10-11_1449_before.md`
(produced by `run_eval.py::run_once`, which calls `agent.py::run_agent`):

**Criterion 1 — "matching query completes", try 1** (query: `vintage graphic tee under $30`)

```
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:
Channeling major 2000s pop-star-off-duty energy with this nostalgic Y2K butterfly baby tee I just scored on depop! At only $18.0, it gives the ultimate pop of color when paired with baggy denim or relaxed trousers. Such a breezy, effortless vibe for everyday wear.
```

**Criterion 2 — "impossible query stops early", try 1** (query: `designer ballgown size XXS under $5`)

```
- stopped early: yes — No listings matched 'designer ballgown' with size XXS and a price under $5.00. Try a broader description, a different size, or a higher price limit.
- selected_item: (none)
- search_results: 0
```

**Criterion 3 — "size and price constraints", try 1** (query: `tee size L under $30`)

```
- stopped early: no
- selected_item: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
- search_results: 2
```
The selected item's actual `size` field is `"L"` and `price` is `24.0` — both satisfy the query's `size="L"` and `max_price=30` constraints.

**Criterion 4 — "fit card mentions item, price, platform", try 1** (query: `vintage graphic tee under $30`)

```
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)

Fit card:
Finally scored this dreamy butterfly print Y2K baby tee on depop for just $18.0, and I am so obsessed with the nostalgic early 2000s energy. It has the ultimate effortless cool-girl vibe, whether I'm dressing it down with baggy denim or styling it retro-chic with wide-leg trousers. I just know this piece is going to be my new daily go-to!
```
Mentions the item ("butterfly print Y2K baby tee"), the price ("$18.0"), and the platform ("depop").

**Criterion 5 — "correct tool-call order", try 1** (query: `platform sneakers size 8`)

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 1 items: Platform Sneakers — White Chunky Sole
[2] suggest_outfit
      in:  dict with keys: new_item
      out: Here are two stylish outfit combinations featuring your new platform sneakers:  **Outfit 1: Casual Streetwear*…
[3] create_fit_card
      in:  dict with keys: outfit
      out: Obsessed with these chunky platform sneakers I just scored on poshmark for $48.0! They give off the ultimate e…
```
`search_listings` → `suggest_outfit` → `create_fit_card`, in that order, with no steps skipped or reordered.

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'graphic tee under $30' --trace

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 6 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +3 more
[2] suggest_outfit
      in:  dict with keys: new_item
      out: Here are two outfit combinations featuring your new Y2K Butterfly Print Baby Tee and pieces from your wardrobe…
[3] create_fit_card
      in:  dict with keys: outfit
      out: Unlocking my ultimate Y2K cool-girl era with this little butterfly print baby tee I just scored on depop! At o…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop
  Outfit:   Here are two outfit combinations featuring your new Y2K Butterfly Print Baby Tee...
  Fit card: Unlocking my ultimate Y2K cool-girl era with this little butterfly print baby tee I just scored on depop!
            At only $18.0, it's giving major nostalgic energy whether I style it with baggy denim or tailored trousers.
            Obsessed with how effortlessly versatile this retro piece is!
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[2] branch
      out: No listings matched 'designer ballgown' with size XXS and a price under $5.00. Try a broader description, a di…
      →    empty search results — stopping before suggest_outfit/create_fit_card

  No listings matched 'designer ballgown' with size XXS and a price under $5.00. Try a broader description, a
  different size, or a higher price limit.
```

The empty-search trace is 2 steps instead of 3 — it stops right after the branch, before either model tool runs.

**On the MCP move:** The commit that was supposed to move `search_listings` to MCP (`c70e4d6`) had registered the tool correctly in `mcp_server.py` and added `from mcp_client import call_tool` to `agent.py`, but `run_agent()` was still calling the local `search_listings(...)` function directly — the import was never actually used. I swapped that one line for `call_tool("search_listings", {...})`, dropped the now-unused direct import of `search_listings` from `tools.py` (the other two tools still import directly — only `search_listings` moved), and confirmed `python mcp_client.py` can list the tool and that `run_agent()` returns the exact same shape of results as before. The rewire worked; the only visible difference is the trace line now reads `search_listings (via MCP)`.

**Failure mode tests**

| # | Failure mode | Command | Observed | Result |
|---|---|---|---|---|
| 1 | Empty search | `python app.py ask "designer ballgown size XXS under $5"` | Agent stopped after `search_listings` returned `[]`. `session["error"]` named the description, size, and price to change. "0 model calls this session" confirmed `suggest_outfit`/`create_fit_card` were never called. | PASS |
| 2 | Empty wardrobe | `python app.py ask "graphic tee under $30" --empty-wardrobe` | `suggest_outfit` returned several paragraphs of general styling advice (no wardrobe pieces named, since there were none), and `create_fit_card` still produced a normal caption afterward. No crash, no empty string. | PASS |
| 3 | Unavailable model | Temporarily flipped the last character of `GEMINI_API_KEY` in `.env`, then ran `python app.py ask "silk slip dress under $40 size M"` (a query not already in the response cache) | The program printed `ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.` and exited cleanly (exit code 1) — no hang, no raw Python traceback. Restored the original key immediately afterward and re-ran `python test.py`, which passed 10/10, confirming the key works again. | PASS |

All three failure modes were triggered on purpose and handled without a crash or a hang.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
