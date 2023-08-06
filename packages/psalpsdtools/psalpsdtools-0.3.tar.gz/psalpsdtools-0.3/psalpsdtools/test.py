# Example usage:
from PhilippinesRegions import PhilippinesRegions
philippines = PhilippinesRegions()
all_regions = philippines.get_regions()

print("Regions of the Philippines:")
for region in all_regions:
    print(region)

selected_region = "Central Luzon"
selected_provinces = philippines.get_provinces(selected_region)

print(f"\nProvinces in {selected_region}:")
if selected_provinces:
    for province in selected_provinces:
        print(province)
else:
    print("Region not found or has no provinces.")