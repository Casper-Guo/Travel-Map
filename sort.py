import json
import sys
from pathlib import Path


def sort_counties(paths):
    """Sort counties by state abbreviation and then by county name, both ascending."""

    def sort_key(county):
        # Use rsplit to always split at the last double underscore
        county_name, state_abbr = county.rsplit("__", 1)
        return (state_abbr, county_name.replace("__", "_"))

    return sorted(paths, key=sort_key)


def main():
    # Check if file path is provided as command line argument
    if len(sys.argv) != 2:
        print("Usage: python3 sort.py <json_file_path>", file=sys.stderr)
        sys.exit(1)

    json_file_path = Path(sys.argv[1])

    try:
        data = json.loads(json_file_path.read_text(encoding="utf-8"))

        if "groups" not in data:
            print("Error: Unexpected JSON format.", file=sys.stderr)
            sys.exit(1)

        for _, group_data in data["groups"].items():
            if "paths" in group_data:
                group_data["paths"] = sort_counties(group_data["paths"])

        json_file_path.write_text(json.dumps(data, indent=3), encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{json_file_path}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
