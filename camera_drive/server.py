# coding=utf-8
'''
Простой HTTP-сервер.
Принимает пустые POST-запросы и подает соответствующие запросы на
аппаратуру (поворачивает моторы, включает подсветку, ...).
@author: Mic, 2012
'''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from httplib import OK, BAD_REQUEST

import nxt

class MotorHandler(object):
    '''
    Класс для управления мотором.
    '''
    
    # Положительная и отрицательная скорости:
    SPEED_POSITIVE = 10
    SPEED_NEGATIVE = -SPEED_POSITIVE
    
    # Угол поворота:
    ANGLE = 10
    
    def __init__(self, brick):
        '''
        @param brick: Brick
        '''
        self.motor_h = nxt.Motor(brick, nxt.PORT_B)
        self.motor_v = nxt.Motor(brick, nxt.PORT_C)
    
    def rotate(self, direction):
        '''
        Вращает установку в указанном направлении.
        @param direction: str
        '''
        if direction == 'up':
            self.motor_v.turn(self.SPEED_NEGATIVE, self.ANGLE)
        if direction == 'down':
            self.motor_v.turn(self.SPEED_POSITIVE, self.ANGLE)
        if direction == 'left':
            self.motor_h.turn(self.SPEED_NEGATIVE, self.ANGLE)
        if direction == 'right':
            self.motor_h.turn(self.SPEED_POSITIVE, self.ANGLE)

class LightHandler(object):
    '''
    Класс для управления подсветкой.
    '''
    
    def __init__(self, brick):
        '''
        @param brick: Brick
        '''
        self.light = nxt.Color20(brick, nxt.PORT_1)
        self.turn('off')
    
    def turn(self, state):
        '''
        Включает или выключает подсветку.
        @param state: str
        '''
        self.light.set_light_color(nxt.Type.COLORRED if state == 'on' else nxt.Type.COLORNONE)

class HttpRequestHandler(BaseHTTPRequestHandler):
    '''
    Реализация обработчика запросов.
    '''
    
    def do_GET(self):
        '''
        Обрабатывает входящий GET-запрос.
        Просто отдаем клиентскую страничку.
        '''
        self.send_response(OK)
        self.end_headers()
        response = open('client.htm').read()
        self.wfile.write(response)
    
    def _handle_command(self):
        '''
        Обрабатывает запрос, передавая команды оборудованию.
        Возвращает True, если запрос корректный.
        @return: True
        '''
        parts = filter(bool, self.path.split('/'))
        if len(parts) != 2:
            return False
        if parts[0] == 'motor':
            if parts[1] in ('up', 'down', 'left', 'right'):
                motor_handler.rotate(parts[1])
                return True
        if parts[0] == 'light':
            if parts[1] in ('on', 'off'):
                light_handler.turn(parts[1])
                return True
        return False
    
    def do_POST(self):
        '''
        Обрабатывает входящий POST-запрос.
        '''
        code = OK if self._handle_command() else BAD_REQUEST
        self.send_response(code)

def start(host, port):
    '''
    Запускает HTTP-сервер.
    @param host: str
    @param port: int
    '''
    server = HTTPServer((host, port), HttpRequestHandler)
    server.serve_forever()

brick = nxt.find_one_brick()
motor_handler = MotorHandler(brick)
light_handler = LightHandler(brick)

start('', 8080)
