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

All five verdicts below are read straight off `results/run_2026-10-11_1449_before.md`
(the raw evidence from `run_eval.py::run_once` / `agent.py::run_agent`), not assumed.

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4/5 | **MET** (5/5) | All 5 tries of "matching query completes" show `stopped early: no`, a `selected_item`, and a non-empty fit card — every try completed `search_listings` → `suggest_outfit` → `create_fit_card` and returned the card. |
| 2 | Impossible query stops early | 5/5 | **MET** (5/5) | All 5 tries of "impossible query stops early" show `stopped early: yes`, `search_results: 0`, and the identical specific message naming the description/size/price to change — none show a `[3] create_fit_card` trace step. |
| 3 | Size and price constraints | 4/5 | **MET** (5/5) | All 5 tries of "size and price constraints" selected the same listing, whose actual `size` field is `"L"` and `price` is `24.0` — both satisfy the query's `size="L"` and `max_price=30`. |
| 4 | Fit card mentions item, price, platform | 4/5 | **MET** (5/5) | All 5 independently-generated fit cards in "fit card mentions item, price, platform" name the item (e.g. "butterfly print Y2K baby tee"), the price ($18.0 or $18), and the platform ("depop") — checked each of the 5 texts individually, not just one. |
| 5 | Correct tool-call order | 5/5 | **MET** (5/5) | All 5 tries of "correct tool-call order" trace `[1] search_listings (via MCP)` → `[2] suggest_outfit` → `[3] create_fit_card`, in that order. The early-stop half of this rule is additionally confirmed by criterion 2's traces, which show `[1] search_listings` → `[2] branch` with no `[3]` step in any of its 5 tries. |

**Diagnoses**

There were no misses to diagnose — all five criteria hit 5/5 against targets of 4/5
or 5/5. No target was lowered and no test was altered to make this happen; this is
the result of the first real run.

That said, "all 5/5" isn't the same as "all targets were well-tested," and I don't
think it's honest to just stop at the headline numbers. Two of the four scenarios
behind a MET verdict (criteria 1 and 3) ran the *same literal query* five times
against a fully deterministic, non-model function (`search_listings`). Since
`search_listings` has no randomness, those five tries are not five independent
samples of "does this work in general" — they're one sample, repeated. That matters
specifically for criterion 3: the scenario's query (`tee size L under $30`) selects
an item whose size is the plain, unambiguous token `"L"`. A broken, naive
substring-based size filter (`"l" in listing_size`) would have passed this exact
scenario too, because there's no superstring in the candidate pool for "L" to
falsely match inside (nothing like `"XL"` or `"US 9"` is in the "tee"-matching
candidate set for this query). In other words, **this specific test could not have
caught the bug `tools.py::_size_matches` was written to avoid** — it happens to
pass whether or not the token-matching fix is actually in place.

**What I'd tighten next:** Criterion 3's test scenario, not its target. I'd add a
second scenario to `scenarios.py` under criterion 3 — something like
`"sneakers size S under $50"`, where the candidate pool (before size filtering)
genuinely includes listings sized `"US 8"`, `"US 9"`, `"US 8.5"` that a naive
substring check on `"s"` would wrongly include. Requiring the selected item's size
to be an exact token match, 5/5, across *that* scenario would actually exercise the
failure mode the original criterion's "why this target" paragraph names, instead of
only confirming the easy case. I'd leave the original criterion and its 4/5 target
exactly as written in `criteria.md` — the problem isn't the target, it's that the
scenario testing it was too forgiving to ever disconfirm the claim.

**Challenging each verdict** (the strongest case for the opposite call, and why it
doesn't change the verdict):

- **Criterion 1 (MET):** The counter-argument is the one above — one deterministic
  query repeated 5 times isn't real evidence about "phrasings a person would use,"
  which is exactly what the criterion's own justification worries about. But the
  criterion as *written* only asks whether a query that matches something completes
  all three tools, 4 of 5 tries — it doesn't require phrasing diversity. Read
  literally, MET stands; the weakness is in test coverage, not in whether the
  written condition was satisfied.
- **Criterion 2 (MET):** Same objection: 5 identical runs of a pure Python
  `if/else` aren't 5 independent trials in a statistical sense — a latent bug would
  either be in all 5 or none. But criterion 2's own justification already accounts
  for this ("there is no model randomness involved... anything less than 5 of 5
  means the branch itself is broken"), so determinism was priced into the target
  from the start. MET stands.
- **Criterion 3 (MET):** Covered above — the strongest objection I found, since the
  test literally cannot distinguish correct from buggy behavior for this scenario.
  Still, judged strictly against what was measured (the selected item satisfied
  both constraints, 5/5), the verdict is MET; the scenario, not the verdict, is
  what's weak.
- **Criterion 4 (MET):** One try's fit card says "for just $18" instead of
  "$18.0" — if a grader demanded the literal numeral string from the data field,
  that try would be borderline. But criterion 4 only requires the card "mention...
  its price," not reproduce an exact format, and "$18" plainly communicates the
  price. MET stands.
- **Criterion 5 (MET):** The "correct tool-call order" scenario's query always
  matches, so on its own it only proves the happy-path order, never the early-stop
  half of the rule. But criterion 2's traces (same run) independently show the
  early-stop half holding 5/5, so the full rule is still supported — just by two
  scenarios together rather than one. MET stands.



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

**What I changed:** Added one new scenario to `scenarios.py` under criterion 3 —
`"size matching rejects a shoe-size false match"` (query: `"suede size S"`) — on
top of the original criterion 3 scenario, which I left untouched. No code in
`agent.py` or `tools.py` was changed, and criterion 3's wording and 4/5 target in
`criteria.md` were left exactly as written.

**Which failure it was meant to fix:** Not a code failure — a test-coverage gap
found in the Milestone 4 diagnosis. The original criterion 3 scenario
(`"tee size L under $30"`) always selected an item whose size is the plain token
`"L"`, which a broken, naive substring-based size filter would also match
correctly — so a 5/5 PASS there couldn't actually tell a correct implementation
from a regressed one. Before adding the new scenario, I verified with real data
that `"suede"` appears in exactly one listing (`lst_028`, a Chelsea boot sized
`"US 8.5"`), and confirmed by running an isolated copy of a naive substring
matcher (not `tools.py` itself) that it *would* incorrectly select that boot for
a `size="S"` query, while the real `tools.py::_size_matches` correctly excludes
it. This is a scenario that can actually fail if the implementation regresses,
not one that passes either way.

### Run Log — After

Produced by `python run_eval.py --label after`, saved at
`results/run_2026-10-11_1513_after.md` (the baseline,
`results/run_2026-10-11_1449_before.md`, was preserved and is unchanged).

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops early | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Size and price constraints (original scenario) | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Size matching rejects a shoe-size false match (**new**) | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions item, price, platform | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Correct tool-call order | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**New scenario, try 1** (query: `suede size S`), from `run_eval.py::run_once`:

```
- stopped early: yes — No listings matched 'suede' with size S. Try a broader description, a different size, or a higher price limit.
- selected_item: (none)
- search_results: 0

Trace:
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[2] branch
      out: No listings matched 'suede' with size S. Try a broader description, a different size, or a higher price limit.
      →    empty search results — stopping before suggest_outfit/create_fit_card
```
All 5 tries produced this identical result — correctly empty, not the mismatched
boot, confirming the real `_size_matches` implementation handles this adversarial
case. (A PASS here means "no listing was wrongly selected," consistent with
criterion 3's wording — the original scenario's 5 tries each selected a listing
and confirmed it satisfied the constraints, so together the two scenarios cover
both the "something matches" and "something risky doesn't falsely match" halves
of the criterion.)

Before vs. after, side by side — nothing regressed, and criterion 3 is now backed
by a scenario that could actually have failed:

| | Before | After |
|---|---|---|
| Criterion 1 | MET (5/5) | MET (5/5) — unchanged |
| Criterion 2 | MET (5/5) | MET (5/5) — unchanged |
| Criterion 3 | MET (5/5), weak scenario | MET (5/5) **and** (5/5) on the new adversarial scenario |
| Criterion 4 | MET (5/5) | MET (5/5) — unchanged |
| Criterion 5 | MET (5/5) | MET (5/5) — unchanged |

**Did it help, and how do I know:** It strengthened the *test*, not the *agent* —
and I want to be precise about that distinction rather than overclaim. No line of
`tools.py` or `agent.py` changed between the before and after runs, so the
agent's behavior is provably identical; the before/after comparison for criteria
1, 2, 4, and 5 is really just a determinism/consistency check (and it held — same
selected items, same trace shapes, same verdicts). The actual improvement is that
criterion 3 now has a scenario that is capable of catching a real regression in
`_size_matches` (demonstrated above by simulating the naive-substring bug and
showing it would have produced a wrong, non-empty result here), where the
original scenario could not. If `_size_matches` were ever changed back to a
substring check, this new scenario — not the original one — is the one that
would turn red. That is a meaningful improvement in what the test suite can
detect, even though this run surfaced no defect in the current code to fix.


---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

**No criterion remains below target.** Against the most recent evaluation
(`results/run_2026-10-11_1513_after.md`), all five criteria — plus the
additional criterion-3 scenario added in Milestone 5 — are MET at or above
their written targets in `criteria.md`: 1 (4/5 target, 5/5 observed), 2 (5/5,
5/5), 3-original (4/5, 5/5), 3-new/adversarial (4/5, 5/5), 4 (4/5, 5/5), and 5
(5/5, 5/5). There is no criterion to diagnose a fix for here, and I'm not
going to manufacture one — but "nothing failed" isn't the same as "nothing is
worth flagging," so the honest risks I can see, grounded in the actual code
and evaluation evidence, are below.

**Milestone 5's fix, stated precisely:** the one change made was adding an
adversarial test scenario (`"suede size S"`) to `scenarios.py` under criterion
3, on top of the existing scenario — not a code change. `"suede"` appears in
exactly one listing (`lst_028`, a Chelsea boot sized `"US 8.5"`). The correct,
token-based `tools.py::_size_matches` implementation excludes it from a
`size="S"` query (`"us 8.5"` tokenizes to `["us","8","5"]`, which contains no
`"s"` token) and `search_listings` correctly returns `[]`, 5/5 tries. A naive
substring-based matcher (`"s" in "us 8.5"`) would have incorrectly kept that
boot and returned it as `search_results[0]` — I confirmed this by running an
isolated simulation of that bug outside `tools.py`, not by assuming it. So
this change improved *regression detection* for criterion 3: it gives the
test suite a scenario that can actually turn red if `_size_matches` is ever
weakened. It did not fix an implementation bug and did not change the agent's
behavior, because the current size-matching code was already correct —
`tools.py` and `agent.py` are byte-for-byte identical between the before and
after runs.

**The MCP move, and whether it changed anything:** moving `search_listings`
to MCP (Milestone 4) changed exactly one line of behavior in
`agent.py::run_agent` — the direct call `search_listings(description, size,
max_price)` became `call_tool("search_listings", {"description": ...,
"size": ..., "max_price": ...})`, imported from `mcp_client.py`. `call_tool`
opens a stdio connection to `mcp_server.py`, which registers the same
`search_listings` implementation from `tools.py` under `@mcp.tool()`, sends
the request, and unwraps the JSON response back into the identical list of
listing dicts the direct call always returned — `suggest_outfit` and
`create_fit_card` were not moved and still call `tools.py` directly. Behavior
did not change: the before/after evaluation runs selected identical items for
every matched scenario, and `python mcp_client.py` correctly lists
`search_listings` with its schema. The only observable difference anywhere in
the evidence is cosmetic — the trace step is labeled `search_listings (via
MCP)` instead of `search_listings`. The trade-off, visible directly in
`mcp_client.py`'s own docstring, is that `call_tool` starts and stops a fresh
server subprocess over stdio on every single call rather than holding one
connection open — fine for a CLI tool making one search per query, but a real
cost if `run_agent` ever needed to call `search_listings` more than once per
request.

**Remaining limitations and risks, honestly:**

- **Query-phrasing coverage is thin.** Criteria 1, 4, and 5 are each backed by
  exactly one hand-picked query run 5 times against a deterministic search
  function; criterion 3 now has two queries. None of this tests the actual
  risk criterion 1's own justification names — "synonyms, paraphrases, a word
  that doesn't appear verbatim" — since `search_listings` has no randomness
  and the same query always produces the same candidates. A query that a
  person would consider a reasonable match but that shares no literal words
  with the listing text (e.g. "comfy old band shirt" for a "graphic tee")
  would score 0 and be silently dropped, by design of
  `tools.py::_keyword_score`'s exact-word-overlap scoring — this is exactly
  why criterion 1's target is 4/5 and not 5/5, so it's an accepted, named
  limitation rather than a surprise, but it's still genuinely untested here.
- **`_keyword_score` does plain word-overlap, not stemming or synonyms.** A
  query word like "jean" won't match a listing that only says "jeans," and a
  query like "shoes" won't match "sneakers" or "boots" unless that exact word
  appears in the listing's `style_tags`. This is a known trade-off for a
  small mock dataset, not a bug, but it bounds how well the search would
  generalize past these 40 listings.
- **MCP overhead**, covered above — a fresh subprocess per `search_listings`
  call, acceptable at the current single-call-per-request scale.
- **Fit-card content checks (criterion 4) are read by eye, not automated.**
  `run_eval.py` deliberately leaves PASS/FAIL blank for a human to fill in;
  nothing in the codebase automatically verifies a fit card mentions the
  item, price, and platform. That's correct for this course's grading model,
  but it means the criterion 4 verdicts in this README rest on my own
  reading of 5 generated captions each time, not on a script.

I didn't address any of these because none of them are failures against a
written target — they're scope boundaries I noticed while writing the
evaluation and diagnosis, and fixing them (broader phrasing tests, stemming,
a persistent MCP connection, automated fit-card content checks) would each be
a real, separate piece of work rather than something to slip in at the end of
Milestone 6 without its own test.



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
