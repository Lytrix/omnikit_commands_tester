import re
import requests
from datetime import datetime


def get_times_units(rawgit_page_pdm_values):
    markdown_page = requests.get(rawgit_page_pdm_values)
    #print(markdown_page)
    input_data_text = markdown_page.text
    #print(input_data_text)
    regex_basal_schedules = r'\#\#\ (.*)\]*\n\s([\*\s\d:\-\.\:\n]*)\n'
    basal_schedules = re.finditer(regex_basal_schedules, input_data_text)

    for matchNum, match in enumerate(basal_schedules):
        matchNum = matchNum + 1
        # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

        print("log.info(\"",match.group(1),"\")")
        print(suspend_command)
        print("let basalSchedule{} = BasalSchedule(entries: [".format(matchNum))
        # Get separate values
        regex_times_and_units = r'\*\s*([\d:]+)\s*-\s*([\d:]+)\s*([\d.]+)'
        entry = re.finditer(regex_times_and_units, match.group(2))
        for values in entry:
            start_time = values.group(1)
            end_time = values.group(2)
            units = values.group(3)
            # print(start_time, end_time, units)
            entry_command = fill_basal_entry(units, start_time, end_time)
            print(entry_command)
        print("""])
let scheduleOffset{0} = podState.timeZone.scheduleOffset(forDate: Date())
try setBasalSchedule(schedule: basalSchedule{0}, scheduleOffset: scheduleOffset{0}, confidenceReminder: false, programReminderInterval: .minutes(0))
sleep(5)""".format(matchNum))


def get_pdm_recordings(rawgit_page_pdm_values):
    markdown_page = requests.get(rawgit_page_pdm_values)
    input_data_text = markdown_page.text
    temp_basals_pdm = re.search(r"\* (.*) ", input_data_text, re.S).group(1)
    return data


def fill_basal_entry(units, start_time, end_time):
    if end_time == '24:00':
        end_time = '00:00'
    FMT = '%H:%M'
    duration = datetime.strptime(start_time, FMT) - datetime.strptime('00:00', FMT)
    entry = """      BasalScheduleEntry(rate: {}, startTime: .hours({})),""".format(units, duration.seconds/3600)
    return entry

suspend_command = """try cancelDelivery(deliveryType: .all, beepType: .bipBip)
sleep(5)
"""


def main():
    basal_captures_wikipage = "https://raw.githubusercontent.com/wiki/openaps/openomni/Basal-Schedule-captures.md"
    get_times_units(basal_captures_wikipage)


if __name__ == '__main__':
    main()
