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

#### Add record to db
```python
student_database.add_record(first_name='John', last_name='Doe', age=18, average_grade=85.5)
student_database.add_record(first_name='Jane', last_name='Smith', age=17, average_grade=92.3)
```

#### Save database
```python
# Save to JSON file
student_database.save_to_file('student_database.json')
```

#### Load database
```python
# Load from JSON file
student_database.load_from_file('student_database.json')
```

#### Search in field
```python
search_results = student_database.search_records('age', 18)
print(f"Search results for age 18: {search_results}")
```
`Search results for age 18: [('1', {'first_name': 'John', 'last_name': 'Doe', 'age': 18, 'average_grade': 85.5})]`


#### Print fields
```python
print (student_database.fields)
```
`['first_name', 'last_name', 'age', 'average_grade']`

#### Print records
```python
print (student_database.records)
```
`{'1': {'first_name': 'John', 'last_name': 'Doe', 'age': 18, 'average_grade': 85.5}, '2': {'first_name': 'Jane', 'last_name': 'Smith', 'age': 17, 'average_grade': 92.3}}`


#### First ID
```python
print (student_database.first_id())
```
`1`

#### Last ID
```python
print (student_database.last_id())
```
`2`

#### Memory usage
```python
print (student_database.memory_usage())
```
`48`

#### Add field
```python
student_database.add_field('email', default_value='')
```

### Get record by ID
```python
print (student_database.get_record('1'))
```
`{'first_name': 'John', 'last_name': 'Doe', 'age': 18, 'average_grade': 85.5, 'email': ''}`

### Update record
```python
student_database.update_record('1', 'email', 'info@domain.com')
```

### Remove field
```python
student_database.remove_field('email')
```

### Delete record
```python
student_database.delete_record('1')
```
