'''

Move the nozzle by this (relative) amount.

Will only move things if 
  psypnp.should_proceed_with_motion
says we're good to go.

@see: https://inductive-kickback.com/2020/10/psypnp-for-openpnp/


@author: Pat Deegan
@copyright: Copyright (C) 2020 Pat Deegan, https://psychogenic.com
@license: GPL version 3, see LICENSE file for details.

'''

############## BOILER PLATE #################

# submitUiMachineTask should be used for all code that interacts
# with the machine. It guarantees that operations happen in the
# correct order, and that the user is presented with a dialog
# if there is an error.
from org.openpnp.util.UiUtils import submitUiMachineTask


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

#from __future__ import absolute_import, division
from org.openpnp.util import MovableUtils
from org.openpnp.model import LengthUnit, Location
from org.openpnp.model.Motion import MotionOption
import psypnp
import psypnp.ui




def main():
    if psypnp.should_proceed_with_motion():
        submitUiMachineTask(go_nozz)


def go_nozz():
    
    if machine.defaultHead is None:
        # too weird
        return # should error
    
    defNozz = machine.defaultHead.getDefaultNozzle()
    if defNozz is None:
        return # should error
    
    loc = get_coords(defNozz)
    if loc is None:
        # cancel
        return
        
    MovableUtils.moveToLocationAtSafeZ(defNozz, loc)
    #machine.defaultHead.moveToSafeZ()
    # machine.defaultHead.defaultCamera.moveTo(loc)


def get_coords(nozz):
    curloc = nozz.location
    xval = psypnp.ui.getUserInputFloat("X", 0)
    if xval is None:
        # cancel
        return None
    yval = psypnp.ui.getUserInputFloat("Y", 0)
    if yval is None:
        # cancel
        return None
    try:
        xval = float(xval)
    except:
        xval = 0

    try:
        yval = float(yval)
    except:
        yval = 0


    location = curloc.add(Location(LengthUnit.Millimeters, xval, yval, 0, 0))
    return location

main()
