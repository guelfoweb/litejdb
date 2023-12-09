# LiteJDB (Lite JSON Database)
LiteJDB is a lightweight database management system, Pandas based, designed for simplicity and
flexibility. It efficiently stores and manages data using JSON serialization, making it easy to 
work with structured information. It's an ideal choice for small projects that demand an 
uncomplicated yet powerful database solution.

## Example

```python
from litejdb import LiteJDB

# Initialize a generic database with a given entity name
student_database = LiteJDB('student_database.json')
```

#### add()
Add a new record to the database
```python
student_database.add({"first_name": "John", "last_name": "Doe", "age": 25})
student_database.add({"first_name": "Jane", "last_name": "Smith", "age": 30})
student_database.add({"first_name": "John", "last_name": "Smith", "age": 22})
```

#### save()
Save the database to a JSON file
```python
student_database.save()
```

#### load()
Load the database from a JSON file
```python
student_database.load('student_database.json')
```

#### query()
Filter records based on multiple fields and their values
```python
filters = "first_name == 'John' and last_name == 'Doe' and age > 23"
result = student_database.query(filters)
print (result)
```
```
  first_name last_name  age
0       John       Doe   25
```
```python
# Return id list
result = student_database.query(filters, "get_id")
```
`[0]`

#### get()
Retrieve a record by its ID
```python
obj = student_database.get(1)
print (obj)
```
```
first_name     Jane
last_name     Smith
age              30
Name: 1, dtype: object
```
Retrieve first_name field by its ID
```python
first_name = student_database.get(1).first_name
print (first_name)
```
`Jane`

#### update()
Update/replace field value by its ID
```python
student_database.update(0, 'first_name', 'Johnny')
print (student_database.df().head())
```
```
  first_name last_name  age
0     Johnny       Doe   25
1       Jane     Smith   30
2       John     Smith   22
```

#### delete()
Delete a record by its ID
```python
student_database.delete(1)
```
Delete a records 0 and 1 by their ID
```python
student_database.delete([0, 1])
```

#### df()
Use database as Pandas dataframe
```python
df = student_database.df().head()
print (df)
```
```
  first_name last_name  age
0       John       Doe   25
1       Jane     Smith   30
2       John     Smith   22
```

