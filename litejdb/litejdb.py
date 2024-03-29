import pandas as pd

class LiteJDB:
    # LiteJDB.version
    version = "0.1.0"
    
    def __init__(self, filename):
        """
        # Initialize a generic database
        db = LiteJDB("database.json")
        """
        self.filename  = filename
        self.dataframe = pd.DataFrame()

    def add(self, data):
        """
        >>> data = {
            "first_name": ["Jhon", "Jane"],
            "last_name": ["Doe", "Smith"],
            "age": [18, 17],
            "average_grade": [85.5, 92.3]
        }
        >>> db.add(data)
        
        or

        >>> db.add({"first_name": "John", "last_name": "Doe", "age":18, "average_grade": 85.5})
        >>> db.add({"first_name": "Jane", "last_name": "Smith", "age":17, "average_grade": 92.3})
        """
        
        # convert scalar to list and fix the following errors:
        # ValueError: If using all scalar values, you must pass an index
        # ValueError: All arrays must be of the same length
        dataset = {}
        for item in data:
            if isinstance(data[item], str) or isinstance(data[item], list):
                dataset.update({item: [data[item]]})
            elif isinstance(data[item], dict):
                dataset.update({item: {data[item]}})
            else:
                dataset.update({item: data[item]})

        # The ignore_index=True key is used to reset indexes incrementally.
        self.dataframe = pd.concat([self.dataframe, pd.DataFrame(dataset)], ignore_index=True)

    def delete(self, index):
        """
        drop rows by ID

        if index is integer:

        >>> db.delete(1)
        >>> print (db.df().head())
          first_name last_name  age  average_grade
        0       John       Doe   18           85.5

        if index is list:

        >>> db.delete([0, 1])
        >>> print (db.df().head())
        Empty DataFrame
        Columns: [first_name, last_name, age, average_grade]
        Index: []
        """
        return self.dataframe.drop(index, inplace=True)

    def get(self, index):
        """
        >>> obj = db.get(1)
        >>> print (obj)
        first_name        Jane
        last_name        Smith
        age                 17
        average_grade     92.3
        Name: 1, dtype: object

        >>> first_name = db.get(0).first_name
        >>> print (first_name)
        John

        >>> obj = db.get([0,1])
        >>> print obj
          first_name last_name  age  average_grade
        0       John       Doe   18           85.5
        1       Jane     Smith   17           92.3
        
        # loc: only work on index
        # iloc: work on position
        # at: get scalar values. It's a very fast loc
        # iat: Get scalar values. It's a very fast iloc
        """
        return self.dataframe.iloc[index]

    def update(self, index, field, new_value):
        """
        student_database.update(0, 'first_name', 'Johnny')
        print (student_database.df().head())
        
          first_name last_name  age
        0     Johnny       Doe   25
        1       Jane     Smith   30
        2       John     Smith   22
        """
        self.dataframe.at[index, field] = new_value

    def duplicates(self):
        """
        db.duplicates()
        """
        return len(self.dataframe) - len(self.dataframe.drop_duplicates())

    def remove_duplicates(self):
        """
        db.remove_duplicates()
        """
        self.dataframe.drop_duplicates(inplace=True)

    def isnull(self):
        """
        - To detect NaN values numpy uses np.isnan().
        - To detect NaN values pandas uses either .isna() or .isnull().
        - The NaN values are inherited from the fact that pandas is built on top of numpy, 
          while the two functions' names originate from R's DataFrames, whose structure 
          and functionality pandas tried to mimic.
        """
        return self.dataframe.isnull().sum().sort_values(ascending=False)

    def fields(self):
        """
        returna list of fields
        
        >>> fields = db.fields()
        >>> print (fields)

        ['first_name', 'last_name', 'age']
        """
        return self.dataframe.columns.values.tolist()

    def query(self, query, get_id=False):
        """
        >>> query = "first_name == 'John' or last_name == 'Smith'"
        >>> filters = db.query(query)
        >>> print (filters)
          first_name last_name  age  average_grade
        0       John       Doe   18           85.5
        1       Jane     Smith   17           92.3

        >>> query = "first_name == 'John' or last_name == 'Smith'"
        >>> filters = db.query(query, "get_id")
        >>> print (filters.head())
        [0, 1]

        info: https://www.statology.org/pandas-check-if-column-contains-string/
        """
        if not get_id:
            return self.dataframe.query(query)
        return self.dataframe.query(query).index.values.tolist()

    def save(self):
        """
        db.save()
        """
        self.dataframe.to_json(self.filename)

    def load(self):
        """
        db.load()
        """
        try:
            self.dataframe = pd.read_json(self.filename)
        except FileNotFoundError:
            self.dataframe = pd.DataFrame()

    def df(self):
        """
        use database as pandas dataframe

        >>> df = db.df().head()
        >>> print (df)
          first_name last_name  age  average_grade
        0       John       Doe   18           85.5
        1       Jane     Smith   17           92.3

        >>> df = db.df()['first_name'].head()
        >>> print (df)
        0    John
        1    Jane
        Name: first_name, dtype: object
        """
        return self.dataframe

