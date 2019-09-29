lines_seen = set()
in_file = open('./info.csv', 'r')
out_file = open('./info_out.csv', 'w+')
lines = in_file.readlines()
for line in lines:
    if line not in lines_seen:
        out_file.write(line)
        lines_seen.add(line)

in_file.close()
out_file.close()

