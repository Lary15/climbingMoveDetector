import os, time
import getopt, sys
import matplotlib
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd

os.environ['TZ'] = 'Brazil/East'
time.tzset()


def get_moves(filename):
  moves = []

  with open(filename) as f:

    dic = { "start": None, "end": None }
    
    for line in f:
      time = line.split()[0]
     
      if dic["start"] == None:
        dic["start"] = pd.Timestamp(time[::-1].replace(":",".",1)[::-1])
      else:
        dic["end"] = pd.Timestamp(time[::-1].replace(":",".",1)[::-1])
        moves.append(dic)
        dic = { "start": None, "end": None }

  return pd.DataFrame.from_records(moves)


def build_graph(moves=None):

  plt.figure(figsize=(12, 8))

  axis_labels = {
    "accx": "Aceleração no eixo X",
    "accy": "Aceleração no eixo Y",
    "accz": "Aceleração no eixo Z",
  }


  for axis in ["accx", "accy", "accz"]:
    plt.clf()

    # Set time formatter
    fmt = matplotlib.dates.DateFormatter('%H:%M:%S')
    plt.gca().xaxis.set_major_formatter(fmt)

    plt.plot(df.timestamp, df[axis], color="blue", linewidth=1)

    if moves is not None:
      # shift moves to start at the same time as the data
      t = df.timestamp.iloc[0]
      delta = pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

      m = moves.copy()
      m.start += delta
      m.end += delta

      for _, move in m.iterrows():
        plt.axvspan(move.start, move.end, color='green', alpha=0.3)

    # Add title and labels
    plt.title(axis_labels[axis], fontsize=16)
    plt.xlabel('Hora')
    plt.ylabel('Aceleração')

    # Add legend
    plt.grid()
    plt.legend()

    # Auto space
    plt.tight_layout()

    # Display plot
    plt.savefig(f"imgs/{axis}")



def build_mag_graph(moves=None):

  df["mag"] = np.sqrt(df["accx"]**2 + df["accy"]**2 + df["accz"]**2)

  plt.figure(figsize=(12, 8))

  plt.clf()

  # Set time formatter
  fmt = matplotlib.dates.DateFormatter('%H:%M:%S')
  plt.gca().xaxis.set_major_formatter(fmt)

  plt.plot(df.timestamp, df.mag, color="blue", linewidth=1)

  if moves is not None:
    # shift moves to start at the same time as the data
    t = df.timestamp.iloc[0]
    delta = pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

    m = moves.copy()
    m.start += delta
    m.end += delta

    for _, move in m.iterrows():
      plt.axvspan(move.start, move.end, color='green', alpha=0.3)

  # Add title and labels
  plt.title("Magnitude da aceleração", fontsize=16)
  plt.xlabel('Hora')
  plt.ylabel('Aceleração')

  # Add legend
  plt.grid()
  plt.legend()

  # Auto space
  plt.tight_layout()

  # Display plot
  plt.savefig(f"imgs/mag")


args = sys.argv[1:]

short_options = "f:s:e:m:"
long_options = ["file=", "start=", "end=", "moves="]

try:
  args, _ = getopt.getopt(args, short_options, long_options)
  filename = args[0][1]

  df = pd.read_csv(filename, parse_dates=["timestamp"], date_parser=pd.Timestamp)

  if len(args) >= 3:
    start = args[1][1]
    end = args[2][1]

    df = df[(df.timestamp >= start) & (df.timestamp <= end)]

  moves = None
  if len(args) >= 4:
    moves_filename = args[3][1]
    moves = get_moves(moves_filename)

  build_graph(moves)
  build_mag_graph(moves)

except getopt.GetoptError as e:
  print(str(e))