from litejdb import LiteJDB

# Examples
student_database = LiteJDB('student_database.json')

student_database.add({"first_name": "John", "last_name": "Doe", "age": 25})
student_database.add({"first_name": "Jane", "last_name": "Smith", "age": 30})
student_database.add({"first_name": "John", "last_name": "Smith", "age": 22})

filters = "first_name == 'John' and last_name == 'Doe' and age > 23"

result = student_database.query(filters, "get_id")
print(result)
# [0]

obj = student_database.get(1)
print (obj)
"""
first_name     Jane
last_name     Smith
age              30
Name: 1, dtype: object
"""

first_name = student_database.get(1).first_name
print (first_name)
# Jane

df = student_database.df().head()
print (df)
"""
  first_name last_name  age
0       John       Doe   25
1       Jane     Smith   30
2       John     Smith   22
"""

student_database.update(0, 'first_name', 'Johnny')
print (student_database.df().head())
"""
  first_name last_name  age
0     Johnny       Doe   25
1       Jane     Smith   30
2       John     Smith   22
"""

fields = student_database.fields()
print (fields)
# ['first_name', 'last_name', 'age']

for index, row in student_database.df().iterrows():
  print (row['first_name'])
"""
Johnny
Jane
John
"""