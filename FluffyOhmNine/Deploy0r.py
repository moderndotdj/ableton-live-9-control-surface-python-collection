'''
Created on Dec 31, 2012

@author: simonfuog
'''
import shutil, glob, os
import subprocess

src_path = "/Users/simonfuog/DJStuff/PyDevWS/FluffyOhmNine/src"
dst_path = "/Applications/Ableton Live 9 Beta.app/Contents/App-Resources/MIDI Remote Scripts/FluffyOhmNine"

for file in glob.glob(src_path + "/*.py"):
    shutil.copy(file, dst_path)

for file in glob.glob(dst_path + "/*.pyc"):
    os.remove(file)
    
subprocess.call(['/bin/restart_live'])
