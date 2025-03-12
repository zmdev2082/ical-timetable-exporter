import argparse
import json
import sys
import os
from .excel_reader import ExcelReader
from .ical_generator import IcalGenerator

def timetable_exporter():
    parser = argparse.ArgumentParser(description='Generate an iCal file from a timetabling Excel sheet.')
    parser.add_argument('file_path', type=str, help='The path of the local Excel file.')
    parser.add_argument('filters', type=str, help='Path to the JSON file containing filters.')
    parser.add_argument('--config', type=str, help='Path to the JSON file containing column configuration. (default: config/mapping.json)')
    parser.add_argument('--exact', action='store_true', help='Use exact matching for filters.')
    parser.add_argument('--timezone', type=str, default='Australia/Sydney', help='Timezone for the events (default: Australia/Sydney).')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    parser.add_argument("--output_dir", type=str, default=".", help="Directory to save the output iCal files (default: current directory).")

    try:
        args = parser.parse_args()

        # Read the filters from the JSON file if provided
        filters = None
        with open(args.filters, 'r') as f:
            filters = json.load(f)

        # Read the timetable data from the Excel file
        excel_reader = ExcelReader()
        timetable_df = excel_reader.read_excel(args.file_path, filters["global_filters"], exact_match=args.exact)


    except argparse.ArgumentError as e:
        print(f"Argument error: {e}", file=sys.stderr)
        parser.print_help()
        sys.exit(2)
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    
    output_dir = "./"
    if args.output_dir:
        output_dir = args.output_dir
    elif filters["output_dir"]:
        output_dir = filters["output_dir"]
    
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist. Creating it.")
        os.makedirs(output_dir)

    if args.output_dir:
        filters["output_dir"] = args.output_dir

    if filters["output_dir"] is None:
        filters["output_dir"] = os.path.dirname("./")
    
    if not args.config:
        args.config = os.path.join(os.path.dirname(__file__), "config", "mapping.json")
    if not os.path.exists(args.config):
        print(f"Config file {args.config} does not exist. Exiting.")
        sys.exit(1)

    for calendar in filters["calendars"]:
        output_file = os.path.join(output_dir, f"{calendar["filename"]}.ics")
        calendar_filters = calendar["filter"]
        filtered_df = excel_reader.filter_df(timetable_df, calendar_filters, exact_match=args.exact)
        # Convert the DataFrame to a structured format (e.g., list of dictionaries)
        timetable_data = filtered_df.to_dict(orient='records')

        # Generate the iCal file from the timetable data
        ical_generator = IcalGenerator(output_file, args.config)
        ical_generator.generate_ical(timetable_data)
        
if __name__ == '__main__':
    timetable_exporter()

