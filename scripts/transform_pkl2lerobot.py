"""
UR Dual Arm Data to LeRobot V3 Dataset Converter
"""

import os
import glob
import pickle
import numpy as np
import torch
import draccus
import json
import random
from dataclasses import dataclass
from pathlib import Path
TASKDESCRIPTION = "Scoop out the salt and pour it onto white paper."
try:
    from scipy.spatial.transform import Rotation as R
except ImportError:
    print("please install scipy: pip install scipy")
    exit(1)

try:
    from lerobot.datasets.lerobot_dataset import LeRobotDataset
except ImportError:
    print("please install lerobot: pip install lerobot")
    exit(1)

@dataclass
class Args: 
    raw_data_dir: str = None
    repo_id: str = None
    fps: int = 25               # 数据帧率

    mode: str = "dual"          # 模式: dual / left / right, dual 代表双臂的数据都会被转换, left / right 代表只有单臂的数据会被转换

    def check(self): 
        assert self.mode in ["dual", "left", "right"], "Invalid mode: {}, mode must be dual / left / right.".format(self.mode)
        assert os.path.exists(os.path.join(self.raw_data_dir, "task_name.json")), "task_name.json not exist!"

def load_raw_episodes(data_dir):
    """读取所有 .pkl 文件"""
    pkl_files = sorted(glob.glob(os.path.join(data_dir, "*.pkl")))
    print(f"找到 {len(pkl_files)} 个数据文件。")
    
    for pkl_path in pkl_files:
        try:
            with open(pkl_path, "rb") as f:
                data = pickle.load(f)
            if isinstance(data, list) and len(data) > 0:
                yield pkl_path, data
            else:
                print(f"跳过无效文件: {pkl_path}")
        except Exception as e:
            print(f"读取错误 {pkl_path}: {e}")

def process_frame(frame, use_left, use_right):
    """
    parse data of single frame
    """
    # --- 1. Gripper ---
    left_grip_pos = frame["dual_gripper"]["left_gripper"]["position"] 
    right_grip_pos = frame["dual_gripper"]["right_gripper"]["position"]
    
    left_grip_arr = np.array([left_grip_pos], dtype=np.float32)
    right_grip_arr = np.array([right_grip_pos], dtype=np.float32)

    # --- 2. State ---
    # q_actual (6) + Gripper (1)
    left_q = np.array(frame["dual_arm_ur"]["left_arm"]["q_actual"], dtype=np.float32)
    right_q = np.array(frame["dual_arm_ur"]["right_arm"]["q_actual"], dtype=np.float32)
    
    if use_left and use_right: 
        state = np.concatenate([left_q, left_grip_arr, right_q, right_grip_arr])
    elif use_left: 
        state = np.concatenate([left_q, left_grip_arr])
    elif use_right: 
        state = np.concatenate([right_q, right_grip_arr])

    # --- 3. Action ---
    left_target = np.array(frame["dual_arm_ur"]["left_arm"]["q_target"], dtype=np.float32)
    right_target = np.array(frame["dual_arm_ur"]["right_arm"]["q_target"], dtype=np.float32)
    if use_left and use_right: 
        action = np.concatenate([
            left_target, left_grip_arr, right_target, right_grip_arr
        ])
    elif use_left: 
        action = np.concatenate([
            left_target, left_grip_arr
        ])
    elif use_right: 
        action = np.concatenate([
            right_target, right_grip_arr
        ])

    # --- 4. Image ---
    imgs = frame["cameras"]["images"]
    images = {
        "head": imgs["head"],
    }
    if use_left: 
        images.update({"left_wrist": imgs["left_wrist"]})
    if use_right: 
        images.update({"right_wrist": imgs["right_wrist"]})

    return state, action, images


@draccus.wrap()
def main(args: Args): 
    args.check()

    # LeRobot dataset feature
    features = {
        # --- image ---
        "observation.images.head": {
            "dtype": "video",
            "shape": (400, 720, 3),
            "names": ["height", "width", "channel"],
        },
    }


    if args.mode == "dual": 
        features.update(
            {
                "observation.images.left_wrist": {
                    "dtype": "video",
                    "shape": (360, 720, 3),
                    "names": ["height", "width", "channel"],
                }, 
                "observation.images.right_wrist": {
                    "dtype": "video",
                    "shape": (360, 720, 3),
                    "names": ["height", "width", "channel"],
                }, 
                # --- State ---
                "observation.state": {
                    "dtype": "float32",
                    "shape": (14,),
                    "names": [
                        "left_j0", "left_j1", "left_j2", "left_j3", "left_j4", "left_j5", "left_gripper", 
                        "right_j0", "right_j1", "right_j2", "right_j3", "right_j4", "right_j5", "right_gripper"
                    ],
                },
                # --- Action ---
                "action": {
                    "dtype": "float32",
                    "shape": (14,),
                    "names": [
                        "left_j0", "left_j1", "left_j2", "left_j3", "left_j4", "left_j5", "left_gripper", 
                        "right_j0", "right_j1", "right_j2", "right_j3", "right_j4", "right_j5", "right_gripper"
                    ],
                },
            }
        )
    elif args.mode == "left": 
        features.update(
            {
                "observation.images.left_wrist": {
                    "dtype": "video",
                    "shape": (360, 720, 3),
                    "names": ["height", "width", "channel"],
                }, 
                # --- State ---
                "observation.state": {
                    "dtype": "float32",
                    "shape": (7,),
                    "names": [
                        "left_j0", "left_j1", "left_j2", "left_j3", "left_j4", "left_j5", "left_gripper", 
                    ],
                },
                # --- Action ---
                "action": {
                    "dtype": "float32",
                    "shape": (7,),
                    "names": [
                        "left_j0", "left_j1", "left_j2", "left_j3", "left_j4", "left_j5", "left_gripper", 
                    ],
                },
            }
        )
    elif args.mode == "right": 
        features.update(
            {
                "observation.images.right_wrist": {
                    "dtype": "video",
                    "shape": (360, 720, 3),
                    "names": ["height", "width", "channel"],
                }, 
                # --- State ---
                "observation.state": {
                    "dtype": "float32",
                    "shape": (7,),
                    "names": [
                        "right_j0", "right_j1", "right_j2", "right_j3", "right_j4", "right_j5", "right_gripper"
                    ],
                },
                # --- Action ---
                "action": {
                    "dtype": "float32",
                    "shape": (7,),
                    "names": [
                        "right_j0", "right_j1", "right_j2", "right_j3", "right_j4", "right_j5", "right_gripper"
                    ],
                },
            }
        )

    repo_id = args.repo_id if args.repo_id is not None else Path(args.raw_data_dir).name
    print(f"Creating LeRobot dataset: {repo_id}")
    print(f"FPS: {args.fps}")
    
    dataset = LeRobotDataset.create(
        repo_id=repo_id,
        fps=args.fps,
        features=features,
        use_videos=True,
    )

    episode_idx = 0
    total_frames = 0

    task_name_list = json.load(
        open(os.path.join(args.raw_data_dir, "task_name.json"), "r")
    )
    import pdb; pdb.set_trace()

    use_left = (args.mode == "dual") or (args.mode == "left")
    use_right = (args.mode == "dual") or (args.mode == "right")

    for pkl_path, raw_frames in load_raw_episodes(args.raw_data_dir):
        num_frames = len(raw_frames)
        print(f"Processing Ep {episode_idx}: {os.path.basename(pkl_path)} {num_frames}")
        
        for frame in raw_frames:
            state, action, images = process_frame(frame, use_left, use_right)
            
            frame_data = {
                "observation.state": torch.from_numpy(state),
                "action": torch.from_numpy(action),
                "observation.images.head": images["head"],
                "task": random.choice(task_name_list),
            }
            if use_left: 
                frame_data.update({"observation.images.left_wrist": images["left_wrist"]})
            if use_right: 
                frame_data.update({"observation.images.right_wrist": images["right_wrist"]})
            dataset.add_frame(frame_data)
            total_frames += 1

        dataset.save_episode()
        episode_idx += 1

    print(f"\nFinish all data: {episode_idx} Episodes, {total_frames} Frames.")
    
    
    print(f"\ndataset path: {dataset.root}")

if __name__ == "__main__":
    main()