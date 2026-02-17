import argparse
import datetime
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("API-TOKEN")

API_URL = "https://api-ww.cert.orangecyberdefense.com"
API_HEADERS = {"Authorization": TOKEN}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export advisories by ID or by relative date."
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-id", "--advisory-id", type=str, help="Specific advisory ID to export."
    )

    group.add_argument(
        "-s",
        "--since",
        action="store_true",
        help="Export advisories from a relative date (uses --unit and --amount).",
    )

    # Date options (used only with --since)
    parser.add_argument(
        "-u",
        "--unit",
        choices=["day", "month", "year"],
        default="month",
        help="Time unit for relative date calculation (default: month).",
    )

    parser.add_argument(
        "-a",
        "--amount",
        type=int,
        default=1,
        help="Amount of time units to go back (default: 1).",
    )

    # Output format
    parser.add_argument(
        "-f",
        "--format",
        choices=["html", "md"],
        default="md",
        help="Output format (default: md).",
    )

    # Output directory
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("advisories"),
        help='Output directory (default: "advisories").',
    )

    return parser.parse_args()


def calculate_since_date(unit: str, amount: int) -> str:
    now = datetime.datetime.now()

    if unit == "day":
        result = now - datetime.timedelta(days=amount)

    elif unit == "month":
        result = now - datetime.timedelta(days=30 * amount)

    elif unit == "year":
        result = now - datetime.timedelta(days=365 * amount)

    else:
        raise ValueError("Invalid unit")

    return result.strftime("%Y-%m-%d")


def fetch_and_save_advisory(
    advisory_id: int | str, format: str, output_dir: Path
) -> None:
    print(
        f"Fetching advisory {advisory_id} in {format} format. Will be saved in `./{output_dir}`"
    )
    try:
        response = requests.get(
            f"{API_URL}/api/advisory/{advisory_id}/{format}/minimized",
            headers=API_HEADERS,
        )
        response.raise_for_status()
        advisory = response.json()
        ext = "md" if format == "markdown" else "html"
        filepath = output_dir / f"advisory_{advisory_id}.{ext}"
        filepath.write_text(advisory[format])
    except Exception:
        print(f"Failed to fetch advisory {advisory_id}")


def main():

    args = parse_args()

    format = "markdown" if args.format == "md" else "html"
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.advisory_id:
        fetch_and_save_advisory(args.advisory_id, format, output_dir)

    elif args.since:
        params: dict[str, str | int] = {"limit": 999}
        since_date: str = calculate_since_date(args.unit, args.amount)
        till_date: str = (
            datetime.datetime.now() + datetime.timedelta(days=1)
        ).strftime("%Y-%m-%d")
        params["updated_after"] = since_date
        params["updated_before"] = till_date

        response = requests.get(
            f"{API_URL}/api/advisory/", headers=API_HEADERS, params=params
        )
        response.raise_for_status()

        advisories = response.json()["items"]
        for advisory in advisories:
            fetch_and_save_advisory(advisory["id"], format, output_dir)


if __name__ == "__main__":
    main()
