import socket
from typing import List

from ..ship import Ship
from ..asteroid import Asteroid
from ..bullet import Bullet
from ..scenario import Scenario
from ..score import Score

class GraphicsUE:
    def __init__(self, map_size, ship_count, team_count):

        # Create udp senders/receivers
        udp_host = 'localhost'
        udp_port = 12345
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_recvr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_recvr.bind(('localhost', 12346))
        self.udp_addr = (udp_host, udp_port)

        # TODO Launch game

        # Wait for graphics engine to be fully initialized before sending scenario initialization message
        print('Waiting for graphics to launch.')
        graphics_ready = False
        while not graphics_ready:
            buf, tmp = self.udp_recvr.recvfrom(2097152)
            graphics_ready = buf.decode('utf-8') == 'graphics_ready'
        print('Graphics ready. Starting simulation')

        start_str = '::start::'
        start_str += 'map:' + str(map_size[0]) + ',' + str(map_size[1]) + ';'
        start_str += 'ships:' + str(ship_count)  + ';'
        start_str += 'teams:' + str(team_count)
        self.udp_sock.sendto(start_str.encode('utf-8'), self.udp_addr)

    def update(self, score: Score, ships: List[Ship], asteroids: List[Asteroid], bullets: List[Bullet]):
        update_str = '::frame::'
        for ship in ships:
            update_str += 's(' + str(int(ship.position[0])) + \
                          ',' + str(int(ship.position[1])) + \
                          ',' + str(int(ship.heading)) + \
                          ',' + str(int(ship.radius)) + \
                          ',' + str(int(ship.alive)) + \
                          ',' + str(float(ship.respawn_time_left)) + \
                          ');'
        for ast in asteroids:
            update_str += 'a(' + str(int(ast.position[0])) + \
                          ',' + str(int(ast.position[1])) + \
                          ',' + str(int(ast.angle)) + \
                          ',' + str(int(ast.radius)) + \
                          ',' + str(int(0.00)) + \
                          ',' + str(int(0.00)) + \
                          ');'
        for bullet in bullets:
            update_str += 'b(' + str(int(bullet.position[0])) + \
                          ',' + str(int(bullet.position[1])) + \
                          ',' + str(int(bullet.heading)) + \
                          ',' + str(int(bullet.length)) + \
                          ',' + str(int(0.00)) + \
                          ',' + str(int(0.00)) + \
                          ');'

        # Append scoreboard information to update_str
        update_str += '::score::'
        update_str += 'time;' + str(round(score.sim_time, 2)) + ';'
        for team in score.teams:
            update_str += 'team;' + str(int(team.team_id)) + \
                          ',' + str(int(team.asteroids_hit)) + \
                          ',' + str(int(team.lives_remaining)) + \
                          ',' + str(int(team.bullets_remaining)) + \
                          ',' + str(round(team.accuracy*100, 1)) + \
                          ';'




        self.udp_sock.sendto(update_str.encode('utf-8'), self.udp_addr)

    def close(self):
        self.udp_sock.close()
