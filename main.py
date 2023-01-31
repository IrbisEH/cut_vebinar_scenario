import os
from pathlib import Path


DIR = os.path.dirname(__file__)

current_work_dir_name = '23-01-2023'
work_dir_path = os.path.join(DIR, current_work_dir_name)

cut_time_file_extension = '.txt'
scenario_file_extension = '.csv'

cut_time_file_path = '/Users/evgenijhristenko/Desktop/cut_scenario/23-01-2023/1 часть тайминг обрезки.txt'
scenario_file_path = '/Users/evgenijhristenko/Desktop/cut_scenario/23-01-2023/scenario_export_1213870.csv'

output_file_path = os.path.join(DIR, current_work_dir_name, f'new_{Path(scenario_file_path).name}')


def convert_in_sec(hours, minutes, seconds):
    return int(seconds) + (int(minutes) * 60) + (int(hours) * 60 * 60)


cut_time_file = open(cut_time_file_path, 'r')
lines = cut_time_file.read().splitlines()
cut_time_file.close()
cut_time_values = [i.split(' - ') for i in lines]
cut_time_values_sec = []        # список катов
for value in cut_time_values:
    time_from, time_to = [i.split('.') for i in value]
    time_from_sec = convert_in_sec(time_from[0], time_from[1], time_from[2])
    time_to_sec = convert_in_sec(time_to[0], time_to[1], time_to[2])
    cut_time_values_sec.append([time_from_sec, time_to_sec])

# проверка
print(f'______________ CHECK_1 ______________')
if len(cut_time_values) == len(cut_time_values_sec):
    print(f'После обработки осталось такое же количество отрезков: {len(cut_time_values_sec)}')
for i in range(len(cut_time_values_sec)):
    print(f'ч.м.с {cut_time_values[i]} | сек {cut_time_values_sec[i]}')

# читаем файл сценария
scenario_file = open(scenario_file_path, 'r', encoding='utf-8-sig')
lines = scenario_file.read().splitlines()
scenario_file.close()
scenario_values = []
for line in lines:
    line = line.split(';')
    line[0] = int(line[0])
    scenario_values.append(line)

# проверка
print(f'______________ CHECK_2 ______________')
count_offset = 0
for segment in cut_time_values_sec:
    offset = segment[1] - segment[0]
    count_offset += offset
print(f'Итоговое смещение в сек: {count_offset}')


time_offset = 0
for segment in cut_time_values_sec:
    start_cut = segment[0] - time_offset
    stop_cut = segment[1] - time_offset
    for value in scenario_values:
        comment_sec = value[0]
        if comment_sec < start_cut:
            pass
        elif start_cut <= comment_sec <= stop_cut:
            value[1] = 'delete'
        elif comment_sec > stop_cut:
            offset = stop_cut - start_cut
            comment_sec -= offset
            value[0] = comment_sec

    time_offset = stop_cut - start_cut

output_scenario_values = [i for i in scenario_values if i[1] != 'delete']
output_scenario_values.sort()

output_file = open(output_file_path, 'w', encoding='utf-8-sig')
for value in output_scenario_values:
    value = [str(i) for i in value]
    output_file.write(f'{";".join(value)}\n')
output_file.close()
