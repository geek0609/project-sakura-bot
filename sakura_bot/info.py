import requests
import json
import texts


def get_device_info(device):
    request = requests.get("https://raw.githubusercontent.com/ProjectSakura/OTA/11/website/" + device + ".json")
    print("https://raw.githubusercontent.com/ProjectSakura/OTA/11/website/" + device + ".json")
    print(request.content)
    if not request.ok:
        return False
    converted = json.loads(request.content)
    required = converted['response'][0]
    request = requests.get("https://raw.githubusercontent.com/ProjectSakura/OTA/11/devices.json")
    json_processed = json.loads(request.content)
    name = "Error: Could not find name"
    brand = "Error: Could not find brand"
    maintainer = "Error: Could not find maintainer"
    active = False

    # To avoid warning like these
    # "Local variable 'maintainer' might be referenced before assignment"

    for devices in json_processed:
        if devices['codename'] == device:
            maintainer = devices['maintainer_name']
            name = devices['name']
            brand = devices['brand']
            active = devices["active"]

    if "VANILLA" in required['filename']:
        variant = "Vanilla"
    elif "GAPPS-Core" in required['filename']:
        variant = "GApps Core"
    elif "GAPPS-Basic" in required['filename']:
        variant = "GApps Basic"
    elif "microg" in required['filename'].lower():
        variant = "MicroG"
    else:
        variant = "GApps"

    if required['updater']:
        notes = "✅ OTA has been pushed; Clean flash not mandatory"
    else:
        notes = "❎ OTA not pushed; Clean flash mandatory"

    print("Device is : " + device)
    print("Size is : " + str(required['size']))
    print("Maintained by : " + maintainer)
    print("File name : " + required['filename'])
    print("Version : " + required['version'])
    print("Variant : " + variant)
    print("Notes : " + notes)

    return {
        "device": device,
        "size": str(required['size']),
        "maintainer": maintainer,
        "variant": variant,
        "version": required['version'],
        'name': name,
        "brand": brand,
        "notes": notes,
        "time": required['datetime'],
        "filename": required['filename'],
        "id": required['id'],
        "romtype": required['romtype'],
        "url": required['url'],
        "updater": required['updater'],
        "active": active
    }


def cook_content(information):
    if not information:
        return "Device not found, make sure you are typing the correct codename (case sensitive), you can do /list to find out the codename. See /help for more"

    if information["active"]:
        active_status = "✅ This device is currently <b>officially supported</b>"
    else:
        active_status = "❎ This device is <b>not currently officially supported</b>\nIf you wish to maintain " \
                        "Project Sakura for this device, see " + texts.link("https://projectsakura.xyz/wiki/#/apply",
                                                                            "our official wiki")

    message = \
        "Latest" + texts.bold(" Project Sakura ", "") + "for " + information['name'] + " (" + str(
            information['device']) + ")\n" + \
        "👤 " + texts.bold("by ", str(information["maintainer"])) + "\n" + \
        "ℹ️ " + texts.bold("Version : ", str(information['version'])) + "\n" + \
        "❕ " + texts.bold("Variant: ", str(information["variant"])) + "\n" + \
        "⬇️ " + texts.bold(texts.link("https://projectsakura.xyz/download/#/" + information['device'],
                                      "Download"), "") + "\n\n" + active_status

    return message
