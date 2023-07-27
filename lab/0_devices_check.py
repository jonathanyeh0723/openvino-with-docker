from openvino.runtime import Core


core = Core()
devices = core.available_devices
print("plugin | full_device_name")
for device in devices:
    full_device_name = core.get_property(device, "FULL_DEVICE_NAME")
    print(device + ":     " +  full_device_name)
