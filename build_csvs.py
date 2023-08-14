#
# Example usage:  python build_csvs.py -f verde1.txt 
#

import getopt, sys
import ctypes
import pandas as pd

ACCEL_UUID = "c4c1f6e2-4be5-11e5-885d-feff819cdc9f"
GYRO_UUID = "b7c4b694-bee3-45dd-ba9f-f3b5e994f49a"

## Get csv filename
arg_list = sys.argv[1:]

short_options = "f:o:"
long_options = ["file=", "output="]


def get_timestamp_and_val(line):
  line_s = line.split()

  timestamp = line_s[1]
  val = line_s[-1]

  return timestamp, val

def hex_str_to_axis_int(hex):
  hex_s = hex.split('-')

  x = ctypes.c_int16(int(f"{hex_s[1]}{hex_s[0]}", 16)).value
  y = ctypes.c_int16(int(f"{hex_s[3]}{hex_s[2]}", 16)).value
  z = ctypes.c_int16(int(f"{hex_s[5]}{hex_s[4]}", 16)).value

  return x, y, z

try:

  args, _ = getopt.getopt(arg_list, short_options, long_options)

  accel_list = []
  gyro_list = []

  filename = args[0][1]
  output = args[1][1]

  try:
    with open(filename) as f:
      for line in f:

        if f"Notification received from {ACCEL_UUID}" in line:
          timestamp, accel_val = get_timestamp_and_val(line)
          x, y, z = hex_str_to_axis_int(accel_val)
          accel_list.append({"timestamp": timestamp,
                            "accx": x/1000,
                            "accy": y/1000,
                            "accz": z/1000})

        if f"Notification received from {GYRO_UUID}" in line:
          timestamp, gyro_val = get_timestamp_and_val(line)
          x, y, z = hex_str_to_axis_int(gyro_val)
          gyro_list.append({"timestamp": timestamp,
                            "gyrx": x/100,
                            "gyry": y/100,
                            "gyrz": z/100})

        

  except IOError as e:
    print(str(e))

  # Save csvs
  accel_csv = pd.DataFrame.from_records(accel_list)
  gyro_csv = pd.DataFrame.from_records(gyro_list)

  accel_csv.to_csv(f"{output}.csv", index=False)
  gyro_csv.to_csv('gyro.csv', index=False)


except getopt.error as e:
  print(str(e))
