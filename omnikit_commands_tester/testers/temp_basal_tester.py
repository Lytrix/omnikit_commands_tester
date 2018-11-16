import re
import pathlib
import requests
import logging

logger = logging.getLogger(__name__)


def get_raw_temp_basals_rtlomni(rtlomni_log_text):
    commands = []
    #regex = r"BODY:([0-9A-Za-z]+)\s.*\n*.*\n*.*\n*.*\n*CON:([A-Za-z0-9]+)\s"
    regex = r"(.*)\sID1.*BODY:([0-9A-Za-z]*).*\n.*\n.*CON:([A-Za-z0-9]+)*\s"
    select = re.findall(regex, rtlomni_log_text)
    for line in select:
        time = ' '.join(line[0][:-4].split('T'))
        string = "{}{}".format(line[1], line[2])
        raw_value = ''.join(map(str, string))
        commands.append({"time": time, "raw_value": raw_value})
    return commands


def get_raw_temp_basals_xcode(xcode_log_text):
    """
    Args:
        - xcode_log_text: raw xcode logs as a string
        - command: message type in lowercase, like:  '1a', '1f'
        - command_extra: message type in lowercase, like '13, '16', '17'
    Result:
        returns a list of all raw hex commands
    """
    commands = []
    regex = r"Send\(Hex\): .{0,12}(.*)\n([0-9-:\s]*)"
    select_1a_commands = re.findall(regex, xcode_log_text, re.MULTILINE)
    for line in select_1a_commands:
        commands.append({"time": line[1], "raw_value": line[0]})
        # print(line)
    return commands


def reformat_raw_hex(commands_list, command_type, extra_command_type):
    print("List of commands:")
    commands = []

    for line in commands_list:
        #print(line)
        time = line['time']
        raw_value = line['raw_value']

        if raw_value[:2] == command_type and raw_value[32:34] == extra_command_type:
            raw_value = ''.join(map(str, raw_value))

            if raw_value[40:44]:
                units = "{0:.2f}".format(int(raw_value[40:44], 16)/100)
            else:
                units = ""

            command_elements = [
                #command_type,
                time,
                "",
                units,
                " 0.5h",
                raw_value[0:2],
                raw_value[2:4],
                raw_value[4:12],
                raw_value[12:14],
                raw_value[14:18],
                raw_value[18:20],
                raw_value[20:24],
                raw_value[24:28],
                raw_value[28:32],
                raw_value[32:34],
                raw_value[34:36],
                raw_value[36:38],
                raw_value[38:40],
                raw_value[40:44],
                raw_value[44:52],
                raw_value[52:56],
                raw_value[56:64]]
            command = ' '.join(command_elements)
            #print(command)
            commands.append(command)
    return commands


def match_temp_basals_pdm(commands, rawgit_page_pdm_values):
    """
    Args:
        - commands: list of raw hex temp basal commands
        - filename_pdm_values: text file with a list of all temp basal values, spaced as on the openomni wiki
    Result:
        printed mismatched temp basals Loop vs PDM
    """
    output = {"total_results": '', "results": []}
    tested_results = []
    markdown_page = requests.get(rawgit_page_pdm_values)
    input_data_text = markdown_page.text
    temp_basals_pdm = re.search(r"```(.*)```", input_data_text, re.DOTALL).group(1)
    pdm_values = temp_basals_pdm.split('\n')
    mismatch = 0
    for i, command in enumerate(commands):
        for line in pdm_values:
            # Replace reminders by 00 to match Loop
            if line[59:61] != '00':
                    line = line[:59] + '00' + line[61:]
            error = ''
            unit_rate_pdm = line[:5].strip()
            unit_rate_loop = command[20:25].strip() # command[12:18].strip()
            if unit_rate_loop == unit_rate_pdm:
                pre_name = "PDM................"
                pdm = pre_name + line
                # test after the nonce
                if command[47:].strip() == line[27:].strip():
                    match = "Yes"
                    break
                if command[47:].strip() != line[27:].strip():
                    match = "No"
        tested_results.append({"pdm": pdm, "loop": command, "match": match})
        if match == "No":
                mismatch += 1
    if mismatch > 0:
        total_results = "Found {}mismatches".format(mismatch)
    else:
        total_results = "No Temp basal mismatches found"
    return {"total_results": total_results, "results": tested_results, "header":  "Day....... Time.... "+ pdm_values[1]}


def extractor(file):
    pdm_values_url = 'https://raw.githubusercontent.com/wiki/openaps/openomni/All-Temp-basal-units-for-0.5h.md'
    text=file.read().decode('utf-8')
    if pathlib.Path(file.name).suffix == '.omni':
        all_commands=get_raw_temp_basals_rtlomni(text)
    else:
        all_commands=get_raw_temp_basals_xcode(text)
    temp_basal_commands=reformat_raw_hex(all_commands, '1a', '16')

    matching_tempbasals = match_temp_basals_pdm(temp_basal_commands, pdm_values_url)
    return {"allcommands": temp_basal_commands, "matching_tempbasals": matching_tempbasals}