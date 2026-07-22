"""
Seeds the database with 5000 sample books across several categories.

Run inside the container so it uses the same DATABASE_URL as the app:
    docker compose run --rm lib python seed_books.py

Safe to re-run: it skips seeding if the books table already has rows,
unless you pass --force.
"""
import argparse
import random

from persistence.database import SessionLocal
from models.book import Book

CATEGORIES = {
    "Science Fiction": [
        "A lone engineer on a dying starship races to solve a failure "
        "before life support runs out.",
        "First contact with an alien signal forces a research team to "
        "question what intelligence really means.",
        "A colony on a distant moon discovers their terraforming project "
        "has awakened something ancient.",
    ],
    "Fantasy": [
        "An apprentice mage stumbles onto a conspiracy that threatens to "
        "unravel the kingdom's fragile peace.",
        "A retired knight is pulled back into battle when an old enemy "
        "resurfaces with a forbidden power.",
        "Two rival kingdoms are forced into an uneasy alliance against a "
        "shared, ancient threat.",
    ],
    "Mystery": [
        "A small-town detective uncovers a decades-old secret while "
        "investigating a seemingly ordinary disappearance.",
        "A journalist's routine assignment turns into a dangerous hunt for "
        "the truth behind a string of unsolved cases.",
        "A private investigator is drawn into a web of lies after a client "
        "vanishes without a trace.",
    ],
    "Romance": [
        "Two rivals forced to work together on a shared project slowly "
        "discover there's more between them than competition.",
        "A chance encounter reunites childhood friends who must confront "
        "feelings they never fully left behind.",
        "A wedding planner falls for the one groom she's determined to "
        "keep at arm's length.",
    ],
    "History": [
        "A sweeping account of the events and figures that shaped a "
        "pivotal era, drawn from newly uncovered records.",
        "An exploration of everyday life during a period of major social "
        "upheaval, told through personal letters and diaries.",
        "A reassessment of a well-known historical turning point, "
        "challenging long-held assumptions.",
    ],
    "Biography": [
        "An intimate portrait of a figure whose decisions quietly shaped "
        "the world around them.",
        "A candid look at the triumphs and setbacks behind a remarkable "
        "public career.",
        "The story of an ordinary life that became extraordinary through "
        "persistence and circumstance.",
    ],
    "Self-Help": [
        "A practical guide to building better habits without relying on "
        "willpower alone.",
        "A framework for making clearer decisions when facing uncertainty "
        "or competing priorities.",
        "Straightforward strategies for managing stress and staying "
        "focused in a demanding routine.",
    ],
    "Technology": [
        "A clear-eyed look at how emerging tools are reshaping the way "
        "people work and communicate.",
        "A hands-on guide to core concepts every newcomer to the field "
        "should understand.",
        "An examination of the tradeoffs behind some of today's most "
        "widely used systems.",
    ],
    "Horror": [
        "A family's move to a quiet countryside home unearths a presence "
        "that was never really gone.",
        "A group of friends' weekend trip takes a dark turn after they "
        "ignore a local warning.",
        "Something in the old apartment building doesn't want new tenants "
        "settling in.",
    ],
    "Children": [
        "A curious young adventurer learns the value of friendship on a "
        "journey through a magical forest.",
        "A small animal with a big dream sets out to prove that size "
        "isn't everything.",
        "A gentle story about sharing, patience, and finding courage in "
        "unexpected places.",
    ],
}

FIRST_NAMES = [
    "James", "Maria", "Chinedu", "Aisha", "Wei", "Elena", "Carlos", "Fatima",
    "Liam", "Sofia", "Kwame", "Yuki", "Amara", "David", "Priya", "Noah",
]
LAST_NAMES = [
    "Okafor", "Garcia", "Chen", "Ibrahim", "Novak", "Silva", "Adeyemi",
    "Kowalski", "Osei", "Fernandez", "Nakamura", "Mensah", "Petrov", "Diallo",
]

TITLE_TEMPLATES = [
    "The {adj} {noun}",
    "{noun} of the {adj} {place}",
    "A {adj} {noun}",
    "The Last {noun}",
    "{place} of {noun}",
    "Chronicles of the {adj} {noun}",
]
ADJECTIVES = [
    "Silent", "Hidden", "Forgotten", "Broken", "Endless", "Quiet", "Distant",
    "Golden", "Shattered", "Restless", "Final", "Secret",
]
NOUNS = [
    "River", "Garden", "Kingdom", "Promise", "Shadow", "Storm", "Light",
    "Mirror", "Journey", "Letter", "Flame", "Bridge",
]
PLACES = [
    "the North", "the Valley", "the Coast", "Winter", "the City",
    "the Mountains", "Summer", "the Harbor",
]


def random_title() -> str:
    template = random.choice(TITLE_TEMPLATES)
    return template.format(
        adj=random.choice(ADJECTIVES),
        noun=random.choice(NOUNS),
        place=random.choice(PLACES),
    )


def random_author() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_isbn(seen: set) -> str:
    while True:
        isbn = f"978{random.randint(10**9, 10**10 - 1)}"
        if isbn not in seen:
            seen.add(isbn)
            return isbn


def build_books(count: int) -> list[Book]:
    seen_isbns: set[str] = set()
    categories = list(CATEGORIES.keys())
    books = []
    for _ in range(count):
        category = random.choice(categories)
        summary = random.choice(CATEGORIES[category])
        books.append(
            Book(
                isbn=random_isbn(seen_isbns),
                title=random_title(),
                author=random_author(),
                category=category,
                summary=summary,
                total_copies=random.randint(1, 10),
                borrowed_copies=0,
            )
        )
    return books


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--count", type=int, default=5000, help="Number of books to insert"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Insert even if the books table already has rows",
    )
    args = parser.parse_args()

    session = SessionLocal()
    try:
        existing = session.query(Book).count()
        if existing and not args.force:
            print(
                f"books table already has {existing} rows — pass --force "
                "to insert anyway."
            )
            return

        print(f"Generating {args.count} books...")
        books = build_books(args.count)

        print("Inserting (bulk)...")
        session.bulk_save_objects(books)
        session.commit()
        print(f"Done. Inserted {len(books)} books.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()

    