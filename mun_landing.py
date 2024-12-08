import krpc

conn = krpc.connect(name='Lunar Landing')
vessel = conn.space_center.active_vessel

obt_frame = vessel.orbit.body.non_rotating_reference_frame
orb_speed = conn.add_stream(getattr, vessel.flight(obt_frame), 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')

print("Preparing for landing...")
vessel.control.speed_mode = vessel.control.speed_mode.surface
ap = vessel.auto_pilot
ap.sas = True
ap.sas_mode = ap.sas_mode.retrograde

def burn_to_speed(target_speed, throttle):
    """Reduces speed to the target speed."""
    while orb_speed() > target_speed:
        vessel.control.throttle = throttle
    vessel.control.throttle = 0.0

print("Deorbiting from lunar orbit...")
while 5000 < altitude() < 7000:
    burn_to_speed(200, 0.8)

print("Commencing landing...")

land_stages = [ 
    (1500, 150, 0.6),  
    (1000, 100, 0.5),  
    (500, 60, 0.5),   
    (100, 17, 0.35),
    (50, 12, 0.15)
]

for stage in land_stages:
    target_altitude, target_speed, throttle = stage
    while altitude() > target_altitude:
        burn_to_speed(target_speed, throttle)

# Final landing phase
print("Final approach...")
while altitude() > 10:
    if orb_speed() > 3:
        vessel.control.throttle = 0.3
    else:
        vessel.control.throttle = 0.0

vessel.control.throttle = 0.0
print("Landing complete!")