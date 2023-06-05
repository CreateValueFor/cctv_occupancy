import pyDOE2 as doe2

# 건물 모델링
building = doe2.Building()
building.add_zone("Zone1", area=100, volume=300, height=3)
building.add_wall("Wall1", zone_name="Zone1", area=50, u_value=0.2)
# 필요한 모델링 요소들을 추가로 정의합니다.

# 시뮬레이션 설정
simulation = doe2.Simulation(building)
simulation.set_weather("weather.epw")
simulation.set_start_date("01/01/2023")
simulation.set_end_date("12/31/2023")
# 추가적인 시뮬레이션 설정을 정의합니다.

# 시뮬레이션 실행
results = simulation.run()

# 결과 분석
indoor_temperatures = results.get_variable("Zone1:Zone Mean Air Temperature")
# 원하는 출력 변수를 추출합니다.

# 실내온도 예측 결과 출력
for time, temperature in zip(results.time, indoor_temperatures):
    print(f"Time: {time}, Temperature: {temperature}")
