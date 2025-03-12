# iCal Timetable Project

This project is designed to create an iCal file from a timetabling Excel sheet stored in SharePoint. It consists of several components that work together to read the Excel file, process the timetable data, and generate an iCal file for easy calendar integration.

## Project Structure

```
ical-timetable-project
├── src
│   ├── main.py            # Entry point of the application
│   ├── excel_reader.py    # Module for reading Excel files
│   ├── ical_generator.py   # Module for generating iCal files
│   └── sharepoint_client.py # Module for interacting with SharePoint
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/ical-timetable-project.git
   cd ical-timetable-project
   ```

2. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Configure SharePoint credentials** in the `sharepoint_client.py` file.
2. **Run the application:**
   ```
   python src/main.py --file-url <SharePoint Excel file URL>
   ```

## Example

To generate an iCal file from a specific Excel file stored in SharePoint, use the following command:

```
python src/main.py --file-url https://yoursharepointsite.com/path/to/excel/file.xlsx
```

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.