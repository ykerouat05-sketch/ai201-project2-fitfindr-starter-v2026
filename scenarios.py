"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Both a size AND a price ceiling that actually filter something out.
        # "tee" + size L matches lst_006 ($24) and lst_033 ($19); size S/M
        # items like lst_002 ($18, no "L" token) and over-budget items
        # outside $30 should be excluded. Tests that the selected item
        # really satisfies both constraints, not just that something came
        # back. Criterion 3.
        "name": "size and price constraints",
        "query": "tee size L under $30",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Milestone 4 diagnosis: the scenario above can't tell a correct,
        # token-based size filter from a naive substring one, because its
        # requested size ("L") never collides with a superstring in the
        # candidate pool. This scenario closes that gap with real data.
        #
        # "suede" appears in exactly one listing: lst_028, a Chelsea boot
        # sized "US 8.5". Verified directly (not assumed) against both
        # implementations before adding this:
        #   - correct (token match): "s" is not a token of "us 8.5"
        #     (tokens are ["us", "8", "5"]), so the boot is filtered out
        #     before scoring, and search_listings("suede", size="S")
        #     returns [] — nothing else in the data contains "suede".
        #   - naive substring ("s" in "us 8.5".lower()): True, so the boot
        #     survives filtering, is the ONLY listing scoring > 0 on
        #     "suede", and becomes search_results[0] — a shoe standing in
        #     for a requested clothing size "S".
        # A regression to substring matching is therefore directly
        # observable here: the agent would select a listing whose actual
        # size plainly fails the requested constraint, instead of stopping
        # on an empty search. Criterion 3.
        "name": "size matching rejects a shoe-size false match",
        "query": "suede size S",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Same query as criterion 1, run 5 separate times (run_eval.py's
        # per-scenario try count) with caching off, so the search always
        # picks the same listing but create_fit_card has to generate 5
        # independent captions for it. Tests whether the fit card reliably
        # mentions the item, price, and platform across tries, not just once.
        # Criterion 4.
        "name": "fit card mentions item, price, platform",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # A query with exactly one unambiguous match, so the trace is easy
        # to read: search_listings -> suggest_outfit -> create_fit_card,
        # in that order, every try. Criterion 5.
        "name": "correct tool-call order",
        "query": "platform sneakers size 8",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
