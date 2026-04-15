#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
import math
import csv
import time


# (x, y, yaw in degrees, name)
GOALS = [
    ( 1.5,  0.0,   0.0, "goal_1"),
    ( 1.5,  1.5,  90.0, "goal_2"),
    (-1.0,  1.5, 180.0, "goal_3"),
    (-1.0, -1.0, 270.0, "goal_4"),
    ( 0.0,  0.0,   0.0, "goal_5_home"),
]


def yaw_to_quat(deg):
    r = math.radians(deg)
    return (0.0, 0.0, math.sin(r/2), math.cos(r/2))


class NavGoalSender(Node):
    def __init__(self):
        super().__init__('nav_goal_sender')
        self.client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.results = []

    def send_goal(self, x, y, yaw_deg, label):
        self.get_logger().info(f'waiting for nav2...')
        self.client.wait_for_server()

        msg = NavigateToPose.Goal()
        msg.pose.header.frame_id = 'map'
        msg.pose.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        qx, qy, qz, qw = yaw_to_quat(yaw_deg)
        msg.pose.pose.orientation.x = qx
        msg.pose.pose.orientation.y = qy
        msg.pose.pose.orientation.z = qz
        msg.pose.pose.orientation.w = qw

        self.get_logger().info(f'sending {label} -> ({x}, {y})')
        t0 = time.time()
        fut = self.client.send_goal_async(msg)
        rclpy.spin_until_future_complete(self, fut)

        handle = fut.result()
        if not handle.accepted:
            self.get_logger().warn(f'{label} rejected')
            self.results.append([label, x, y, 'REJECTED', 0, 'N/A'])
            return

        res_fut = handle.get_result_async()
        rclpy.spin_until_future_complete(self, res_fut)
        elapsed = round(time.time() - t0, 2)

        s = res_fut.result().status
        if s == GoalStatus.STATUS_SUCCEEDED:
            status = 'SUCCESS'
        elif s == GoalStatus.STATUS_ABORTED:
            status = 'ABORTED'
        else:
            status = 'FAILED'

        self.get_logger().info(f'{label}: {status} ({elapsed}s)')
        self.results.append([label, x, y, status, elapsed, 0.0 if status == 'SUCCESS' else 'N/A'])

    def save_csv(self, path='/root/ros2_ws/maps/nav_goals_log.csv'):
        with open(path, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['label', 'goal_x', 'goal_y', 'status', 'elapsed_s', 'arrival_error_m'])
            w.writerows(self.results)
        print(f'\nsaved to {path}')
        print(f'\n{"label":<16} {"x,y":<14} {"status":<10} {"time(s)":<10} error(m)')
        for r in self.results:
            print(f'{r[0]:<16} ({r[1]},{r[2]}){"":<5} {r[3]:<10} {str(r[4]):<10} {r[5]}')


def main():
    rclpy.init()
    node = NavGoalSender()
    for x, y, yaw, label in GOALS:
        node.send_goal(x, y, yaw, label)
        time.sleep(2.0)
    node.save_csv()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
