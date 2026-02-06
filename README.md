## 1 数据录制
Please refer to [data_record](docs/data_record.md) 
- 数据录制脚本: 
    ```bash
    # --log-dir: 数据存放目录
    # --enable-right-trigger: 是否允许右夹爪闭合
    # --no-enable-right-trigger: 在使用勺子的时候需要关闭，防止出错
    python scripts/hardware/teleop_dual_ur5e_hardware.py --log-dir /path/to/your/data/dir --enable-right-trigger

    # 录制数据并自动回到初始位置
    # --log_file: 读取初始位姿的数据路径
    python scripts/hardware/teleop_dual_ur5e_hardware_back_to_init.py --log_file /path/to/pkl/file 

    # 回到某一条数据的初始位置，使得所有数据的初始位置严格相同
    # --log-file: 数据的路径
    python scripts/hardware/dual_arm_ur5e_back_to_initial_pos.py --log-file /path/to/pkl/file 

    # 轨迹回放，用于验证轨迹正确性
    python scripts/hardware/dual_arm_ur5e_trajectory_replay.py --log-file /path/to/pkl/file
    
    # 渲染数据中的图像，用于检查数据正确性(单个数据)
    cd logs
    python write_video.py --log_file /path/to/your/pkl/file

    # 渲染数据中的图像，用于检查数据正确性(多个数据)
    # 持续监测 logs 文件夹下出现的成对数据
    # 并将（数据对+视频文件+质量曲线图）放到logs/tmp下的同名文件夹里
    # 按 control+C 退出监测
    cd logs
    python write_video_multi.py
    ```
## 2 数据格式，存放和格式转换
Please refer to [data_format_storage_transform](docs/data_format_storage_transform.md)
## 3 模型部署 
Please refer to [deployment](docs/deployment.md)
## 4 注意事项
- 录有勺子的数据时，需要关闭右夹爪闭合: `--no-enable-right-trigger`
- 录数据过程中一定要时不时检查数据是否正确，图像是否正常
- 关机时，先给机械臂断电，再关闭电源
- 超过三周不使用时，需打开左侧面外壳，关闭四个电闸