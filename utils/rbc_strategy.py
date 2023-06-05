# The performance of the proposed adaptive control scheme will be compared with a baseline rule-based on/off control (RBC) scheme commonly used by thermostats in residential homes. These RBC algorithms represent the core logic behind the most popular mechanical and digital controls of thermostats in residential homes. Figure 2a,b describe the overall schemes for summer and winter cases, respectively. Basically, the RBC rules compare the indoor temperature T with a given reference temperature 𝑇𝑟𝑒𝑓
# , which is allowed to drift by a cooling/heating dead band Δ𝑇𝑐
#  or Δ𝑇ℎ , respectively.

class HVACSystem_rbc:
    def __init__(self):
        self.target_temperature = 24.0
        self.current_temperature = 0.0
        self.heating_threshold = 0.5
        self.cooling_threshold = 0.5

    def measure_temperature(self, ta):
        # 실제로는 센서를 통해 온도를 측정합니다.
        self.current_temperature = ta

    def control_hvac(self):
        if self.current_temperature < self.target_temperature - self.heating_threshold:
            self.turn_on_heating()
        elif self.current_temperature > self.target_temperature + self.cooling_threshold:
            self.turn_on_cooling()

    def turn_on_heating(self):
        # 난방 장치를 켜는 동작을 수행합니다.
        print("Heating turned on.")

    def turn_on_cooling(self):
        # 냉방 장치를 켜는 동작을 수행합니다.
        print("Cooling turned on.")


def main():
    hvac_system = HVACSystem_rbc()
    hvac_system.measure_temperature()
    hvac_system.control_hvac()


if __name__ == "__main__":
    main()
