- 启动机器：
    - 底盘，两个机械臂
    - 机械臂可能需要手动启动
    - 充电：正面不能被遮挡，屏幕显示是否充电
    - 走之后，要把所有东西关掉
- no machine 连接：
    - IP: xxx.xxx.xx.x
    - CMCC 网络，xxxxxxx
    - username: xx
    - password: xxx
- 底盘遥控器：
    - 开机，关机：长按中间圆形按钮
    - 前进和后退档
    - X: 平移档
    - 左边摇杆控制移动
    - B, R: 前驱，后驱
- 启动程序：
    - 启动电机：
        ```bash
        cd /home/tl/workspace/plab_controller
        cd docker 
        docker compose up
        ```
    - 旋转 base: 
        ```bash
        docker exec -it zmq_servers bash
        python plab_driver/examples/moons_motor_example.py
        ```
    - 启动相机: 
        ```bash
        cd /home/tl/workspace/ws_vision
        python vision_docker_demo/scripts/start_rest_api.py

        # 验证相机是否启动成功
        # 浏览器 -> 127.0.0.1:7000 -> 图像查看器 -> 连接 -> 查询话题
        ```
    - 启动遥操作：
        ```bash
        cd /home/tl/workspace/pxr
        bash ./scripts/start.sh
        python scripts/hardware/teleop_dual_ur5e_hardware.py

        # 启动 VR, 连接网络，启动 XRobot
        # 连接局域网
        # 勾选 controller, send
        # 把界面调整到正对机器的朝向

        # 如果有 bug，逐级重启
        # 重启遥操作脚本
        python scripts/hardware/teleop_dual_ur5e_hardware.py
        # 重启遥操作 docker
        bash ./scripts/stop.sh
        bash ./scripts/start.sh
        # 重启电机
        cd /home/tl/workspace/plab_controller
        cd docker 
        docker compose up
        # 重启整个机器
        ```
    - 录数据：
        - 按 B 开始
        - 再按一次结束
        - 数据检查：
        ```bash
            # 因为运行环境都在 docker 里面，必须进 docker 里面才能执行脚本
            docker exec -it pxr_container bash 
            cd logs
            python write_video.py --log_file /path/to/your/pkl/file
            # 这个脚本会在 logs 目录下把三个视角的图像写成三个 mp4 文件
        ```