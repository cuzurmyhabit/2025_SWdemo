from protocols.generateprotocol import GenerateProtocol
from operations.cube.cubeoperationutils import CubeOperationUtils
import time
import copy

class CubeOperation():
    def __init__(self, number, group_id, robot_status, start_check, write):
        self._GenerateProtocolInstance = GenerateProtocol(number, group_id)
        self._robot_status = robot_status
        self._start_check_copy = start_check
        self._write_copy = write
       

    ### robot_status 얻기
    def _get_robot_status(self, group_id, status, variable):
        return eval("self._robot_status[{}].{}.{}".format(group_id, status, variable))

    ### robot_status 설정
    def _set_robot_status(self, group_id, status, variable, value):
        exec("self._robot_status[{}].{}.{} = {}".format(group_id, status, variable, value))

    ### 센서 데이터 얻기
    def receive_sensor_data(self, cube_ID, method, period=1, group_id=None):
        group_id = CubeOperationUtils.proc_group_id(self._GenerateProtocolInstance._group_id, group_id)
        ### start 체크
        self._start_check_copy()
        ### 연결 개수
        connection_number = self._robot_status[group_id].controller_status.connection_number
        ### 버튼 데이터 처리
        if connection_number == 1:
            self._button_before = -1
            #self._button_before2 = -1
        else:
            self._button_before = [-1]*connection_number
            #self._button_before2 = [-1]*connection_number
        ### cube ID 처리
        cube_ID = CubeOperationUtils().process_cube_ID(cube_ID, connection_number)
        ### method 체크 (str, "oneshot", "periodic", "stop")
        CubeOperationUtils().check_method(method, cube_ID, group_id, self._get_robot_status, self._set_robot_status)
        ### period 체크 & 처리 (int or float, 0.01 to 1 (sec))
        period = CubeOperationUtils().process_period(method, period)
        ### 바이트 쓰기
        sending_bytes = self._GenerateProtocolInstance.GetSensors_bytes(cube_ID, period, group_id)
        self._write_copy(sending_bytes) 
        ### sleep
        time.sleep(0.2)

    ### 센서 데이터 끄기
    def stop_sensor_data(self, cube_ID, group_id=None):
        self.receive_sensor_data(cube_ID, "stop", 1, group_id)

    ### 현재 proximity 값 얻기 (robot_status로 부터)
    def get_current_proxy(self, cube_ID, group_id=None):
        group_id = CubeOperationUtils.proc_group_id(self._GenerateProtocolInstance._group_id, group_id)

        connection_number = self._robot_status[group_id].controller_status.connection_number
        cube_ID = CubeOperationUtils().process_cube_ID(cube_ID, connection_number)
        if connection_number == 1 and cube_ID == 0xFF:
            cube_ID = 0
        if cube_ID == 0xFF:
            proxy_value = self._robot_status[group_id].processed_status.sensor_prox
        else:
            proxy_value = self._robot_status[group_id].processed_status.sensor_prox[cube_ID]
        return proxy_value

    ### 디폴트 proximity 값 얻기 (robot_status로 부터)
    def get_default_proxy(self, cube_ID,  group_id=None):
        group_id = CubeOperationUtils.proc_group_id(self._GenerateProtocolInstance._group_id, group_id)

        connection_number = self._robot_status[group_id].controller_status.connection_number
        cube_ID = CubeOperationUtils().process_cube_ID(cube_ID, connection_number)
        if connection_number == 1 and cube_ID == 0xFF:
            cube_ID = 0
        if cube_ID == 0xFF:
            while True:
                proxy_value = self._robot_status[group_id].processed_status.sensor_prox
                for i in range(connection_number):
                    if proxy_value[i] == 0:
                        break
                else:
                    return proxy_value
        else:
            while True:
                proxy_value = self._robot_status[group_id].processed_status.sensor_prox[cube_ID]
                if proxy_value > 0:
                    return proxy_value

    ### 현재 button 값 얻기 (robot_status로 부터)
    def get_current_button(self, cube_ID, group_id=None):
        group_id = CubeOperationUtils.proc_group_id(self._GenerateProtocolInstance._group_id, group_id)

        connection_number = self._robot_status[group_id].controller_status.connection_number
        cube_ID = CubeOperationUtils().process_cube_ID(cube_ID, connection_number)
        if connection_number == 1 and cube_ID == 0xFF:
            cube_ID = 0
        if cube_ID == 0xFF:
            button_value = self._robot_status[group_id].processed_status.button
        else:
            button_value = self._robot_status[group_id].processed_status.button[cube_ID]
        
        if type(button_value) == int or type(button_value) == type(None):
            if button_value == None or button_value == 0:
                button_out = 0
            elif button_value > 0 and (self._button_before == -1 or self._button_before == None):
                button_out = 0
            else:
                button_out = 1
        elif type(button_value) == list:
            button_out = [-1]*connection_number
            for i, button_ev in enumerate(button_value):
                if button_ev == None or button_ev == 0:
                    button_out[i] = 0
                elif button_ev > 0 and (self._button_before[i] == -1 or self._button_before[i] == None):
                    button_out[i] = 0
                else:
                    button_out[i] = 1
        else:
            raise ValueError(type(button_value), ": Not expected type.")

        #print(button_value)
        #self._button_before2 = copy.copy(self._button_before)
        self._button_before = button_value

        # Not_pressed: 0, Pressed: 1
        return button_out

    ### 현재 zyro 값 얻기 (robot_status로 부터)
    def get_current_gyro(self, cube_ID, group_id=None):
        group_id = CubeOperationUtils.proc_group_id(self._GenerateProtocolInstance._group_id, group_id)
        connection_number = self._robot_status[group_id].controller_status.connection_number
        cube_ID = CubeOperationUtils().process_cube_ID(cube_ID, connection_number)
        if connection_number == 1 and cube_ID == 0xFF:
            cube_ID = 0
        if cube_ID == 0xFF:
            gyro_value = self._robot_status[group_id].processed_status.sensor_gyro_xyz
        else:
            gyro_value = self._robot_status[group_id].processed_status.sensor_gyro_xyz[cube_ID]
        for i, value in enumerate(gyro_value):
            if type(value) != list and type(value) == type(None):
                gyro_value[i] = 0
            elif type(value) == list:
                for j, value2 in enumerate(value):
                    if type(value2) == type(None):
                        gyro_value[i][j] = 0
        # yaw right: z +90, yaw left: z -90
        # star: x +90, square: x -90, triangle: y +90, circle: y -90
        return gyro_value
