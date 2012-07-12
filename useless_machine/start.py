# coding=utf-8
# Больше информации и пример работы: http://mic-dm.blogspot.com/2012/07/blog-post.html.

from time import sleep

import nxt
from nxt.locator import find_one_brick
from nxt.sensor.generic import Touch

# Определяем кирпич, мотор и кнопку:
brick = find_one_brick()
motor = nxt.Motor(brick, nxt.PORT_B)
sensor = Touch(brick, nxt.PORT_1)

# "Мотор запаркован" у нас будет означать, что
# кочерга мотора находится в нижнем положении:
is_parked = False
while True:
    if sensor.is_pressed():
        # Если кнопка нажата, ждем недолго и крутим мотор,
        # чтобы освободить кнопку:
        sleep(1)
        motor.turn(-20, 40, False)
        is_parked = False
    elif not is_parked:
        # Если кнопка отжата, но мотор не запаркован,
        # паркуем:
        motor.turn(20, 40, False)
        is_parked = True
    sleep(0.1)
