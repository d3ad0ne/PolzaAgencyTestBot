import os


this_script_path = os.path.abspath(__file__).replace('\\', '/')
tmp_path = this_script_path[:this_script_path.find('src')]
print(tmp_path)