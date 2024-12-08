import krpc

def transfer_to_mun():
    conn = krpc.connect(name="Mun Transfer")
    sc = conn.space_center
    mj = conn.mech_jeb

    Mun = conn.space_center.bodies["Mun"]
    conn.space_center.target_body = Mun
    print("Target set to Mun.")

    print("Planning Hohmann transfer...")
    planner = mj.maneuver_planner
    hohmann = planner.operation_transfer
    hohmann.simple_transfer = True
    hohmann.make_nodes()

    warning = hohmann.error_message
    if warning:
        print(f"Warning: {warning}")
        conn.close()
        return

    print("Transfer nodes created.")

    executor = mj.node_executor
    print("Executing transfer nodes...")
    executor.execute_all_nodes()

    with conn.stream(getattr, executor, "enabled") as enabled:
        enabled.rate = 1
        with enabled.condition:
            while enabled():
                enabled.wait()

    print("Transfer to Mun complete!")
    conn.close()

if __name__ == "__main__":
    transfer_to_mun()