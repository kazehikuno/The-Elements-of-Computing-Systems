# Christopher Hays
# Elements of Computing Systems
# Parser module of the Assembler, Chapter 6
# Assembly instructions are in the format: destination=operation;branch
# This is converted to binary machine code
# Supports labels for branching and variable creation

import os																		# import operating system interface
from symbol_table import dest_table, branch_table, op_table, label_table		# import lookup tables

# **** open read file ****
from sys import argv					# import the command line argument
program_name, input_name = argv			# first argument is this program's file name, second is the input file name
input_file = open(input_name, 'r+')		# open the input file
data = input_file.readlines()			# reads all the lines and stores them in a list

# **** name and open write file ****
name, extension = os.path.splitext(input_name)		# splits the file name into two parts: name and extension
extension = ".hack"									# change extenstion to '.hack'
output_name = name + extension						# concatenate to create the output file name
output_file = open(output_name, 'w+')				# open the output file
print "New file %s created." % output_name			# print on success

# **** remove comments and white space ****
clean_data = []										# empty list for clean data
for line in data:									# for each line
	line = line.partition('/')[0]					# split the line contents at '/' and keep the leftmost portion
	line = line.strip()								# remove whitespace
	if line == '':									# if the line is blank
		continue									# skip it
	clean_data.append(line)							# write the line to the clean data list
	
	
# **** remove branch labels and add them to the lookup table ****
commands_data = []									# new list for data with the labels removed
for item in clean_data:								# for each item
	if item[0] == '(':								# if it has the label syntax
		label = item.strip('()')					# grab the label
		label_table[label] = len(commands_data)		# add to the lookup table
	else:											# if not a label
		commands_data.append(item)					# add the command to the command list
	

# **** determine instruction type and convert to binary ****
variable_index = 16										# the first 15 addresses are already assigned
for item in commands_data:								# for each item in the list
	if '@' in item:										# if an A-type command
		temp = item[1:]									# grab the constant
		if not temp.isdigit():							# if the string is not all digits
			if temp not in label_table.keys():			# if argument is a new variable
				label_table[temp] = variable_index		# add it to the lookup table and assign it an address
				variable_index += 1						# increment the address index
			temp = label_table[temp]					# get the value from the lookup table
		temp = int(temp)								# convert to integer
		temp = bin(temp)[2:]							# convert to binary string (removing the 0b)
		temp = int(temp)								# convert to integer again
		temp = '%0*d' % (15, temp)						# place leading zeros, padding to 15 bit width
		temp = str(temp)								# convert to string
		item = '0' + temp								# place 0 in front, denoting an A-type command			
		output_file.write(item + "\n")					# write line to the output file
	else:											# if a C-type command
		assignment_index = item.find('=')			# if there is an equals sign this is an assignment instruction
		branch_index = item.find(';')				# a semicolon denotes a branching instruction
		
		if assignment_index == -1:							# not an assignment instruction, must be a branch instruction
			destination = '000'								# binary for the destination portion of the instruction
			operation = item[0:branch_index]				# read the operation
			operation = op_table[operation]					# replace it with binary from a lookup table
			branch = item[branch_index+1:]					# read the branch type
			branch = branch_table[branch]					# replace it with binary from a lookup table
		if branch_index == -1:								# must be an assignment instruction
			branch = '000'									# binary for the branch portion of the instruction
			destination = item[:assignment_index]			# read the destination portion
			destination = dest_table[destination]			# replace it with binary from a lookup table
			operation = item[assignment_index+1:]			# read the operation portion
			operation = op_table[operation]					# replace it with binary from a lookup table
		item = '111' + operation + destination + branch		# concatenate all the binary into the full instruction
		output_file.write(item + "\n")						# write line to the output file
	
	
	
	
	
	
	


	