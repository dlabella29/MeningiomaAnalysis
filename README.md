To run the AuthorAffiliationListGenerator.py, you'll need a .xlsx file that has column A - H as such:
Overall order;	First Name;	Middle Name(s);	Last Name;	Affiliation 1 name;	Affiliation 2 name;	Affiliation 3 name;	Affiliation 4 name
The overall order is the desired order of the authors.
Each author will have their own row starting on row 2. Row 1 reserved for the column headers as specified above.

Overall order	First Name	Middle Name(s)	Last Name	Affiliation 1 name	Affiliation 2 name	Affiliation 3 name	Affiliation 4 name

1	Dominic	 	LaBella	Duke University Medical Center, Department of Radiation Oncology, Durham, NC, USA			

2...

...120...

121	Evan	 	Calabrese	Duke University Medical Center, Department of Radiology, Durham, NC, USA	University of California San Francisco, CA, USA		




The UCSF -gtv.nii.gz cases all have a 1 voxel expansion added in the presegmentations. Therefore, "inward1mm_UCSF.py" creates a gtv-manual.nii.gz label file for the UCSF cases with a 1mm inward margin applied.

The PMH cases all have a translation of the -gtv.nii.gz label files of 1 voxel in "y" direction. Therefore, "translatePMH_y_plus_1.py" creates a gtv-manual.nii.gz label file with a translation of 1 voxel in -y direction.
