from streetlevel import lookaround

panos = lookaround.get_coverage_tile(69150, 40123)


# Print the 100 first panoramas ID
# for i in range(1):
#     print(panos[i].id)
#     auth = lookaround.Authenticator()
#     zoom = 0
#     for face in range(0, 6):
#         lookaround.download_panorama_face(panos[i], f"TestFolder/{panos[i].id}_{face}_{zoom}.heic",
#                                           face, zoom, auth)

# print(f"""
# Got {len(panos)} panoramas. Here's one of them:
# ID: {panos[0].id}\t\tBuild ID: {panos[0].build_id}
# Latitude: {panos[0].lat}\tLongitude: {panos[0].lon}
# Capture date: {panos[0].date}
# """)
#


if __name__ == "__main__":
    auth = lookaround.Authenticator()
    zoom = 2
    for face in range(0, 1):
        lookaround.download_panorama_face(panos[0], f"TestFolder/{panos[0].id}_{face}_{zoom}.heic",
                                          face, zoom, auth)



