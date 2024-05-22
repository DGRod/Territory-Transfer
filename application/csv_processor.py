import csv
from application.min_heap import MinHeap
from application.binary_search import binary_search

# Storage for Poughkeepsie Structures Data
sorted = MinHeap()
sorted_addresses = []
# Storage for SOPO Territory Data
dncs = []
clean_addresses = []
territory_addresses = []

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
with open("SOPO Territory #01.csv", "r") as structures:

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
    
    dncs = addresses[4:index]
    clean_addresses = addresses[index + 1:]

    for address in clean_addresses:
        new_address = []
        for item in address:
            item = item.upper()
            new_address.append(item)
        territory_addresses.append(standardize(new_address))   

    # print("DNCs", dncs)
    # print("Addresses", clean_addresses)


# ////////// Gather Poughkeepsie Structures Data //////////
with open("Poughkeepsie Structures.csv", "r") as structures:
    
    reader = csv.reader(structures)

    for line in reader:
        if line != ['OCC_CLS', 'PRIM_OCC', 'PROP_ADDR', 'PROP_CITY', 'PROP_ST', 'PROP_ZIP', 'LONGITUDE', 'LATITUDE']:
            sorted.add(line)

    while sorted.count > 0:
        sorted_addresses.append(sorted.retrieve_min())



# ////////// Data Comparison //////////
# for address in sorted_addresses:
#     print(address[2])
# print(territory_addresses)

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

# print(len(territory_addresses), len(complete_addresses), len(failed_searches))

