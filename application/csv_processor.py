import csv
from min_heap import MinHeap
from binary_search import binary_search


# Standardized Address Data:
# ------------------------------------------------------------------------------------------------------------------------------------------
# line1 / line2 / city / state / postalcode / dnc / lang / locationType / latitude / longitude / sortOrder / hideOnMap / lastWorked / notes
# ------------------------------------------------------------------------------------------------------------------------------------------

# ////////// Storage //////////
# Storage for Poughkeepsie Structures Data
sorted = MinHeap()
sorted_addresses = []
# Storage for SOPO Territory Data
dncs = []
clean_addresses = []
territory_addresses = []

# Standardize Address Format
def standardize(address):
    dict = {"DR":"DRIVE", "LN":"LANE", "RD":"ROAD", "ST":"STREET", "AV":"AVENUE", "BLVD":"BOULEVARD", "CIR":"CIRCLE", "EXT":"EXTENSION", "HTS":"HEIGHTS", "JCT":"JUNCTION"}
    nsew = {"N":"NORTH", "S":"SOUTH", "E":"EAST", "W":"WEST"}

    split_address = address[0].split(" ")
    
    if split_address[-1] in dict.keys():
        split_address[-1] = dict[split_address[-1]]
    if split_address[1] in nsew.keys():
        split_address[1] = nsew[split_address[1]]

    address[0] = " ".join(split_address)
    return address


# ////////// Gather Territory Records Data //////////
filename = input("What file would you like to access?\n")
with open("input/" + str(filename), "r") as structures:

    reader = csv.reader(structures)

    addresses = []
    counter = 0
    for row in reader:
        item_list = []
        #print(row)
        for item in row:
            if item != '':
                item_list.append(item)
        addresses.append(item_list)
    #print(len(addresses))

    for element in addresses:
        if element == []:
            addresses.remove(element)

    index = 0
    for address in addresses:
        if address == ['Address', 'Name', 'Phone Numbers', 'Notes']:
            break
        index += 1
    
    dncs = addresses[5:index]
    clean_addresses = addresses[index + 1:]

    for address in clean_addresses:
        new_address = []
        for item in address:
            item = item.upper()
            new_address.append(item)
        territory_addresses.append(standardize(new_address))   


# print("Addresses", clean_addresses)


# ////////// Gather Poughkeepsie Structures Data //////////
with open("data/Poughkeepsie Structures.csv", "r") as structures:
    
    reader = csv.reader(structures)

    for line in reader:
        if line != ['OCC_CLS', 'PRIM_OCC', 'PROP_ADDR', 'PROP_CITY', 'PROP_ST', 'PROP_ZIP', 'LONGITUDE', 'LATITUDE']:
            sorted.add(line)

    while sorted.count > 0:
        sorted_addresses.append(sorted.retrieve_min())



# ////////// Data Comparison //////////
failed_searches = []
complete_addresses = []
for territory_address in territory_addresses:
    search = binary_search(sorted_addresses, territory_address[0])
    if search is None:
        failed_searches.append(territory_address)
    else:
        complete_addresses.append([territory_address[-1]] + search)

print("Failed Searches: ", failed_searches)
print("Completed Addresses:", complete_addresses)


# ////////// Write Data to Output CSV //////////
with open("output/output.csv", "w") as output:
    fieldnames = ["line1","line2","city","state","postalcode","dnc","lang","locationType","latitude","longitude","sortOrder","hideOnMap","lastWorked","notes"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for address in complete_addresses:
        line1 = address[3]
        line2 = ""
        city = address[4]
        state = address[5]
        postalcode = address[6]
        dnc = ""
        lang = ""
        locationType = str(address[1] + " / " + address[2])
        latitude = address[8]
        longitude = address[7]
        sortOrder = ""
        hideOnMap = ""
        lastWorked = ""
        notes = ""
    
        writer.writerow({"line1":line1, "line2":line2, "city":city, "state":state, "postalcode":postalcode, "dnc":dnc, "lang":lang, "locationType":locationType, 
                         "latitude":latitude, "longitude":longitude, "sortOrder":sortOrder, "hideOnMap":hideOnMap, "lastWorked":lastWorked, "notes":notes})



# with open("output/output.csv", "r") as output:
#     reader = csv.DictReader(output)
#     for row in reader:
#         print(row)