### 数据格式
- 所有的原始数据都存放在 pkl 文件里，具体内容请自己读取，格式比较简单（后续会更新具体内容）
### 数据存放
- 数据存放目录组织: 
    ```bash
    your/task/name/
    ├── teleop_data_20251219_194758_metadata.json   # json 文件中写明了 pkl 中的数据格式
    ├── teleop_data_20251219_194758.pkl             # pkl 文件中存放原始数据
    ├── teleop_data_20251219_195916_metadata.json
    ├── teleop_data_20251219_195916.pkl
    ├── ...
    └── task_name.json                              # task_name.json 存放任务的 instruction
    ```
- task_name.json 文件的格式: 
    ```bash
    [
        "task instruction 1", 
        "task instruction 2", # 一个任务可能与多种意思相同的自然语言指令, 或者只有一个也可以
        ...
    ]
    ```
### 数据转换
- 环境: (待更新)
- 将数据从原始 pkl 格式转换到 lerobot 格式
    ```bash
    # raw_data_dir: str, 原始数据路径
    # repo_id: str, 默认是 None, 会直接使用 raw_data_dir 的目录名
    # mode: str, dual / left / right
    # fps: int, 帧率
    python scripts/transform_pkl2lerobot.py 
        --raw_data_dir /path/to/your/data \
        --mode dual \
        --fps 25
    ```