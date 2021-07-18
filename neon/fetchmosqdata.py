import os
import csv


class Location():
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long


with open("neon_mos_data.csv", 'w') as neon_file:
    writer = csv.writer(neon_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['Site Name', 'Longitude', 'Latitude', 'Point Type', 'Date/Time', 'Plot ID']
    writer.writerow(header)
    directory_in_str = '/Users/sujayr/Downloads/NEON_count-mosquitoes'
    presCount = 0
    absCount = 0
    for file in os.listdir(directory_in_str):
        if (file.endswith("L") or file.endswith("1")):
            monthly_dir = directory_in_str + "/" + file
            for filename in os.listdir(monthly_dir):
                if ("mos_trapping" in filename):
                    with open(monthly_dir + '/' + filename) as csv_file:
                        reader = csv.reader(csv_file)
                        rowNbr = 0
                        for row in reader:
                            if rowNbr >= 1:
                                location = Location(row[7], row[8])
                                if "Y" in row[27]:
                                    writer.writerow([row[3], location.long, location.lat, 'Presence', row[14], row[4]])
                                    presCount = presCount + 1
                                else:
                                    writer.writerow([row[3], location.long, location.lat, 'Absence', row[14], row[4]])
                                    absCount = absCount+1
                            rowNbr = rowNbr + 1
        else:
            continue
print(presCount)
print(absCount)
