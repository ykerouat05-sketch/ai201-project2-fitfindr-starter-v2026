# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Successful search

Given a user query that matches at least one listing, the agent should:

1. call `search_listings`
2. select the first returned listing
3. call `suggest_outfit`
4. call `create_fit_card`
5. return the resulting fit card to the user.

**Pass condition:** this works correctly in at least 4 out of 5 test attempts.

**Why this target:** `search_listings` ranks by plain keyword overlap between
the query and each listing's title/description/style_tags. Some phrasings a
person would consider "matching" (synonyms, paraphrases, a word that doesn't
appear verbatim in the data) will score zero even though a human would call it
a hit. 4 of 5 allows for that gap without excusing a search that fails most of
the time.

---

## 2. No search results

Given a user query that matches no listings, the agent should:

1. call `search_listings`
2. receive an empty list
3. stop without calling `suggest_outfit` or `create_fit_card`
4. return a useful message explaining what the user could change about their
   search.

**Pass condition:** this works correctly in 5 out of 5 test attempts.

**Why this target:** this is a plain `if results: ... else: ...` branch on a
deterministic, non-model function — `search_listings` returns `[]` or it
doesn't, and there is no model randomness involved in deciding whether to
stop. Unlike criterion 1, there's no reasonable source of flakiness here, so
anything less than 5 of 5 means the branch itself is broken, not that the
target was too strict.

---

## 3. Size and price constraints

When the user specifies a size and/or maximum price, the selected listing must
satisfy those constraints.

**Pass condition:** at least 4 out of 5 test attempts return a listing
satisfying every specified size and price constraint.

**Why this target:** `max_price` filtering is an exact numeric comparison
(`price <= max_price`), so it should never fail on its own. The risk is size
matching: sizes in the data are free text (`"S/M"`, `"US 9"`, `"XL
(oversized)"`), and a query size has to be checked as one of a listing's own
size tokens rather than a substring, or it will either miss real matches or
let through sizes that only share letters (`"L"` inside `"XL"`). 4 of 5 leaves
room for an edge case in how a size string is tokenized without accepting a
filter that regularly leaks the wrong size.

---

## 4. Fit card contents

When a listing is successfully found, the final fit card must mention:

* the selected item
* its price
* its platform

**Pass condition:** at least 4 out of 5 test attempts produce a fit card
containing all three pieces of information.

**Why this target:** `create_fit_card` calls the model, so the exact wording
varies every time by design (`TEMPERATURE = 0.9`) — that variation is the
point, not a defect. The instruction to the model always asks for item, price,
and platform, but a generative response can occasionally drop one of them even
when the prompt supplies it. 4 of 5 catches a prompt that is reliably good
without demanding the kind of word-for-word guarantee only a non-generative
template could give.

---

## 5. Correct tool-call order

The agent must call the tools in this order:

`search_listings → suggest_outfit → create_fit_card`

If `search_listings` returns an empty list, the agent must stop immediately
and must not call the other two tools.

**Pass condition:** the correct tool-call order and early-stop behavior occur
in 5 out of 5 test attempts.

**Why this target:** this is the loop's control flow, not a model output —
which tool gets called next is decided entirely by Python branching on
`session["search_results"]`, with no randomness anywhere in that decision. If
the order or the early stop is ever wrong, that is a bug in `run_agent`, not
an acceptable rate of variation, so the target is 5 of 5.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
