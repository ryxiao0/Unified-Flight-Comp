#  YOU SHOULD NOT NEED TO CHANGE THIS FILE FOR THIS PROBLEM
from GetUEFC import UEFC
from opt_mO3 import opt_mO3
import numpy as np
import pandas
import matplotlib.pyplot as plt

def report_opt_mO3(UEFC, AR, S):
    
    # This function is a wrapper for opt_mO3. Calling it will print out the 
    # optimized performance, operating conditions, etc found after running 
    # opt_mO3.  It calls opt_mO3 and then prints out useful information.
    
    opt_vars, mO3, success = opt_mO3(UEFC, AR, S)
    
    if success:
        
        wing_dimensions = UEFC.wing_dimensions(AR, S)
        
        N    = opt_vars[0]
        R    = opt_vars[1]
        mpay = opt_vars[2]
        
        V     = UEFC.flight_velocity(opt_vars, AR, S)
        Omega = UEFC.turn_rate(opt_vars, AR, S)
        
        print()
        print("Results Summary from opt_mO3\n")
        print("mpay Omega^3 = %0.0f g/s^3" % mO3)
        print("mpay         = %0.0f g"     % mpay)
        print("R            = %0.2f m"     % R)
        print("V            = %0.2f m/s"   % V)
        print("Omega        = %0.2f rad/s" % Omega)
        print()
        
        print("Geometry")
        print("----------------------------------------------\n")
        print("AR      = %5.3f"       % AR)
        print("S       = %5.3f sq. m" % S)
        print("b       = %5.3f m"     % wing_dimensions["Span"])
        print("cbar    = %5.3f m"     % wing_dimensions["Mean chord"])
        print("cr      = %5.3f m"     % wing_dimensions["Root chord"])
        print("ct      = %5.3f m"     % wing_dimensions["Tip chord"])
        print("lambda  = %5.3f"       % UEFC.taper)
        print("tau     = %5.3f"       % UEFC.tau)
        print("eps     = %5.3f\n"     % UEFC.max_camber())
        
        mass_data = UEFC.mass(opt_vars,AR, S)
        
        print("Masses")
        print("----------------------------------------------\n")
        print("W/g     = %4.0f g"   % mass_data["Total"])
        print("Wfuse/g = %4.0f g"   % mass_data["Breakdown"]["Fuselage"])
        print("Wwing/g = %4.0f g"   % mass_data["Breakdown"]["Wing"])
        print("Wpay/g  = %4.0f g\n" % mass_data["Breakdown"]["Payload"])
        
        CL      = UEFC.lift_coefficient(opt_vars, AR, S)
        CD_data = UEFC.drag_coefficient(opt_vars, AR, S)
        e       = UEFC.span_efficiency( opt_vars, AR, S)
        
        print("Aerodynamic performance")
        print("----------------------------------------------")
        print("N       = %5.3f"   % N)
        print("CL      = %5.3f"   % CL)
        print("CLdes   = %5.3f"   % UEFC.CLdes)
        print("CD      = %5.3f"   % CD_data["Total"])
        print("CDfuse  = %5.3f"   % CD_data["Breakdown"]["Fuselage"])
        print("CDp     = %5.3f"   % CD_data["Breakdown"]["Wing"])
        print("CDi     = %5.3f"   % CD_data["Breakdown"]["Induced"])
        print("CDpay   = %5.3f"   % CD_data["Breakdown"]["Payload"])
        print("e0      = %5.3f"   % UEFC.e0)
        print("e       = %5.3f\n" % e)
    
        T_req = UEFC.required_thrust(opt_vars, AR, S)
        T_max = UEFC.maximum_thrust(V)
        
        print("Thrust")
        print("----------------------------------------------\n")
        print("T       = %5.3f N"   % T_req)   
        print("Tmax    = %5.3f N\n" % T_max)
        
        db = UEFC.wing_tip_deflection(opt_vars, AR, S)
        
        print("Bending")
        print("----------------------------------------------\n")    
        print("d/b     = %5.3f" % db)
        print("d/bmax  = %5.3f" % UEFC.dbmax)
    
    else:
        
        print("\nError in opt_V: success = " + str(success))
        print("  Usually this is because the airplane could not fly while " +
              "meeting all constraints.\n")
    
    return
        

if __name__ == "__main__":
    
    # Simple test case. Feel free to modify this part of the file.
    aircraft = UEFC()

    AR = 9.45
    S  = 0.4  # m^2
    aircraft.dbmax = .1
    aircraft.dihedral = 10 # degrees
    aircraft.e0 = 1
    aircraft.taper = .4
    aircraft.tau = .08
    aircraft.CLdes = .758
    # aircraft.rhofoam = 25.5 # kg/m^3
    # aircraft.Efoam = 12 * 10**6 # Pa

    # AR = 11
    # S  = 0.3  # m^2

    # Optimal Values
    # AR = 9.25
    # S = .385
    """
    AR      = 9.500
    S       = 0.400 sq. m
    b       = 1.949 m
    cbar    = 0.205 m
    cr      = 0.293 m
    ct      = 0.117 m
    lambda  = 0.400
    tau     = 0.080
    eps     = 0.060
    """
    # b = 1.5
    # cr = .2
    # ct = .1

    # CLdes = np.arange(.6, .86, .05)
    # z = np.zeros(len(CLdes))
    # col = ["CLdes", "m_pay*omega^3", "m_pay", "omega", "R", "CL", "T", "Tmax", "d/b", "N"]
    # zz = np.array([z for i in range(len(col))])

    # data = pandas.DataFrame(zz.T, columns=col)


    # for c in range(len(CLdes)):
    #     aircraft.CLdes = CLdes[c]
    #     opt_vars, mO3, success = opt_mO3(aircraft, AR, S)
    #     V = aircraft.flight_velocity(opt_vars, AR, S)

    #     data["CLdes"].loc[c] = CLdes[c]
    #     data["m_pay"].loc[c] = opt_vars[2]
    #     data["omega"].loc[c] = aircraft.turn_rate(opt_vars, AR, S)
    #     data["m_pay*omega^3"].loc[c] = data["m_pay"].loc[c] * data["omega"].loc[c]**3
    #     data["R"].loc[c] = opt_vars[1]
    #     data["CL"].loc[c] = aircraft.lift_coefficient(opt_vars, AR, S)
    #     data["T"].loc[c] = aircraft.required_thrust(opt_vars, AR, S)
    #     data["Tmax"].loc[c] = aircraft.maximum_thrust(V)
    #     data["d/b"].loc[c] = aircraft.wing_tip_deflection(opt_vars, AR, S)
    #     data["N"].loc[c] = opt_vars[0]

    # print(data)

    # data.plot(kind="scatter", x="CLdes", y="m_pay*omega^3", title="Objective vs CLdes")
    # data.plot(kind="scatter", x="CLdes", y="m_pay", title="Payload Mass vs CLdes")
    # data.plot(kind="scatter", x="CLdes", y="R", title="R vs CLdes")
    # data.plot(kind="scatter", x="CLdes", y="CL", title="CL vs CLdes")
    # Tax = data.plot(kind="scatter", x="CLdes", y="Tmax", label="Tmax", title="T vs CLdes")
    # data.plot(kind="scatter", x="CLdes", y="T", ax=Tax, color="orange", label="T")
    # data.plot(kind="scatter", x="CLdes", y="d/b", title="d/b vs CLdes")
    # data.plot(kind="scatter", x="CLdes", y="N", title="N vs CLdes")
    
    # plt.legend()
    # plt.show()

    report_opt_mO3(aircraft, AR, S)
