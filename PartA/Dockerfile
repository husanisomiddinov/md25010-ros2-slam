FROM osrf/ros:humble-desktop-full

RUN apt-get update && apt-get install -y \
    git nano vim wget curl \
    python3-pip \
    python3-colcon-common-extensions \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-turtlebot3 \
    ros-humble-turtlebot3-msgs \
    ros-humble-turtlebot3-simulations \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    novnc websockify tigervnc-standalone-server fluxbox xterm \
    libgl1-mesa-dri libgl1-mesa-glx mesa-utils \
    && rm -rf /var/lib/apt/lists/*

ENV TURTLEBOT3_MODEL=waffle
ENV GAZEBO_MODEL_PATH=/opt/ros/humble/share/turtlebot3_gazebo/models
ENV LIBGL_ALWAYS_SOFTWARE=1
ENV GALLIUM_DRIVER=softpipe
ENV MESA_GL_VERSION_OVERRIDE=3.3

WORKDIR /root/ros2_ws
RUN mkdir -p src maps

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /root/ros2_ws/install/setup.bash 2>/dev/null || true" >> ~/.bashrc && \
    echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc && \
    echo "export LIBGL_ALWAYS_SOFTWARE=1" >> ~/.bashrc && \
    echo "export GALLIUM_DRIVER=softpipe" >> ~/.bashrc && \
    echo "export GAZEBO_MODEL_PATH=/opt/ros/humble/share/turtlebot3_gazebo/models" >> ~/.bashrc

CMD ["bash"]
