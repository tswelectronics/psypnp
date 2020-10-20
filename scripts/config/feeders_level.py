'''

Set the configured feeder height based on some reference elevation
for all feeders matching some name/substring of name.

This script takes into account the height of the parts set in these 
feeds.

For example, you have 10 feeders called "left*" and they hold the 
top of all their parts--tiny 0402s, fat 1210 caps, etc--at the same
level, say -34.00mm.  When the script is called, it will get the
height for each part and adjust the configured height of the feeder
to ensure the nozzle goes down to -34, so e.g.

  -34.1 for the 0402
  -34.9 for the 1210
etc

@see: https://inductive-kickback.com/2020/10/psypnp-for-openpnp/

@author: Pat Deegan
@copyright: Copyright (C) 2020 Pat Deegan, https://psychogenic.com
@license: GPL version 3, see LICENSE file for details.

'''

############## BOILER PLATE #################
# boiler plate to get access to psypnp modules, outside scripts/ dir
import os.path
import sys
python_scripts_folder = os.path.join(scripting.getScriptsDirectory().toString(),
                                      '..', 'lib')
sys.path.append(python_scripts_folder)

# setup globals for modules
import psypnp.globals
psypnp.globals.setup(machine, config, scripting, gui)

############## /BOILER PLATE #################

from org.openpnp.model import Location, Length, LengthUnit 

import psypnp

def main():
    set_feeder_heights()

def get_height_len():
    lenstr = psypnp.getUserInput("Enter desired height (mm) for these feeders", -9.876)
    try:
        heightval = float(lenstr)
        height = Length(heightval, LengthUnit.Millimeters)
    except:
        height = Length.parse(lenstr)

    return height

def set_feeder_heights():
    pname = psypnp.getUserInput("Name of feeder, or substring thereof to match many", "8mmStrip")
    if pname is None or not len(pname):
        return
    height = get_height_len()
    if height is None:
        return

    numChanged = 0
    for afeeder in machine.getFeeders():
        if pname == '*' or afeeder.getName().find(pname) >= 0:
            apart = afeeder.getPart()
            if apart is not None:
                pHeight = apart.getHeight()
                feederHeight = height.subtract(pHeight)
                refHole = afeeder.getReferenceHoleLocation()
                if refHole is not None:
                    numChanged += 1
                    newHole = Location(refHole.getUnits(), refHole.getX(), refHole.getY(), 0, 0)
                    newZ = Location(feederHeight.getUnits(), 0, 0, feederHeight.getValue(), 0)
                    newHole = newHole.add(newZ)
                    print("Setting ref hole for %s to %s" % (afeeder.getName(), str(newHole)))
                    afeeder.setReferenceHoleLocation(newHole)
    print("Number feeders affected: %i" % numChanged)
    gui.getFeedersTab().repaint()
    psypnp.showMessage("Set level Z for %i feeders" % numChanged)



main()
