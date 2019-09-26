import csv
import os, sys
g_csv_filename = '1.csv'
g_f = None
if not os.path.exists(g_csv_filename):
    print("{} not exists".format(g_csv_filename))
    g_f = open(g_csv_filename, 'rw')
    
    g_f.close()

g_f = open(g_csv_filename, 'w')



f_csv = csv.writer(f)
