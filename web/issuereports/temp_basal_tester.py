import re
import pathlib
import requests
import argparse
from datetime import date


def parser():
    desc = 'Extract all 1a temp basal commands from Xcode logs and evaluate against PDM temp basals'
    parser = argparse.ArgumentParser(desc)
    parser.add_argument(
        'filename', type=str, help='filename to parse')
    parser.add_argument(
        'command_type', type=str, help='extra command to parse, for example basal, tempbasal')
    return parser


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


def get_raw_temp_basals_xcode(xcode_log_text, captureDate=date.today()):
    """
    Args:
        - xcode_log_text: raw xcode logs as a string
        - command: message type in lowercase, like:  '1a', '1f'
        - command_extra: message type in lowercase, like '13, '16', '17'
    Result:
        returns a list of all raw hex commands
    """
    commands = []

    if captureDate < date(2018, 11, 26):
        regex = r"Send\(Hex\): .{0,12}(.*)\n([0-9-:\s]*)"
        select_1a_commands = re.findall(regex, xcode_log_text, re.MULTILINE)
        for line in select_1a_commands:
            commands.append({"time": line[1], "raw_value": line[0]})
            print(line)
    else:
        regex = r"\* ([0-9-:\s]*)\s.*[send,receive]\s([a-z0-9]*)\n"
        select_1a_commands = re.findall(regex, xcode_log_text, re.MULTILINE)
        for line in select_1a_commands:
            commands.append({"time": line[0], "raw_value": line[1]})
            print(line)
    return commands


def reformat_raw_hex(commands_list, command_type, captureDate=date.today()):
    print("List of commands:")
    commands = []

    if command_type == "basal":
        basal = True
    if command_type == "tempbasal":
        basal = False

    print("Day        Time     1a LL NNNNNNNN 00 CCCC HH SSSS PPPP napp napp napp napp napp 13 LL RR MM NNNN XXXXXXXX YYYY ZZZZZZZZ YYYY ZZZZZZZZ YYYY ZZZZZZZZ")
    for line in commands_list:
        print(line)
        time = line['time']
        raw_value = line['raw_value']

        #if raw_value[:2] == command_type and raw_value[32:34] == extra_command_type:
        print(raw_value[12:14])
        if basal and raw_value[12:14] == '1a' and captureDate < date(2018, 11, 26):
            raw_value = ''.join(map(str, raw_value))
        elif basal and raw_value[12:14] == '1a':
            raw_value = raw_value[12:]
            raw_value = ''.join(map(str, raw_value))

            # 1a LL NNNNNNNN 00 CCCC HH SSSS PPPP napp napp napp 13 LL RR MM NNNN XXXXXXXX YYYY ZZZZZZZZ
            # 1a 12 b92270c2 00 06ba 29 10d8 0009 f01e f0 1e f0 1e 130e 40000762 004c 4b403840

            # if raw_value[40:44]:
            #    units = "{0:.2f}".format(int(raw_value[40:44], 16)/100)
            # else:
            #    units = ""
            command_elements = [
                #command_type,
                time,
                raw_value[0:2],    # 1a
                raw_value[2:4],    # LL
                raw_value[4:12],   # NNNNNNNN
                raw_value[12:14],  # 00
                raw_value[14:18],  # CCCC
                raw_value[18:20],  # HH
                raw_value[20:24],  # SSSS
                raw_value[24:28],  # PPPP
                raw_value[28:32],  # napp
                raw_value[32:36],  # napp
                raw_value[36:40],  # napp
                raw_value[40:44],  # napp
                raw_value[44:48],  # napp
                raw_value[48:50],  # 13
                raw_value[50:52],  # LL
                raw_value[52:54],  # RR
                raw_value[54:56],  # MM
                raw_value[56:60],  # NNNN
                raw_value[60:68],  # XXXXXXXX
                raw_value[68:72],  # YYYY
                raw_value[72:80],  # ZZZZZZZZ
                raw_value[80:84],  # YYYY
                raw_value[84:92],  # ZZZZZZZZ
                raw_value[92:96],  # YYYY
                raw_value[96:104],  # ZZZZZZZZ
                raw_value[104:108],  # YYYY
                raw_value[108:116]]  # ZZZZZZZZ
            command = ' '.join(command_elements)
            #print(command)
            commands.append(command)
        if basal == False and raw_value[12:14] == '1a':
            raw_value = raw_value[12:]
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
        #print(command)
        for line in pdm_values:
            #print(line)
            # Replace reminders by 00 to match Loop
            if line[59:61] != '00':
                    line = line[:59] + '00' + line[61:]
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
            else:
                pdm = "This unit value does not match any of the PDM values."
                match = "No"
        tested_results.append({"pdm": pdm, "loop": command, "match": match})
        print(pdm)
        print(command)
        print(match)
        if match == "No":
                mismatch += 1
    if mismatch > 0:
        total_results = "Found {} mismatches".format(mismatch)

    else:
        total_results = "No Temp basal mismatches found"
    print(total_results)
    return {"total_results": total_results, "results": tested_results, "header":  "Day....... Time.... "+ pdm_values[1]}


def extractor(file, command_type='tempbasal'):
    pdm_values_url = 'https://raw.githubusercontent.com/wiki/openaps/openomni/All-Temp-basal-units-for-0.5h.md'
    text=file.read().decode('utf-8')
    if pathlib.Path(file.name).suffix == '.omni':
        all_commands=get_raw_temp_basals_rtlomni(text)
    else:
        all_commands=get_raw_temp_basals_xcode(text)
    temp_basal_commands=reformat_raw_hex(all_commands, command_type)
    if command_type == 'tempbasal':
        matching_tempbasals = match_temp_basals_pdm(temp_basal_commands, pdm_values_url)
        return {"allcommands": temp_basal_commands, "matching_tempbasals": matching_tempbasals}


def main():
    args=parser().parse_args()
    with open(args.filename, 'rb') as input_file:
        output_json = extractor(input_file, args.command_type)


if __name__ == '__main__':
    main()
