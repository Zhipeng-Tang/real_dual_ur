- 主文件: 都在目录 `XRoboToolkit-Teleop-Sample-Python/scripts/hardware/`, 暂时没实现成比较统一的形式
    - `dual_arm_ur5e_launch.py`: 双臂 pi0 部署
    - `right_arm_ur5e_launch.py`: 右臂 pi0 部署
    - `dual_arm_ur5e_trajectory_replay.py`: 双臂轨迹回放 (需要手动修改代码里的 log file)
- 控制代码: 双臂 + 夹爪控制代码参考 `XRoboToolkit-Teleop-Sample-Python/xrobotoolkit_teleop/policy_controller/dual_arm_ur_gripper_controller.py`
    - **尽量不要修改这个文件**
    - 模型推理: `policy_step` 函数
- 策略代码: 目前都实现在 `XRoboToolkit-Teleop-Sample-Python/xrobotoolkit_teleop/policy_controller/policy`. 当前有
    - `TrajectoryReplayPolicy`: 双臂
    - `Pi0WebPolicy`: 单臂
    - `Pi0WebDualArmPolicy`: 双臂
- 自定义 policy: 
    - 都继承 `BasePolicy`, 重写 `step` 函数即可
    - 输入: `obs`, 在 `step` 函数中统一组织成如下形式
        ```python
        {
            "camera_head": np.array, image of head
            "camera_left_wrist": np.array, image of left wrist (optional)
            "camera_right_wrist": np.array, image of right wrist (optinal)
            "state": np.array, current state (optional)
            "prompt": np.array, language instruction (optional)
        }
        ```
    - 输出: `action, np.array`
        - 单臂情况下是 7 维数组
        - 双臂情况下是 14 维数组