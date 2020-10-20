'''

Send the nozzle over to bottom cam's location.

Will only move things if 
  psypnp.should_proceed_with_motion
says we're good to go.

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


#from __future__ import absolute_import, division

from org.openpnp.model import Location
import psypnp



def main():
    if psypnp.should_proceed_with_motion():
        go_to_bottom()



def go_to_bottom():
    botcamloc = get_coords()
    if botcamloc is None:
        # cancel
        return
    # always safeZ
    machine.defaultHead.moveToSafeZ()
    # we don't want to go straight to the cam location--first XY, 
    # then Z
    safeMoveLocation = Location(botcamloc.getUnits(), botcamloc.getX(), botcamloc.getY(), 0, 0);
    machine.defaultHead.defaultNozzle.moveTo(safeMoveLocation)
    # our default z will be whatever the camera says
    noz = machine.getDefaultHead().getDefaultNozzle()
    finalLocation = botcamloc.add(Location(botcamloc.getUnits(), 0,0, botcamloc.getZ(), 0))
    if noz is not None:
        ntip = noz.getNozzleTip()
        if ntip is not None:
            ntipcalib = ntip.getCalibration()
            if ntipcalib is not None and ntipcalib.isEnabled():
                zoffset = ntipcalib.getCalibrationZOffset()
                if zoffset is not None:
                    finalLocation = botcamloc.add(Location(zoffset.getUnits(), 0, 0, zoffset.getValue(), 0))

    #print("WOULD LIKE TO MOVE TO %s" % str(finalLocation))
    machine.defaultHead.defaultNozzle.moveTo(finalLocation)


def get_coords():
    headcams = machine.defaultHead.getCameras()
    maccams = machine.getCameras()
    targetCam = None
    for acam in maccams:
        targetCam = acam
        for hcam in headcams:
            if targetCam is not None and hcam.getId() == targetCam.getId():
                # bottom cam is not on the head, kill this
                targetCam = None

    if targetCam is None:
        psypnp.showMessage("Could not find a camera not on defaultHead")
        return None

    return targetCam.getLocation()

main()
