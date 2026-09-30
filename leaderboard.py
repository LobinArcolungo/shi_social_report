import re
import unicodedata
from collections import defaultdict
from datetime import datetime

POO = "💩"

MONTHS_IT = {
    1: "Gennaio",
    2: "Febbraio",
    3: "Marzo",
    4: "Aprile",
    5: "Maggio",
    6: "Giugno",
    7: "Luglio",
    8: "Agosto",
    9: "Settembre",
    10: "Ottobre",
    11: "Novembre",
    12: "Dicembre",
}

LINE_RE = re.compile(
    r"^\[(\d{2}/\d{2}/\d{2,4}),\s\d{2}:\d{2}:\d{2}\]\s([^:]+):\s(.*)$"
)


def is_emoji_only(text):
    text = text.strip()

    if not text:
        return False

    for char in text:
        if char.isspace():
            continue

        cat = unicodedata.category(char)

        if not (cat.startswith("So") or cat.startswith("Sk")):
            return False

    return True


def parse_chat_file(uploaded_file):

    stats = defaultdict(
        lambda: defaultdict(
            lambda: {"normal": 0, "double": 0}
        )
    )

    months_available = set()

    for raw in uploaded_file:

        line = raw.decode("utf-8")

        m = LINE_RE.match(line.strip())

        if not m:
            continue

        date_str, author, message = m.groups()

        try:
            date = datetime.strptime(
                date_str,
                "%d/%m/%y"
            )
        except:
            date = datetime.strptime(
                date_str,
                "%d/%m/%Y"
            )

        if not is_emoji_only(message):
            continue

        poo_count = message.count(POO)

        if poo_count == 0:
            continue

        key = (date.year, date.month)

        months_available.add(key)

        if poo_count == 1:
            stats[key][author]["normal"] += 1
        else:
            stats[key][author]["double"] += 1

    months = []

    for y, m in sorted(months_available, reverse=True):
        months.append(
            (
                y,
                m,
                f"{MONTHS_IT[m]} {y}"
            )
        )

    return stats, months


def build_month_leaderboard(stats, year, month):

    data = stats[(year, month)]

    ranking = []

    for user, counts in data.items():

        total = (
            counts["normal"]
            + counts["double"]
        )

        ranking.append(
            (
                user,
                total,
                counts["double"]
            )
        )

    ranking.sort(
        key=lambda x: (-x[1], x[0])
    )

    result = []

    for pos, (user, total, doubles) in enumerate(
        ranking,
        start=1
    ):
        result.append(
            f"{pos}. {user} {total} ({doubles}💩💩)"
        )

    return "\n".join(result)