import pathlib
import sys

wage_phrases = ["hourly_wage", "wage", "salary", "hourly_rate", "rate"]
hours_phrases = ["hours_worked", "worked_hours", "total_hours"]


def parse_args():
    out_file_name = "out.txt"
    data_paths = []
    for i in range(1, len(sys.argv)):
        if sys.argv[i].endswith(".csv"):
            data_paths.append(sys.argv[i])
        if sys.argv[i] == "--report":
            out_file_name = sys.argv[i + 1]
    return out_file_name, data_paths


def parse_data(data, data_paths):
    for path in data_paths:
        with open(path, 'r') as file:
            headers = [h.strip() for h in file.readline().split(',')]
            headers_dict = {}
            for i, header in enumerate(headers):
                header_lower = header.lower()
                if any(phrase in header_lower for phrase in hours_phrases):
                    headers_dict["hours"] = i
                elif any(phrase in header_lower for phrase in wage_phrases):
                    headers_dict["wage"] = i
                else:
                    headers_dict[header] = i
            for row in file.readlines():
                row = row.replace('\n', '')
                row = row.strip().split(',')
                data.append([row[headers_dict["name"]],
                             row[headers_dict["department"]],
                             row[headers_dict["hours"]],
                             row[headers_dict["wage"]],
                             int(row[headers_dict["wage"]]) * int(row[headers_dict["hours"]]),])
    return data


def write_file(data, out_file_name):
    column_widths = []
    write_headers = ["name","department", "hours", "wage", "payout"]
    for i in range(len(write_headers)):
        column_widths.append(len(write_headers[i]))

    for row in data:
        for i, item in enumerate(row):
            if len(str(item)) > column_widths[i]:
                column_widths[i] = len(str(item))
    column_widths = [w + 2 for w in column_widths]
    format_str = "".join([f"{{:<{w}}}" for w in column_widths])

    with open(out_file_name, 'w') as file:
        pass

    with open(out_file_name, "a") as f:
        f.write(format_str.format(*write_headers) + "\n")
        f.write("-" * sum(column_widths) + "\n")
        for row in data:
            f.write(format_str.format(*row))
            f.write(f""+"\n")

def main():
    out_file_name, data_paths = parse_args()
    data = []
    data = parse_data(data, data_paths)
    write_file(data, out_file_name)

if __name__ == '__main__':
    main()
