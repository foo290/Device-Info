# Device-Info
A simple script to get Device Info and current location

### Intro
This is a simple script to extract device and location information and saves it in json files.

### Requirements
```
psutil
re
uuid
platform
socket
geocoder
time
nvgpu
json
```

### Execution
```
>>> python client_node.py
```

### Output
System_information.json
```
{
    "Network info": {
        "hostname": host name here...
        "IP-address": ip address...
    },
    "OS Info": {
        "platform": ...
        "platform-release": ...
        "Operating System": ...
        "platform-version": ...
    },
    "Partition Info": {
        "C:\\": {
            "Total": ...,
            "Used": ...,
            "Free": ....
            "Percent": ...
        }

    more...

```

Location.json
```
{
    "Latitude": ...
    "Longitude": ...
    "City": ...,
    "Postal Code": ...
    "Country": ...
    "State": ...
}
```

##### Location file may take 40 seconds to be saved if you are not connected to internet. <hr>
😀
