import csv
from min_heap import MinHeap
from binary_search import binary_search


# Address Data Standard Form:
# ------------------------------------------------------------------------------------------------------------------------------------------
# line1 / line2 / city / state / postalcode / dnc / lang / locationType / latitude / longitude / sortOrder / hideOnMap / lastWorked / notes
# ------------------------------------------------------------------------------------------------------------------------------------------

# ////////// Storage //////////
# Storage for Abbreviations
abbrv_dict = {"DR":"DRIVE", "LN":"LANE", "RD":"ROAD", "ST":"STREET", "AV":"AVENUE", "BLVD":"BOULEVARD", "CIR":"CIRCLE", "EXT":"EXTENSION", "HTS":"HEIGHTS", "JCT":"JUNCTION", "CT":"COURT"}
nsew = {"N":"NORTH", "S":"SOUTH", "E":"EAST", "W":"WEST"}
# Storage for Poughkeepsie Structures Data
sorted = MinHeap()
sorted_addresses = []
# Storage for SOPO Territory Data
dncs = []
clean_addresses = []
territory_addresses = []

# Standardize Address Format
def expand_abbrv(address):
    
    split_address = address[0].split(" ")
    
    if split_address[-1] in abbrv_dict.keys():
        split_address[-1] = abbrv_dict[split_address[-1]]
    if len(split_address) >= 2:
        if split_address[1] in nsew.keys():
            split_address[1] = nsew[split_address[1]]

    address[0] = " ".join(split_address)
    return address

def standardize(address, is_dnc=False):
    standard_form_address = {"line1":"", "line2":"", "city":"", "state":"", "postalcode":"", "dnc":"", "lang":"", "locationType":"", 
                                    "latitude":0, "longitude":0, "sortOrder":"", "hideOnMap":"", "lastWorked":"", "notes":""}
    street = address[0].split(" ")
    line1 = []
    line2 = ""
    # If street address ends in an apartment/unit number:
    if len(street[-1]) > 0:
        if street[-1][-1] in [str(x) for x in range(0, 10)]:
            # Determine if apartment/unit number is preceded by a word:
            if street[-2] not in abbrv_dict.keys() and street[-2] not in abbrv_dict.values():
                line2 = street[-2]
                line1 = street[:-2]
            else:
                line1 = street[:-1]
            line2 += street[-1]
        # If street address does not end in an apartment/unit number:
        else:
            line1 = street
    # Add street address into lines 1 and 2
    standard_form_address["line2"] = line2
    standard_form_address["line1"] = " ".join(line1)


    # Check if address[1] contains city or lastWorked data:
    if address[1]:
        if address[1][-1] in [str(x) for x in range(0, 10)]:
            # standard_form_address["lastWorked"] = address[1]
            pass
        else:
            standard_form_address["city"] = address[1]
    
    # Add postal code and any notes:
    standard_form_address["postalcode"] = address[2]
    standard_form_address["notes"] = (" / ".join(address[3:])).strip("/ ")

    #If the address is a DNC:
    #print(is_dnc)
    if is_dnc is True:
        standard_form_address["dnc"] = "TRUE"


    return standard_form_address



# ////////// Gather Territory Records Data //////////
filename = input("What file would you like to access?\n")
with open("input/" + str(filename), "r") as territory_record:

    reader = csv.reader(territory_record)

    addresses = []
    counter = 0
    for row in reader:
        item_list = []
        #print(row)
        is_empty = True
        for item in row[1:]:
            if item != '':
                is_empty = False
            item_list.append(item)
        if is_empty is not True:
            addresses.append(item_list)

    # Remove empty lists from addresses
    for element in addresses:
        if element == []:
            addresses.remove(element)

    # Separate the DNC section from the regular addresses
    index = 0
    for address in addresses:
        if address == ['Address', '', '', 'Name', 'Phone Numbers', '', '', 'Notes']:
            break
        index += 1
    clean_dncs = addresses[5:index]
    clean_addresses = addresses[index + 1:]

    # Put all text in uppercase and expand all contractions
    temp_addresses = []
    for address in clean_addresses:
        new_address = []
        for item in address:
            item = item.upper()
            new_address.append(item)
        temp_addresses.append(expand_abbrv(new_address))   

    for address in clean_dncs:
        new_address = []
        for item in address:
            item = item.upper()
            new_address.append(item)
        dncs.append(expand_abbrv(new_address))

    # Reorder address data into standard form (see line 6):
    # print(dncs, temp_addresses)
    for address in temp_addresses:
        territory_addresses.append(standardize(address, False))
    # Add DNCs to territory_addresses:
    for address in dncs:
        territory_addresses.append(standardize(address, True))
    for address in territory_addresses:
        print(address)


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
    search = binary_search(sorted_addresses, territory_address["line1"])
    if search is None:
        failed_searches.append(territory_address)
    # If binary_search() is succesful, update the territory_address:
    else:
        # If city is empty:
        if territory_address["city"] == "":
            territory_address["city"] = search[3]
        territory_address["state"] = search[4]
        territory_address["longitude"] = search[6]
        territory_address["latitude"] = search[7]
        # territory_address["locationType"] = str(search[0] + " / " + search[1])

        complete_addresses.append(territory_address)

print("Failed Searches: ", failed_searches)
print("Completed Addresses:", complete_addresses)


# ////////// Write Data to Output CSV //////////
with open("output/output.csv", "w") as output:
    fieldnames = ["line1","line2","city","state","postalcode","dnc","lang","locationType","latitude","longitude","sortOrder","hideOnMap","lastWorked","notes"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for address in complete_addresses:
        writer.writerow(address)



# with open("output/output.csv", "r") as output:
#     reader = csv.DictReader(output)
#     for row in reader:
#         print(row)