# LiteJDB (Lite JSON Database)
LiteJDB is a lightweight database management system designed for simplicity and
flexibility. It efficiently stores and manages data using JSON serialization, 
making it easy to work with structured information. LiteJDB offers key features
such as dynamic field management, quick data retrieval, and seamless integration
with JSON files. It's an ideal choice for small projects that demand an
uncomplicated yet powerful database solution.

## Example

```python
from litejdb import LiteJDB

# Initialize a generic database with a given entity name
student_database = LiteJDB('Student', silent=True) # silent is False by default
```

#### add_record
```python
# Add a new record to the database
student_database.add_record(first_name='John', last_name='Doe', age=18, average_grade=85.5)
student_database.add_record(first_name='Jane', last_name='Smith', age=17, average_grade=92.3)
```

#### save_to_file
```python
# Save the database to a JSON file
student_database.save_to_file('student_database.json')
```

#### load_from_file
```python
# Load the database from a JSON file
student_database.load_from_file('student_database.json')
```

#### search_records
```python
# Search for records with a specific field value
search_results = student_database.search_records('age', 18)

print(f"Search results for age 18: {search_results}")
```
`Search results for age 18: [('1', {'first_name': 'John', 'last_name': 'Doe', 'age': 18, 'average_grade': 85.5})]`


#### fields
```python
# Show all fields
print (student_database.fields)
```
`['first_name', 'last_name', 'age', 'average_grade']`

#### records
```python
# Show all records
print (student_database.records)
```
`{'1': {'first_name': 'John', 'last_name': 'Doe', 'age': 18, 'average_grade': 85.5}, '2': {'first_name': 'Jane', 'last_name': 'Smith', 'age': 17, 'average_grade': 92.3}}`


#### first_id
```python
# Get first ID
print (student_database.first_id())
```
`1`

#### last_id
```python
# Get last ID
print (student_database.last_id())
```
`2`

#### memory_usage
```python
# # Get object size in byte
print (student_database.memory_usage())
```
`48`

#### add_field
```python
# Add a new field to the database for all existing records with an optional default value
student_database.add_field('email', default_value='')
```

### get_record
```python
# Retrieve a record by its ID
print (student_database.get_record('1'))
```
`{'first_name': 'John', 'last_name': 'Doe', 'age': 18, 'average_grade': 85.5, 'email': ''}`

### update_record
```python
# Update the value of a field for a specific record
student_database.update_record('1', 'email', 'info@domain.com')
```

### remove_field
```python
# Remove a field from the database for all existing records
student_database.remove_field('email')
```

### delete_record
```python
# Delete a record by its ID
student_database.delete_record('1')
```
