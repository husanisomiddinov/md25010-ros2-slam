#!/usr/bin/env python3

import math
import csv
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseWithCovarianceStamped


GOALS = [
    ( 1.5,  0.0,   0.0, "goal_1"),
    ( 1.5,  1.5,  90.0, "goal_2"),
    (-1.0,  1.5, 180.0, "goal_3"),
    (-1.0, -1.0, 270.0, "goal_4"),
    ( 0.0,  0.0,   0.0, "goal_5_home"),
]

LOG_PATH = '/root/ros2_ws/maps/nav_goals_log.csv'


def yaw_to_quat(deg: float):
    r = math.radians(deg)
    return 0.0, 0.0, math.sin(r / 2), math.cos(r / 2)


class NavGoalSender(Node):
    def __init__(self):
        super().__init__('nav_goal_sender')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # need TRANSIENT_LOCAL to get the last pose even if we subscribe after it was published
        amcl_qos = QoSProfile(
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
        )
        self._current_pose = None
        self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self._amcl_cb,
            amcl_qos,
        )
        self._results = []

    def _amcl_cb(self, msg: PoseWithCovarianceStamped):
        self._current_pose = msg.pose.pose

    def _arrival_error(self, goal_x: float, goal_y: float) -> float:
        if self._current_pose is None:
            return float('nan')
        dx = self._current_pose.position.x - goal_x
        dy = self._current_pose.position.y - goal_y
        return round(math.hypot(dx, dy), 4)

    def send_goal(self, x: float, y: float, yaw_deg: float, label: str):
        self.get_logger().info(f'[{label}] waiting for Nav2...')
        self._action_client.wait_for_server()

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        qx, qy, qz, qw = yaw_to_quat(yaw_deg)
        goal_msg.pose.pose.orientation.x = qx
        goal_msg.pose.pose.orientation.y = qy
        goal_msg.pose.pose.orientation.z = qz
        goal_msg.pose.pose.orientation.w = qw

        self.get_logger().info(f'[{label}] -> ({x}, {y}, {yaw_deg}°)')
        t0 = time.time()
        send_future = self._action_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_future)

        handle = send_future.result()
        if not handle.accepted:
            self.get_logger().warn(f'[{label}] rejected')
            self._results.append([label, x, y, 'REJECTED', 0.0, 'N/A'])
            return

        result_future = handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        elapsed = round(time.time() - t0, 2)

        status_code = result_future.result().status
        if status_code == GoalStatus.STATUS_SUCCEEDED:
            status = 'SUCCESS'
            error = self._arrival_error(x, y)
        elif status_code == GoalStatus.STATUS_ABORTED:
            status = 'ABORTED'
            error = 'N/A'
        else:
            status = 'FAILED'
            error = 'N/A'

        self.get_logger().info(f'[{label}] {status} in {elapsed}s, error={error}m')
        self._results.append([label, x, y, status, elapsed, error])

    def save_csv(self, path: str = LOG_PATH):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['label', 'goal_x', 'goal_y', 'status', 'elapsed_s', 'arrival_error_m'])
            writer.writerows(self._results)
        self.get_logger().info(f'saved to {path}')
        print(f'\n{"label":<16} {"goal (x,y)":<16} {"status":<10} {"time(s)":<10} error(m)')
        print('-' * 62)
        for r in self._results:
            print(f'{r[0]:<16} ({r[1]},{r[2]}){"":<7} {r[3]:<10} {str(r[4]):<10} {r[5]}')


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
