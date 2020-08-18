#! /usr/bin/env python
import os
import shutil
import inspect
import configparser
import sys
import argparse

def cmd_inputs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-dir','--GeoNethomedir',help="File path to directory that will hold the cfg file \
			and the inputs and outputs folders. Default is the GeoNet directory.",
			type=str)
	parser.add_argument('-p','--project',
			help="Project title and name of the folder within GIS, Hydraulics, and NWM directories \
			of Inputs and Outputs. Default is 'my_project'.",
			type=str)
	parser.add_argument('-n','--DEM_name',
			help="Name of Input DEM (without extension) and the prefix used for all \
			project outputs. Default is 'dem'",
			type=str)
	parser.add_argument('--input_dir',help="Name of Inputs folder. Default is 'GeoInputs'.",type=str)
	parser.add_argument('--output_dir',help="Name of Outputs folder. Default is 'GeoOutputs'.",type=str)
	
	args = parser.parse_args()
	if args.GeoNethomedir:
		home_dir = args.GeoNethomedir
		if os.path.abspath(home_dir) == os.path.dirname(os.path.abspath(__file__)): # check for ".\"
			home_dir = os.getcwd()
		print(' ')
		print('GeoNet Home Directory for Inputs and Outputs Folder: ')
		print(home_dir)	
	else:
		ab_path = os.path.abspath(__file__)
		home_dir = os.path.dirname(ab_path)
		print(' ')
		print('Using default GeoNet home directory:')
		print(home_dir)

	if args.project:
		project_name=args.project
		print(f"Project Name: {project_name}")
	else:
		project_name='my_project'
		print(f"Default Project Name: {project_name}")
	
	if args.DEM_name:
		dem_name = args.DEM_name
		print(f'DEM Name: {dem_name}')
	else:
		dem_name='dem'
		print(f'Default DEM: {dem_name}')	
	
	if args.input_dir:
		input_directory = args.input_dir
		print(f'Input Folder Name: {input_directory}')
	else:
		input_directory = "GeoInputs"
		print(f'Default Inputs Folder Name: {input_directory}')

	if args.output_dir:
		output_directory = args.output_dir
		print(f'Output Folder Name: {output_directory}')
	else:
		output_directory = "GeoOutputs"
		print(f'Default Outputs Folder Name: {output_directory}')		

	config = configparser.ConfigParser()
	config['Section']={'geofloodhomedir':home_dir,
		'projectname':project_name,
		'dem_name':dem_name,
		'Input_dir':input_directory,
		'Output_dir':output_directory}
	cfg_fp = os.path.join(home_dir,'GeoNet_'+project_name+'.cfg')
	with open(cfg_fp,'w') as configfile:
		config.write(configfile)
	if home_dir!=os.path.dirname(os.path.abspath(__file__)):
		config2 = configparser.ConfigParser()
		config2['CFG Directory']={'project_cfg_pointer':cfg_fp}
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'project_pointer.cfg'),'w') as configfile2:
			config2.write(configfile2)

if __name__=='__main__':
	cmd_inputs()
	print ("Configuration Complete")