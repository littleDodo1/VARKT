import krpc
import time

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

    print("Launching the rocket...")
    sc.active_vessel.control.activate_next_stage()

    with open("flight_log.txt", "a") as log_file:
        log_file.write("Time (s), Altitude (m), Speed (m/s)\n")

        altitude_stream = conn.add_stream(getattr, sc.active_vessel.flight(), 'mean_altitude')
        speed_stream = conn.add_stream(getattr, sc.active_vessel.flight(sc.active_vessel.orbit.body.reference_frame), 'speed')
        time_stream = conn.add_stream(getattr, sc.active_vessel, 'met')

        start_time = time.time()
        next_log_time = 1 

        with conn.stream(getattr, ascent, "enabled") as enabled:
            with enabled.condition:
                while enabled():
                    current_time = time.time() - start_time

                    altitude = altitude_stream()
                    speed = speed_stream()
                    mission_time = time_stream()

                    if current_time >= next_log_time:
                        log_file.write(f"{mission_time:.2f}, {altitude:.2f}, {speed:.2f}\n")
                        log_file.flush()  # Сбрасываем буфер для немедленной записи на диск
                        next_log_time += 1

                    print(f"Time: {mission_time:.2f} s, Altitude: {altitude:.2f} m, Speed: {speed:.2f} m/s")

    altitude_stream.remove()
    speed_stream.remove()
    time_stream.remove()

    print("Orbit achieved!")
    conn.close()

if __name__ == "__main__":
    launch_to_orbit()
