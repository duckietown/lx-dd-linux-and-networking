"""Print a greeting through sys.stdout."""

# `sys` gives a Python program direct access to its standard streams.
import sys

# Change only the text between the quotation marks.
MESSAGE = "<WRITE A GREETING HERE>"


def main() -> None:
    """Write the configured greeting directly to standard output."""
    # Unlike `print`, `write` does not add a newline, so include one explicitly.
    sys.stdout.write(f"{MESSAGE}\n")


if __name__ == "__main__":
    main()
