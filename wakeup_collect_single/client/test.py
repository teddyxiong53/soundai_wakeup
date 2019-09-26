import csv

def create_csv(path):
    with open(path, "w+", newline='') as file:
        csv_file = csv.writer(file)
        head = ["name","sex"]
        csv_file.writerow(head)

def append_csv(path):
    with open(path, "a+", newline='') as file: # 处理csv读写时不同换行符  linux:\n    windows:\r\n    mac:\r
        csv_file = csv.writer(file)
        datas = [["hoojjack", "boy"], ["hoojjack1", "boy"]]
        csv_file.writerows(datas)


def read_csv(path):
    with open(path,"r+") as file:
        csv_file = csv.reader(file)
        for data in csv_file:
            print("data:", data)
def main():
    path = "example.csv"
    create_csv(path)
    append_csv(path)
    read_csv(path)

if __name__ == "__main__":
    main()
