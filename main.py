from csv_utilite.generation import  generate_from_dict

# Generate CSV from a dictionary
data = {'Name': 'John', 'Age': 25, 'City': 'New York'}
output_path = 'output.csv'
generate_from_dict(data, output_path, headers=['Name', 'Age', 'City'])

# Generate CSV from a list of dictionaries
data = [{'Name': 'John', 'Age': 25, 'City': 'New York'},
        {'Name': 'Jane', 'Age': 30, 'City': 'London'}]
output_path = 'output.csv'
generate_from_dict(data, output_path)