import csv
import json
import ipaddress
import logging

# Configure basic logging to demonstrate enterprise best practices
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def validate_ip(ip_str):
    """
    Validates and returns a clean IP address (IPv4 or IPv6).
    Returns None if the string is not a valid IP.
    """
    try:
        clean_ip = ip_str.strip()
        # The ipaddress module automatically handles both IPv4 and IPv6
        return str(ipaddress.ip_address(clean_ip))
    except ValueError:
        return None

def process_server_data(input_csv_path, output_json_path):
    """
    Reads a messy CSV, cleans/flags the data, and exports to a searchable JSON format.
    """
    processed_data = []

    try:
        with open(input_csv_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                # Extract and strip whitespace from basic string fields
                server_id = row.get('Server_ID', '').strip()
                raw_ip = row.get('Raw_IP_Address', '')
                status = row.get('Current_Status', '').strip().capitalize()
                location = row.get('Physical_Location', '').strip()

                # 1. Clean and validate the IP address
                valid_ip = validate_ip(raw_ip)
                if not valid_ip:
                    logging.warning(f"Invalid IP detected for {server_id}: '{raw_ip.strip()}'")

                # 2. Flag 'Offline' or 'Critical' statuses
                needs_attention = status.lower() in ['offline', 'critical']

                # 3. Construct the clean dictionary record
                record = {
                    "server_id": server_id,
                    "ip_address": valid_ip,
                    "ip_is_valid": valid_ip is not None,
                    "status": status,
                    "location": location,
                    "requires_attention": needs_attention
                }

                processed_data.append(record)

        # 4. Export to a well-formatted JSON database
        with open(output_json_path, mode='w', encoding='utf-8') as json_file:
            json.dump(processed_data, json_file, indent=4)

        logging.info(f"Successfully processed {len(processed_data)} records into '{output_json_path}'.")

    except FileNotFoundError:
        logging.error(f"Input file not found: {input_csv_path}. Please check the path.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Define file paths
    INPUT_FILE = 'messy_servers.csv'
    OUTPUT_FILE = 'clean_servers.json'

    # Run the processor
    process_server_data(INPUT_FILE, OUTPUT_FILE)
