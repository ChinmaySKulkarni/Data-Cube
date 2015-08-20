#!/usr/bin/python
import sys

#Parse the file into a list of dictionaries where each dictionary corresponds to a record and each key of the dictionary to the attributes of the record.
def parse_file(file_name):
	input_file = open(file_name,"r")
	records = []
	lines = input_file.readlines()
	for line in lines:
		line = line.strip().split('\t')
		record = {}
		record['business_id'] = line[0]
		record['City'] = line[1]
		record['State'] = line[2]
		record['Category'] = line[3]
		record['Rating'] = line[4]
		record['Price'] = line[5]
		records.append(record)
	return records

#Define the hierarchies for the dimensions given in the problem. Hierarchies are stored as key-value pairs where the keys are dimension names and values are the 
#number of hierarchies for that dimension.
def define_hierarchies(keys):
	hierarchy = {}
	for key in keys:
		if key == 'Rating' or key == 'Category' or key == 'Price':
			hierarchy[key] = 1
	hierarchy['Location'] = 2
	return hierarchy
		
#Calculate the number of cuboids using the formula: (L_1 + 1)*(L_2 + 1)* ... (L_n + 1)
def calculate_cuboids(hierarchy):
	number = 1
	for value in hierarchy.values():
		number = number * (value + 1)
	return number

#Each cuboid corresponds to a group-by of subsets of attributes. "group_by" contains the set of attributes on which to group the records by.
#We consider an attribute of "*" as the same as not grouping by that attribute.
def count_group_by(records,group_by):
		cuboid_cell_count = 0
		skip_records = []
		for dim in group_by:
			if dim == "*":
				group_by.remove(dim)
		for record in records:
			if record in skip_records:
				continue
			grouping = []
			grouping.append(record)																			#If no other records are found to be similar for the current record, the current record is a group.
			for next_record in records[records.index(record) + 1:len(records)]:
				match_flag = 0
				for dimension in group_by:																#Match each successive record with the current record for every value of dimension to be grouped by.
					if next_record[dimension] == record[dimension]:
						match_flag = match_flag + 1
				if match_flag == len(group_by):														#If the records match on every dimension of the group-by, they will be part of a group (cell).
					grouping.append(next_record)
					skip_records.append(next_record)												#If a matching record is found, do not consider it again.
			cuboid_cell_count = cuboid_cell_count + 1										#Increment the cuboid_cell_count for each group formed.
		return cuboid_cell_count

#This function takes a group(cell) and dimensions and specific dimension values as input and checks whether the values of dimensions for 
#the records in that group are respectively the same as the values in "dim_vals".
def is_match(cell,dimensions,dim_vals):
	sample_cell = cell[0]
	for dim in dimensions:
		if(sample_cell[dim] != dim_vals[dimensions.index(dim)]):
			return -1																									#If there is no match, return -1. Else, return the number of records in that group(cell).
	return len(cell)

#Function to find the count of a cell(group). The "dimensions" parameter consists of the dimensions on which to group-by. The specific values for theses dimensions are
#given in the "dim_vals" list.
def count_cells(records, dimensions, dim_vals):
		skip_records = []
		remove_indices = []
		for dim in dimensions:
			if dim == "*":																						#"*" value for a dimension means that we do not consider it in the group_by
				remove_indices.append(dimensions.index(dim))
		for index in remove_indices:
			del dim_vals[index]	
			del dimensions[index]																			#Remove the corresponding specific value for that dimension.
		for record in records:
			if record in skip_records:
				continue
			grouping = []
			grouping.append(record)
			for next_record in records[records.index(record) + 1:len(records)]:
				match_flag = 0
				for dimension in dimensions:
					if next_record[dimension] == record[dimension]:
						match_flag = match_flag + 1
				if match_flag == len(dimensions):
					grouping.append(next_record)
					skip_records.append(next_record)
			cell_count = is_match(grouping,dimensions,dim_vals)			#The group (cell) is checked for specific values to see it it matches the values in "dim_vals"
			if(cell_count != -1):																		#is_match() returns -1 if the dimension values for a cell do not match with "dim_vals".
				return cell_count																			#Else it returns "cell_count", i.e. the count of each cell (number of records in a group).
		return 0


records = parse_file(sys.argv[1])
hierarchy = define_hierarchies(records[0].keys())
number_of_cuboids = calculate_cuboids(hierarchy)
print "Q.2) 1. Number of cuboids are:\t" + str(number_of_cuboids) + "\n"

dimensions = ["City","Category","Rating","Price"]
number_of_cells_in_cuboid = count_group_by(records,dimensions)
print "Q.2) 2. Number of cells are:\t" + str(number_of_cells_in_cuboid) + "\n"

dimensions = ["State","Category","Rating","Price"]
number_of_cells_in_cuboid = count_group_by(records,dimensions)
print "Q.2) 3. Number of cells are:\t" + str(number_of_cells_in_cuboid) + "\n"

dimensions = ["*","Category","Rating","Price"]
number_of_cells_in_cuboid = count_group_by(records,dimensions)
print "Q.2) 4. Number of cells are:\t" + str(number_of_cells_in_cuboid) + "\n"

dimensions = ["State","*","Rating","Price"]
dimension_values = ["Illinois","X","3","moderate"]
cell_count = count_cells(records,dimensions,dimension_values)
print "Q.2) 5. Count for the cell is:\t" + str(cell_count) + "\n"

dimensions = ["City","Category","*","*"]
dimension_values = ["Chicago","food","X","X"]
cell_count = count_cells(records,dimensions,dimension_values)
print "Q.2) 6. Count for the cell is:\t" + str(cell_count) + "\n"
