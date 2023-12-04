from litejdb import LiteJDB

# Initialize a generic database with a given entity name
student_database = LiteJDB('Student', silent=True) # silent is False by default

# Add a new record to the database
student_database.add_record(first_name='John', last_name='Doe', age=18, average_grade=85.5)
student_database.add_record(first_name='Jane', last_name='Smith', age=17, average_grade=92.3)

student_database.add_field('test', False)
student_database.update_record('1', 'test', True)

print (student_database.records)

# Search for records with a specific field value
print (student_database.search_records('age', 18))

# Filter records based on multiple fields and their values
filters = {
    "first_name": {"J.*": "regex"},
    "age": {16: "greater"},
    "test": {False: "boolean"}
}

print (student_database.filter_records(filters))
