import argparse
from utils import fetcher, reporter, send
import time
import warnings
import sys

warnings.filterwarnings("ignore")

def main():
    parser = argparse.ArgumentParser(
        description="Generate ransomware JSON or Word report, and optionally send by email. Supports periodic reporting."
    )
    parser.add_argument('-d', '--day', type=int, required=True, help='Number of days to include in the report')
    parser.add_argument('-l', '--lang', type=str, default='en', help='Report language (default: en)')
    parser.add_argument('-r', '--report', action='store_true', help='Generate Word report')
    parser.add_argument('-m', '--mail', action='store_true', help='Send report by email periodically')

    args = parser.parse_args()

    if args.lang.lower() not in ['tr', 'en']:
        print("Only 'tr' and 'en' languages are supported at the moment.")
        sys.exit(1)

    if args.day > 40 or args.day < 1:
        print("The 'day' value must be between 1 and 40. Please enter a valid range.")
        sys.exit(1)

    json_file = fetcher.fetch_and_save_data(args.day, args.lang)
    print(f"Data File generated: {json_file}")

    if args.report:
        word_file = reporter.create_report(json_file, args.lang)
        print(f"Word report generated: {word_file}")

    if args.mail:
        while True:
            json_file = fetcher.fetch_and_save_data(args.day, args.lang)
            word_file = reporter.create_report(json_file, args.lang)
            send.email_with_report(word_file)
            print(f"Waiting {args.day} days for the next report...")
            time.sleep(args.day * 24 * 60 * 60)

if __name__ == "__main__":
    main()
