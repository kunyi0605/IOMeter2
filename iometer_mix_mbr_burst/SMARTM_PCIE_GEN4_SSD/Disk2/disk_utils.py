import subprocess
def find_ssd(field = ["Model","DeviceID","Size","SerialNumber"]):
    SSD_MODEL_PREFIX = "LITEON"
    nvme_disks = msft_disk_query_disk()
    if len(nvme_disks) > 0:
        SSD_MODEL_PREFIX = nvme_disks[0]["Model"]
    elif "SSD_MODEL" in environ and environ["SSD_MODEL"] != "":
        SSD_MODEL_PREFIX = environ["SSD_MODEL"]
    
    condition = {
        "Model": {
            "Value": SSD_MODEL_PREFIX,
            "Type": "INCLUDE",
        }
    }
    disks = diskdrive_query_disk(condition, field)
    if len(disks) == 0:
        return None

    for disk in disks:
        disk["DeviceID"] = disk["DeviceID"].replace("\\\\.\\PHYSICALDRIVE", "")
    return disks[0]


def diskdrive_query_disk(condition_dict = {}, return_value= []):
    found_disk = wimc_query(['diskdrive'], condition_dict, return_value)
    return found_disk

def msft_disk_query_disk(condition_dict = { "BusType": {"Value": "17", "Type": "FULL"} }, return_value=["Model"]):
    found_disk = wimc_query(['/namespace:\\\\root\microsoft\windows\storage', 'path', 'msft_disk'], condition_dict, return_value)
    return found_disk

def wimc_query(query = [], condition_dict = {}, return_value = []):
    require_field = condition_dict.keys() + return_value
    require_field = list(require_field)
    command = ["wmic"] + query + ["get", ",".join(require_field), "/format:csv"]
    outputs = subprocess.check_output(command).split("\r\r\n")[1:]
    output_header = outputs[0].split(",")
    output_body = outputs[1:-1]

    accept_line = []
    for output_line in output_body:
        output_array = output_line.split(",")
        fail = False
        for condition_key in condition_dict:
            output_value = output_array[output_header.index(condition_key)]
            judge_value = condition_dict[condition_key]["Value"]
            judge_type = condition_dict[condition_key]["Type"]

            if judge_type == "FULL":
                if judge_value != output_value:
                    fail = True
            else:
                if judge_value not in output_value:
                    fail = True
        if fail:
            continue
        else:
            accept_line.append(output_line)

    accept_line = map(lambda x: format_wmic_csv(x, output_header), accept_line)
    
    return accept_line

def format_wmic_csv(data, header):
    dict_data = {}
    data = data.split(",")
    for index, val in enumerate(data):
        dict_data[header[index]] = val
    return dict_data
