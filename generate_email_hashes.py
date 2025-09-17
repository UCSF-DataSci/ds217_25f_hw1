#!/usr/bin/env python3
"""
Utility script to generate hashed email list for test validation
This should be run by the instructor with the actual student roster
The raw email list should NEVER be committed to the repository
"""

import hashlib
import re
import sys


def clean_username(email):
    """Extract and clean username from email address"""
    # Extract username (part before @)
    username = email.split('@')[0]

    # Convert to lowercase and strip whitespace
    username = username.lower().strip()

    # Remove any non-alphanumeric characters
    username = re.sub(r'[^a-z0-9]', '', username)

    return username


def generate_hash(email):
    """Generate SHA256 hash of cleaned username"""
    username = clean_username(email)
    hash_object = hashlib.sha256(username.encode())
    return hash_object.hexdigest()


def main():
    """Process email list and generate hashes"""

    print("Email Hash Generator for DS217 Assignment 01")
    print("=" * 50)
    print("\nThis script generates SHA256 hashes from student emails.")
    print("The raw email list should NEVER be committed to git!")
    print("\nUsage options:")
    print("1. Interactive mode: Run without arguments and paste emails")
    print("2. File mode: python generate_email_hashes.py emails.txt")
    print("\n" + "=" * 50)

    emails = []

    if len(sys.argv) > 1:
        # Read from file
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                emails = [line.strip() for line in f if line.strip()]
            print(f"\nRead {len(emails)} emails from {filename}")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
    else:
        # Interactive mode
        print("\nEnter student emails (one per line).")
        print("Press Ctrl+D (Unix/Mac) or Ctrl+Z (Windows) when done:\n")

        try:
            while True:
                email = input().strip()
                if email:
                    emails.append(email)
        except EOFError:
            print(f"\n\nProcessing {len(emails)} emails...")

    if not emails:
        print("No emails provided!")
        sys.exit(1)

    # Generate hashes
    hashes = []
    print("\n" + "=" * 50)
    print("Generated Hashes:")
    print("=" * 50)

    for email in emails:
        email = email.strip()
        if email:
            # Basic email validation
            if '@' not in email:
                print(f"Warning: '{email}' is not a valid email format, skipping...")
                continue

            email_hash = generate_hash(email)
            hashes.append(email_hash)

            # Show first/last few chars for verification (not the full email!)
            username = clean_username(email)
            masked = username[:2] + "***" + (username[-2:] if len(username) > 4 else "")
            print(f"{masked:15} -> {email_hash}")

    # Generate Python list format for test file
    print("\n" + "=" * 50)
    print("Python list format for test_assignment.py:")
    print("Copy and paste this into the valid_hashes list:")
    print("=" * 50)
    print("\n    valid_hashes = [")
    for h in sorted(hashes):
        print(f'        "{h}",')
    print("    ]")

    # Also save to a file for convenience
    with open('email_hashes.txt', 'w') as f:
        f.write("# SHA256 hashes of student usernames\n")
        f.write("# Generated for DS217 Assignment 01\n")
        f.write("# DO NOT commit the raw email list!\n\n")
        f.write("valid_hashes = [\n")
        for h in sorted(hashes):
            f.write(f'    "{h}",\n')
        f.write("]\n")

    print("\n" + "=" * 50)
    print(f"✓ Processed {len(hashes)} valid emails")
    print("✓ Hashes saved to email_hashes.txt")
    print("\nREMINDER: Do NOT commit raw email lists to git!")
    print("Only commit the hashed values in the test file.")


if __name__ == "__main__":
    main()