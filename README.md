## 1 数据录制
Please refer to [data_record](docs/data_record.md) 
- 数据录制脚本: 
    ```bash
    # --log-dir: 数据存放目录
    # --enable-right-dir: 是否允许右夹爪闭合，在使用勺子的时候需要关闭，防止出错
    python scripts/hardware/teleop_dual_ur5e_hardware.py --log-dir /path/to/your/data/dir --enable-right-trigger

    # 回到某一条数据的初始位置，使得所有数据的初始位置严格相同
    # --log-file: 数据的路径
    python scripts/hardware/dual_arm_ur5e_back_to_initial_pos.py --log-file /path/to/pkl/file 

    # 轨迹回放，用于验证轨迹正确性
    python scripts/hardware/dual_arm_ur5e_trajectory_replay.py --log-file /path/to/pkl/file
    
    # 渲染数据中的图像，用于检查数据正确性
    cd logs
    python write_video.py --log_file /path/to/your/pkl/file
    ```
## 2 数据格式，存放和格式转换
Please refer to [data_format_storage_transform](docs/data_format_storage_transform.md)
## 3 模型部署: 
Please refer to [deployment](docs/deployment.md)