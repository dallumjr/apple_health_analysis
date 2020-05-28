
'''	Biometric Data:

		Sources: 
			1. YUNMAI 
			2. MyFitnessPal
			3. Dorian's Apple Watch
			4. Donald's iPhone

		Records:

			type="HKQuantityTypeIdentifierBodyMassIndex" 
			type="HKQuantityTypeIdentifierHeight"
			type="HKQuantityTypeIdentifierBodyMass"
			type="HKQuantityTypeIdentifierHeartRate"
			type="HKQuantityTypeIdentifierBodyFatPercentage"
			type="HKQuantityTypeIdentifierLeanBodyMass"
			type="HKQuantityTypeIdentifierVO2Max"

	Activity Data:

		Sources:
			1. Donald's iPhone
			2. Dorian's Apple Watch

		Records:
			type="HKQuantityTypeIdentifierStepCount"
			type="HKQuantityTypeIdentifierDistanceWalkingRunning"
			type="HKQuantityTypeIdentifierBasalEnergyBurned"
			type="HKQuantityTypeIdentifierActiveEnergyBurned" 
			type="HKQuantityTypeIdentifierFlightsClimbed"
			type="HKQuantityTypeIdentifierAppleExerciseTime"
			type="HKQuantityTypeIdentifierWalkingHeartRateAverage"
			type="HKQuantityTypeIdentifierAppleStandTime"
			type="HKCategoryTypeIdentifierAppleStandHour"
			type="HKCategoryTypeIdentifierMindfulSession"

		Workout: (these have metadata entries)
			workoutActivityType="HKWorkoutActivityTypeYoga"
			workoutActivityType="HKWorkoutActivityTypeRunning"
			workoutActivityType="HKWorkoutActivityTypeWalking"
			workoutActivityType="HKWorkoutActivityTypeHiking"
			workoutActivityType="HKWorkoutActivityTypeCoreTraining" 

'''
import xml.etree.ElementTree as ET
import csv

# Create a CSV file for each metric, so that it can be analyzed with Pandas
def create_metric_csv(source, tag_type_attr, tag_type, metric):
	'''
	Takes in the root of the XML Element object, then creates a csv file with the attributes as headers 
	@source: root of xml tree element
	@tag_type: name of element in XML file. E.G. 'Record' or 'Workout'
	@metric: this will be the "type" field in the Record/Workout Elements
	'''
	# find all nodes associated with the tag type given
	children = source.findall(tag_type)
	# Create a new CSV file with the metric as the name
	new_csv = open(metric +'.csv', 'w', newline='', encoding='utf-8')
	# Make a csv writer instance for the new file
	csvwriter = csv.writer(new_csv)
	# Write the data
	write_csv_rows(children, tag_type_attr, metric, csvwriter)
	# Close the file
	new_csv.close()



def write_csv_rows(children, tag_attr, metric, writer):
	'''
	Takes in a csvwriter and creates the appropriate headers and inputs data row by row.
	@children is the children of the tree that were found by parsing the xml doc
	@tag_attr is 'type' or 'workoutActivityType'
	@writer is the csvwriter
	'''
	# create an array for the column names that you will populate the csv file with
	col_names = []
	# iterate through all the children 
	for child in children:

		attrib_dict = child.attrib
		# create new row each time
		new_row = []
		# check to see if the attribute matches what we're looking for
		if attrib_dict[tag_attr] == metric:
			# check to see if there are headers
			if len(col_names) == 0:
				# if not, go through the keys of the tag we are at that matches our tag_attr, and add the keys to the header
				for key in attrib_dict:
					col_names.append(key)
				# write the new row
				writer.writerow(col_names)
			# always add the data that is available
			for key in col_names:
				new_row.append(attrib_dict[key])
		# write the new row to the file
		writer.writerow(new_row)

def metric_arr_to_csv(arr, tree_root, tag_attr, tag_type):
	for elem in arr:
		create_metric_csv(tree_root, tag_attr, tag_type, elem)
		print('created ' + elem + '.csv')


# parse xml file
tree = ET.parse('export.xml')
# find the root element
root = tree.getroot()

# Arrays for each attribute type that I'm interested in analyzing
Metric_types_record = ["HKQuantityTypeIdentifierBodyMassIndex", 
		"HKQuantityTypeIdentifierBodyMass",
		"HKQuantityTypeIdentifierHeartRate",
		"HKQuantityTypeIdentifierBodyFatPercentage",
		"HKQuantityTypeIdentifierLeanBodyMass",
		"HKQuantityTypeIdentifierVO2Max",
		"HKQuantityTypeIdentifierStepCount",
		"HKQuantityTypeIdentifierDistanceWalkingRunning",
		"HKQuantityTypeIdentifierBasalEnergyBurned",
		"HKQuantityTypeIdentifierActiveEnergyBurned" ,
		"HKQuantityTypeIdentifierFlightsClimbed",
		"HKQuantityTypeIdentifierAppleExerciseTime",
		"HKQuantityTypeIdentifierWalkingHeartRateAverage",
		"HKQuantityTypeIdentifierAppleStandTime",
		"HKCategoryTypeIdentifierAppleStandHour",
		"HKCategoryTypeIdentifierMindfulSession"]

workout_types = [
			"HKWorkoutActivityTypeYoga",
			"HKWorkoutActivityTypeRunning",
			"HKWorkoutActivityTypeWalking",
			"HKWorkoutActivityTypeHiking",
			"HKWorkoutActivityTypeCoreTraining" 
]

# create .csvs for each of the metrics
metric_arr_to_csv(Metric_types_record, root, 'type', 'Record')
metric_arr_to_csv(workout_types, root, 'workoutActivityType', 'Workout')


