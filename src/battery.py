#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2023 Thomas Harr <xDevThomas@gmail.com>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2023-01-03
#


import json
import os
import shutil
import subprocess
import sys
import tempfile

from workflow import Workflow
from workflow.util import run_command

# GitHub repo for self-updating
UPDATE_SETTINGS = {'github_slug': 'harrtho/alfred-battery'}

# GitHub Issues
HELP_URL = 'https://github.com/harrtho/alfred-battery/issues'

# Icon shown if a newer version is available
ICON_UPDATE = 'icons/update.png'
ICON_ERROR = 'icons/error.png'
ICON_CHARGING = 'icons//charging.png'
ICON_POWER = 'icons/power.png'
ICON_FULL = 'icons/full.png'
ICON_MEDIUM = 'icons/medium.png'
ICON_LOW = 'icons/low.png'
ICON_CRITICAL = 'icons/critical.png'
ICON_CLOCK = 'icons/clock.png'
ICON_TEMP = 'icons/temp.png'
ICON_CYCLES = 'icons/cycles.png'
ICON_HEALTH = 'icons/health.png'
ICON_SERIAL = 'icons/serial.png'


def battery_info_program():
    """Return path to BateryInfo executable.

    Returns:
        str: Path to ``BatteryInfo`` executable.
    """
    return wf.cachefile('BatteryInfo')


def battery_info_check_update():

    key = '__battery_info_update'
    # Cache that a workflow update is available. This will lead to a BatteryInfo update
    if wf.update_available:
        status = wf.cache_data(key, {
            'available': True,
            'version' : wf.version
        })
        return False

    status = wf.cached_data(key, max_age=0)
    if not status or not status.get('available'):
        return False

    return True


def install_battery_info():
    bi = battery_info_program()
    if os.path.exists(bi):
        os.unlink(bi)

    tempdir = tempfile.mkdtemp(prefix='aw-', dir=wf.cachedir)

    try:
        os.chdir(tempdir)
        source_code = os.path.join(wf.workflowdir, 'BatteryInfo.swift')
        binary_src = os.path.join(tempdir, 'BatteryInfo')
        binary_dest = os.path.join(wf.cachedir, 'BatteryInfo')

        cmd = [
            'swiftc',
            source_code]

        retcode = subprocess.call(cmd)
        if retcode != 0:
            raise RuntimeError(f'BatteryInfo compilation exited with {retcode}')

        if not os.path.exists(binary_src):  # pragma: nocover
            raise ValueError(f'Compiled BatteryInfo file not found: {binary_src}')

        shutil.move(binary_src, binary_dest)

        if not os.path.exists(binary_dest):  # pragma: nocover
            raise ValueError(f'Compiled BatteryInfo file not found: {binary_src}')

    finally:
        os.chdir(wf.workflowdir)

        try:
            shutil.rmtree(tempdir)
        except OSError:  # pragma: no cover
            pass

    # Update successfully
    wf.cache_data('__battery_info_update', {
            'available': False,
            'version' : wf.version
        })


def convert_battery_info(info):
  try:
    return True, json.loads(info)
  except ValueError as e:
    return False, None


def get_battery_info() -> tuple[bool, dict | str]:
    """Get the system battery inforamtion from your laptop

    Returns:
        tuple[bool, dict | str]: In case of success True and the battery info
            otherwiese False and None
    """
    bi = battery_info_program()

    # Install if BatteryInfo does not exist
    if (not os.path.exists(bi)) or battery_info_check_update():
        install_battery_info()


    output = run_command([bi]).decode('utf-8')
    return convert_battery_info(output)


def show_error(battery_err):
    wf.add_item(title='Retrieved an error',
            subtitle=battery_err,
            valid=False,
            icon=ICON_ERROR
        )


def show_info(battery_info):
    raw_current_capacity = battery_info['AppleRawCurrentCapacity']
    raw_max_capacity = battery_info['AppleRawMaxCapacity']
    design_capacity = battery_info['DesignCapacity']
    charge = round(raw_current_capacity * 100 / raw_max_capacity, 2)
    loaded = '●' * round(charge/10)
    unloaded = '○' * round(10-charge/10)
    cells = f'{loaded}{unloaded}'
    status_info = 'Draining...'
    charging = battery_info['IsCharging']
    time_to_empty = battery_info['AvgTimeToEmpty']
    time_to_full = battery_info['AvgTimeToFull']
    time_left = 'Calculating…'
    time_full = 'Calculating…'
    fully_charged = battery_info['FullyCharged']
    external = battery_info['ExternalConnected']

    if time_to_empty < 15000:
        time_left = f'{round(time_to_empty/60)}:{round(time_to_empty%60)}'

    if time_to_full < 15000:
        time_full = f'{round(time_to_full/60)}:{round(time_to_full%60)}'

    if charging:
        time_info = f'{time_full} until full'
        status_info = 'Charging...'
        battery_icon = ICON_CHARGING
    else:
        if fully_charged:
            if external:
                time_info = 'On AC power'
                status_info = 'Fully Charged'
                battery_icon = ICON_POWER
                charge = '100'
                cells = '●●●●●●●●●●'
            else:
                time_info = time_left
                battery_icon = ICON_FULL
        else:
            time_info = time_left
            battery_icon = ICON_CRITICAL
            if charge > 80:
                battery_icon = ICON_FULL
            elif charge > 50:
                battery_icon = ICON_MEDIUM
            elif charge > 10:
                battery_icon = ICON_LOW

    temperature = round(battery_info['Temperature'] / 10 - 273, 2)
    cycle_count = battery_info['CycleCount']
    health = round(raw_max_capacity * 100 / design_capacity)
    serial = battery_info['Serial']

    wf.add_item(title=f'{charge}% {cells}',
            subtitle=status_info,
            valid=False,
            icon=battery_icon
        )
    wf.add_item(title=time_info,
        subtitle='Time Left',
        valid=False,
        icon=ICON_CLOCK
    )
    wf.add_item(title=f'{temperature} °C',
        subtitle='Temperature',
        valid=False,
        icon=ICON_TEMP
    )
    wf.add_item(title=cycle_count,
        subtitle='Charge Cycles Completed',
        valid=False,
        icon=ICON_CYCLES
    )
    wf.add_item(title=f'{health}%',
        subtitle='Health',
        valid=False,
        icon=ICON_HEALTH
    )
    wf.add_item(title=serial,
        subtitle='Serial',
        valid=False,
        icon=ICON_SERIAL
    )


def run():
    """Get the system battery inforamtion from your laptop

    Returns:
        int: The Exit status.

    """
    valid, battery_info = get_battery_info()

    if not valid:
        show_error(battery_info)
    else:
        show_info(battery_info)

    wf.send_feedback()
    return 0


def main(wf):
    """Run the the main workflow logic

    Args:
        wf (Workflow): The Alfred-PyWorkflow instance

    """

    # Notify user if update is available
    # ------------------------------------------------------------------
    if wf.update_available:
        battery_info_check_update()
        wf.add_item('Workflow Update is Available',
                    '↩ or ⇥ to install',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=ICON_UPDATE)


    return run()


if __name__ == '__main__':
    wf = Workflow(update_settings=UPDATE_SETTINGS,
                  help_url=HELP_URL)
    log = wf.logger
    sys.exit(wf.run(main))
