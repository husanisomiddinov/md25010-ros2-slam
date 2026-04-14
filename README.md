# MD25010 — ROS2 SLAM

Intern onboarding task for grant project MD25010 at New Uzbekistan University. The task was basically to get a full SLAM + autonomous navigation pipeline running using ROS2 and Nav2, using a TurtleBot3 in Gazebo simulation.

---

## Requirements

- Docker Desktop
- If you're on Apple Silicon, go to Docker Desktop → Settings → General and enable **"Use Rosetta for x86/amd64 emulation"**. Without this Gazebo just crashes.

---

## How to run

```bash
docker-compose build
docker-compose up -d
```

Then open `http://localhost:8080/vnc.html` in your browser, password is `password`. That gives you the desktop where Gazebo and RViz will show up.

### Part A - launch everything

You need 3 separate terminals inside the container. Open them with `docker exec -it md25010_ros2 bash` in separate tabs.

```bash
# terminal 1
source /opt/ros/humble/setup.bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# terminal 2
source /opt/ros/humble/setup.bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True

# terminal 3
source /opt/ros/humble/setup.bash
ros2 launch nav2_bringup rviz_launch.py
```

Gazebo takes like 40 seconds to load, don't panic.

### Part B - build the map

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Drive around the whole environment with WASD until the map in RViz looks complete. Then save it:

```bash
ros2 run nav2_map_server map_saver_cli -f /root/ros2_ws/maps/turtlebot3_map
```

### Part C - autonomous navigation

Kill the SLAM toolbox terminal first, then:

```bash
# load the saved map with AMCL localization
ros2 launch nav2_bringup bringup_launch.py use_sim_time:=True map:=/root/ros2_ws/maps/turtlebot3_map.yaml

# send 5 navigation goals
python3 /root/ros2_ws/scripts/send_nav_goals.py
```

---

## Files

```
Dockerfile                  - the container setup
docker-compose.yml          - ports, volumes, display config
maps/turtlebot3_map.pgm     - the actual map image
maps/turtlebot3_map.yaml    - map metadata (resolution, origin etc)
maps/nav_goals_log.csv      - results from part C
scripts/send_nav_goals.py   - script that sends the 5 goals
```

---

## Navigation results

5/5 goals reached:

| goal | x, y | time |
|------|------|------|
| goal_1 | 1.5, 0.0 | 135s |
| goal_2 | 1.5, 1.5 | 61s |
| goal_3 | -1.0, 1.5 | 33s |
| goal_4 | -1.0, -1.0 | 78s |
| goal_5_home | 0.0, 0.0 | 39s |

---

## Things worth knowing

- `LIBGL_ALWAYS_SOFTWARE=1` is set in the Dockerfile because there's no GPU in Docker, Gazebo needs software rendering
- `models.gazebosim.org` is blocked in /etc/hosts inside the container — Gazebo tries to fetch models from the internet on startup and just hangs for a minute if you don't do this
