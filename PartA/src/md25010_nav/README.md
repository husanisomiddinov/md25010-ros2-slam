# md25010_nav

ROS 2 package for Grant Project MD25010 — SLAM map building and autonomous navigation
with the TurtleBot3 Waffle in Gazebo. Covers Parts B and C of the intern task set.

## Requirements

| Component | Version |
|-----------|---------|
| OS | Ubuntu 22.04 |
| ROS 2 | Humble |
| Nav2 | `ros-humble-navigation2` `ros-humble-nav2-bringup` |
| SLAM Toolbox | `ros-humble-slam-toolbox` |
| TurtleBot3 | `ros-humble-turtlebot3` `ros-humble-turtlebot3-simulations` |
| Gazebo | Classic (bundled with Humble) |

Docker is also fine — see `../Dockerfile` and `../docker-compose.yml`.
The noVNC GUI is available at `http://localhost:8080` once the container is running.

## Build

```bash
cd ~/ros2_ws
colcon build --packages-select md25010_nav
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
```

## Part B — building the map

```bash
ros2 launch md25010_nav slam.launch.py
```

Brings up Gazebo, SLAM Toolbox (lifelong mode), and RViz. Teleoperate with:

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Save when you have good coverage:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/maps/turtlebot3_map
```

## Part C — autonomous navigation

```bash
ros2 launch md25010_nav full_stack.launch.py
```

Loads the saved map with AMCL and starts Nav2 + RViz. Then either use the
**2D Goal Pose** tool in RViz manually, or run the goal sequence:

```bash
ros2 run md25010_nav send_nav_goals
```

Results are written to `/root/ros2_ws/maps/nav_goals_log.csv`.

## Layout

```
md25010_nav/
├── config/
│   ├── nav2_params.yaml
│   └── slam_params.yaml
├── launch/
│   ├── slam.launch.py
│   ├── nav2_amcl.launch.py
│   └── full_stack.launch.py
├── maps/
│   ├── turtlebot3_map.pgm
│   └── turtlebot3_map.yaml
├── md25010_nav/
│   └── send_nav_goals.py
├── package.xml
├── setup.py
└── setup.cfg
```

Parameter choices and map quality analysis are in `parameter_tuning_report.pdf`.
