# Guide for usage of stat_builder.py:

Run 'python3 stat_builder.py' on docker with python3(grub will work)
The directory the script is run from does not matter as it will change directories as needed
The python3 used does not matter as it uses only packages included by default

For Exome will move to:
	/gscmnt/gc2783/qc/GMSworkorders/Exome
and produce stat file:
	cwl.exome.all.DATE.tsv
in the directory:
	/gscmnt/gc2783/qc/GMSworkorders/Exome/exomestats


For WGS will move to:
	/gscmnt/gc2783/qc/GMSworkorders/WGS
and produce stat file:
	cwl.WGS.all.DATE.tsv
in the directory:
	/gscmnt/gc2783/qc/GMSworkorders/WGS/wgsstats

Outputs location of stats file to terminal
The script will then return to the directory is was run from.
