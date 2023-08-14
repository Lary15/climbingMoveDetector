## COMAND LINES

### VIA VERDE
- python build_csvs.py -f verde1.txt -o accel_verde
- python make_graphs.py -f accel_verde.csv -s 11:10:00 -e 11:12:00

### VIA PRETA
- python build_csvs.py -f preta1_inclinada.txt -o accel_preta  
- python build_csvs.py -f preta1_inclinada.txt -o accel_preta

### BOULDER LARANJA
- python build_csvs.py -f verde1.txt -o accel_verde
- python make_graphs.py -f accel_verde.csv -s 11:10:00 -e 11:12:00

### BOULDER ROSA
- python build_csvs.py -f boulder_laranja.txt -o accel_verde
- python make_graphs.py -f accel_laranja.csv -s 11:29:54 -e 11:31:00 -m rosa_moves.txt
