import json
import sys
import re

"""
LiteJDB (Lite JSON Database) by Gianni Amato (guelfoweb)

LiteJDB is a lightweight database management system designed for simplicity and
flexibility. It efficiently stores and manages data using JSON serialization, 
making it easy to work with structured information. LiteJDB offers key features
such as dynamic field management, quick data retrieval, and seamless integration
with JSON files. It's an ideal choice for small projects that demand an
uncomplicated yet powerful database solution.
"""

class LiteJDB:
    # LiteJDB.version
    version = "0.1.0"

    def __init__(self, entity_name, silent=False):
        # Initialize a generic database with a given entity name
        self.entity_name = entity_name
        # List to store field names
        self.fields = []
        # Dictionary to store records
        self.records = {}
        # Silent print
        self.silent = silent

    def first_id(self):
        if len(self.records) > 0:
            return list(self.records.keys())[0]
        return str(0)

    def last_id(self):
        if len(self.records) > 0:
            return str(int(list(self.records.keys())[-1]))
        return str(0)

    def memory_usage(self):
        # Get object size in byte
        return sys.getsizeof(self)

    def _check_field_type(self, field, value):
        # Check the data type of the field value against the expected data type
        if field in self.fields:
            expected_type = type(self.records['1'][field]) if self.records else type(value)
            if not isinstance(value, expected_type):
                raise ValueError(f"Invalid type for field {field}. Expected {expected_type}, got {type(value)}.")

    def add_record(self, **kwargs):
        # Add a new record to the database
        new_record = {}
        for key, value in kwargs.items():
            if key not in self.fields:
                # If the field is not present, add it to the list of fields
                self.fields.append(key)
            # Check and enforce the data type for the field value
            self._check_field_type(key, value)
            new_record[key] = value

        # Get last_id as string, convert it to integer and finally again to string
        new_id = str(int(self.last_id()) + 1)
        # Add the new record to the records dictionary
        self.records[new_id] = new_record
        if not self.silent:
            print(f"{self.entity_name} added successfully.")

    def add_field(self, field, default_value=None):
        # Add a new field to the database for all existing records with an optional default value
        if field not in self.fields:
            self.fields.append(field)
            for record in self.records.values():
                record[field] = default_value
            if not self.silent:
                print(f"Field '{field}' added successfully.")

    def remove_field(self, field):
        # Remove a field from the database for all existing records
        if field in self.fields:
            self.fields.remove(field)
            for record in self.records.values():
                record.pop(field, None)
            if not self.silent:
                print(f"Field '{field}' removed successfully.")
        else:
            if not self.silent:
                print(f"Field '{field}' does not exist.")

    def get_record(self, record_id):
        # Retrieve a record by its ID
        record_id = str(record_id)
        return self.records.get(record_id, None)

    def update_record(self, record_id, field, new_value):
        # Update the value of a field for a specific record
        record_id = str(record_id)
        if record_id in self.records and field in self.fields:
            # Check and enforce the data type for the new field value
            self._check_field_type(field, new_value)
            self.records[record_id][field] = new_value
            if not self.silent:
                print(f"{self.entity_name} with ID {record_id} updated successfully.")
        else:
            if not self.silent:
                print(f"{self.entity_name} with ID {record_id} or field {field} does not exist.")

    def delete_record(self, record_id):
        # Delete a record by its ID
        record_id = str(record_id)
        if record_id in self.records:
            del self.records[record_id]
            if not self.silent:
                print(f"{self.entity_name} with ID {record_id} deleted successfully.")
        else:
            if not self.silent:
                print(f"{self.entity_name} with ID {record_id} does not exist.")

    def filter_records(self, filters):
        """
        Filter records based on multiple fields and their values.

        Parameters:
        - filters (dict): A dictionary where keys are field names and values are dictionaries
          containing the desired values and match types for each field.

        Returns:
        - list: List of tuples (record_id, record) that match the specified filters.
        """
        results = []

        for record_id, record in self.records.items():
            match = all(self._compare_values(record.get(field, ""), filter_info) 
                        for field, filter_info in filters.items())
            if match:
                results.append((record_id, record))

        return results

    def _compare_values(self, actual_value, filter_info):
        """
        Compare actual and expected values based on the specified match type.

        Parameters:
        - actual_value: The actual value to compare.
        - filter_info: A dictionary containing the desired value and match type for the comparison.

        Returns:
        - bool: True if the values match based on the specified match type, False otherwise.
        """
        filter_value, match_type = next(iter(filter_info.items()))

        if match_type in ["contains", "exact", "regex"]:
            if isinstance(actual_value, str) and isinstance(filter_value, str):
                actual_value = actual_value.lower()
                filter_value = filter_value.lower()
            elif isinstance(actual_value, (int, float, bool)) and isinstance(filter_value, (int, float, bool)):
                pass
            else:
                return False
        elif match_type in ["greater", "less", "equal"]:
            if not isinstance(actual_value, (int, float)) or not isinstance(filter_value, (int, float)):
                return False
        elif match_type == "boolean":
            if not isinstance(actual_value, bool) or not isinstance(filter_value, bool):
                return False
            return actual_value is filter_value
        else:
            raise ValueError("Invalid match_type. Supported values are 'contains', 'exact', 'regex', 'greater', 'less', 'equal', or 'boolean'.")

        if match_type == "contains":
            return filter_value in actual_value
        elif match_type == "exact":
            return actual_value == filter_value
        elif match_type == "regex":
            try:
                pattern = re.compile(filter_value, flags=re.IGNORECASE)
                return bool(pattern.search(str(actual_value)))
            except re.error:
                return False
        elif match_type == "greater":
            return actual_value > filter_value
        elif match_type == "less":
            return actual_value < filter_value
        elif match_type == "equal":
            return actual_value == filter_value
        else:
            return False

    def save_to_file(self, filename):
        # Save the database to a JSON file
        data = {'fields': self.fields, 'records': self.records}
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
        if not self.silent:
            print(f"{self.entity_name} database saved to {filename}.")

    def load_from_file(self, filename):
        # Load the database from a JSON file
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.initialize_from_data(data)
            if not self.silent:
                print(f"{self.entity_name} database loaded from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found. Loading failed.")
        except json.JSONDecodeError as e:
            print(f"An error occurred while loading from {filename}: {e}")

    def initialize_from_data(self, data):
        # Initialize the database from a data dictionary
        self.fields = data.get('fields', [])
        self.records = data.get('records', {})
