import krpc
import time

conn = krpc.connect(name='Retrograde Burn at Periapsis')
vessel = conn.space_center.active_vessel
orbit = vessel.orbit

if orbit.body.name.lower() != 'mun':
    raise Exception("The vessel is not in Mun's orbit!")

vessel.control.sas = True
time_to_periapsis = orbit.time_to_periapsis
print(f"Time to periapsis: {time_to_periapsis:.2f} seconds.")

# Time warp, leaving 10 seconds for preparation
conn.space_center.warp_to(conn.space_center.ut + time_to_periapsis - 10)

print("Waiting for periapsis...")
while orbit.time_to_periapsis > 0.1:
    time.sleep(0.1)

# Set SAS to retrograde
print("Reached periapsis. Engaging SAS in 'retrograde' mode.")
vessel.control.sas_mode = vessel.control.sas_mode.retrograde

print("Engaging engine for 15 seconds...")
vessel.control.throttle = 1.0
start_time = conn.space_center.ut

while conn.space_center.ut < start_time + 15:
    time.sleep(0.1)

vessel.control.throttle = 0.0
print("Engine cutoff. Maneuver complete.")