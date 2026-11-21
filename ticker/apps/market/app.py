"""The market app's tables, computed in its own process and served to its page (App.tsx)."""

from datetime import UTC, datetime

import kermodes as km

from ticker.md import COLUMNS, TICKS


# Its process holds today's md.ticks for the board: about 500 MiB at 8 million ticks.
@km.app(memory="2Gi")
def market(db):
    # Whichever starts first creates md.ticks (creating it again changes nothing).
    db.create_table(TICKS, COLUMNS)
    # A live table is all of md.ticks's rows, weeks of them in the lake; the board is the day's
    # (UTC), from the day the app starts. The filter reaches the files: past days are not read.
    today = datetime.now(UTC).date().isoformat()
    ticks = (
        db.live_table(TICKS).where(f"ts >= '{today}'").update("notional = price * size")
    )
    # Each symbol's day: where it opened and is now, its range, and what traded.
    day = ticks.agg_by(
        "sym",
        open="first(price)",
        last="last(price)",
        low="min(price)",
        high="max(price)",
        volume="sum(size)",
        notional="sum(notional)",
        trades="count(*)",
    ).update(
        "change = last - open",
        "change_pct = 100 * (last - open) / open",
        "vwap = notional / volume",
    )
    board = day.select(
        "sym",
        "last",
        "change",
        "change_pct",
        "open",
        "low",
        "high",
        "vwap",
        "volume",
        "trades",
    )
    # Every symbol, biggest gain first: a ticking sort orders how its rows are read.
    movers = board.select("sym", "last", "change_pct").sort("change_pct desc")
    return {"board": board, "movers": movers}
