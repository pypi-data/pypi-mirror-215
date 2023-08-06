# cmhlims_py

## install the dependencies
pip install -r requirements.txt

## building a package
pip install wheel
python setup.py sdist bdist_wheel

## installing python package
pip install dist/cmh_lims_py-1.0.2-py3-none-any.whl


Usage:

1. import cmhlims package
   pip install cmhlims
   import cmhlims
2. Set Config file
   from cmhlims.setConfig import update_config
   update_config('database.yml', "production")
3. Connect to Lims
   from cmhlims.connectToLIMS import connect_to_lims
   connect_to_lims()
4. Get Analysis
   from cmhlims.getAnalysis import get_analyses
   get_analyses(["cmh000514"], ["GRCh38"])
5. Get Analysis Files
   from cmhlims.getAnalysisFiles import get_analysis_files
   get_analysis_files(["2287"])
6. Get Sample Names
   from cmhlims.getSampleNames import get_sample_names
   get_sample_names()
   
    
    



