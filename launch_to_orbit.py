import krpc

def launch_to_orbit():
    conn = krpc.connect(name="Orbit Ascent")
    sc = conn.space_center
    mj = conn.mech_jeb
    ascent = mj.ascent_autopilot

    ascent.desired_orbit_altitude = 180000  
    ascent.desired_inclination = 0         
    ascent.force_roll = True               
    ascent.vertical_roll = 90
    ascent.turn_roll = 90
    ascent.autostage = True                
    ascent.enabled = True                 

    # Запуск ракеты
    print("Launching the rocket...")
    sc.active_vessel.control.activate_next_stage()

    with conn.stream(getattr, ascent, "enabled") as enabled:
        enabled.rate = 1
        with enabled.condition:
            while enabled():
                enabled.wait()

    print("Orbit achieved!")
    conn.close()

if __name__ == "__main__":
    launch_to_orbit()
