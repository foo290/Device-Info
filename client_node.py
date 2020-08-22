import psutil
import re
import uuid
import platform
import socket
import geocoder
import time
import nvgpu
import json
from psutil._common import bytes2human


location_iteration = 0
active_var = 0
sysInfoDir = 'System_information.json'
locInfoDir = 'Location.json'


def bytes_to_gigs(nt):
    dic = {}
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        dic[name.capitalize()] = value
    return dic


def get_location():
    """
    Returns the location information of the device : if connected to internet, else try for 20 times with 2 seconds
    of interval to wait for internet.
    """

    global location_iteration
    location_info = {}
    try:
        while 1:
            loc = geocoder.ip('me')

            if loc.status_code == 200:
                lat, lang = loc.latlng
                location_info['Latitude'] = lat
                location_info['Longitude'] = lang
                location_info['City'] = loc.city
                location_info['Postal Code'] = loc.postal
                location_info['Country'] = loc.country
                location_info['State'] = loc.state
                return location_info
            else:
                if location_iteration < 20:
                    time.sleep(2)
                else:
                    return location_info
            location_iteration += 1
    except:
        pass


def get_sys_details():
    """ Get every owns of device information and returns a dict """

    try:
        cpu_info = {}
        os_info = {}
        network_info = {}
        system_info = {}
        battery_info = {}
        disc_partition_info = {}
        partition_storage = {}
        gpu_info = nvgpu.gpu_info()[0]

        if not gpu_info:
            gpu_info = {}

        os_info['platform'] = platform.system()
        os_info['platform-release'] = platform.release()
        os_info['Operating System'] = f'{platform.system()} {platform.release()}'
        os_info['platform-version'] = platform.version()
        system_info['Architecture'] = platform.machine()
        network_info['hostname'] = socket.gethostname()
        network_info['IP-address'] = socket.gethostbyname(socket.gethostname())
        system_info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        cpu_info['processor'] = platform.processor()
        cpu_info['Cores'] = psutil.cpu_count()
        cpu_info['Frequency - Current (MHz)'] = psutil.cpu_freq().current
        cpu_info['Frequency - Minimum (MHz)'] = psutil.cpu_freq().min
        cpu_info['Frequency - Maximum (MHz)'] = psutil.cpu_freq().max

        """ Battery Status """
        battry_obj = psutil.sensors_battery()
        battery_info['Percent'] = battry_obj.percent

        if battry_obj.secsleft != psutil.POWER_TIME_UNLIMITED and battry_obj.secsleft != psutil.POWER_TIME_UNKNOWN:
            total_seconds = battry_obj.secsleft
            hours = total_seconds // 3600
            total_seconds %= 3600
            minutes = total_seconds // 60
            battery_info['Time Left'] = f'{hours} Hours, {minutes} Minutes (approx)'
        elif battry_obj.secsleft == psutil.POWER_TIME_UNLIMITED:
            battery_info['Time Left'] = 'N/A -- Plugged In'
        elif battry_obj.secsleft == psutil.POWER_TIME_UNKNOWN:
            battry_obj['Time Left'] = 'N/A -- Battery Not Available'
        else:
            battry_obj['Time Left'] = 'N/A -- Unknown'
        battery_info['Power Plugged'] = battry_obj.power_plugged

        """ Memory (RAM) """
        ram_info = bytes_to_gigs(psutil.virtual_memory())

        """ Disc """
        partitions_list = psutil.disk_partitions()
        for partitions in partitions_list:
            temp = []
            for each in partitions:
                temp.append(each)
            disc_partition_info[partitions.device] = temp
            partition_storage[partitions.device] = bytes_to_gigs(psutil.disk_usage(partitions.device))

        dic_list = [network_info, os_info, system_info, cpu_info, gpu_info, battery_info, ram_info, disc_partition_info,
                    partition_storage]
        dic_label = 'Network info,OS Info,System Info,CPU Info,GPU Info,Battery Info,RAM Info,Disc Info,Partition Info'.split(
            ',')

        return {label: val for label, val in zip(dic_label, dic_list)}

    except:
        pass


def save_host_data():
    """
    Creates two json files in CWD : one for device information and second for location information.
    Location file might be saved after 40 seconds if device is not connected to internet.
    """

    sys_info = get_sys_details()
    with open(sysInfoDir, 'w') as f:
        json.dump(sys_info, f, indent=4)

    location_information = get_location()

    with open(locInfoDir, 'w') as file:
        if location_information:
            json.dump(location_information, file, indent=4)
        else:
            loc_not_found = {}
            json.dump(loc_not_found, file, indent=4)


save_host_data()
