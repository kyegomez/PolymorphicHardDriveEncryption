import hashlib
import os
import shutil
import subprocess
import sys
import time
from typing import Dict


class HardDriveProtector:
    """
    Initializes the HardDriveProtector object.

    Args:
        directory (str): The directory to monitor.
        backup_path (str): The path to the backup directory.
        threshold (int, optional): The threshold for detecting anomalies. Defaults to 5.
        check_interval (int, optional): The interval for checking the directory. Defaults to 10.
    """

    def __init__(
        self,
        directory: str,
        backup_path: str,
        threshold: int = 5,
        check_interval: int = 10,
    ) -> None:
        self.directory = directory
        self.backup_path = backup_path
        self.threshold = threshold
        self.check_interval = check_interval
        self.file_hashes: Dict[str, str] = {}
        self.change_count = 0

    def get_file_hash(self, file_path: str) -> str:
        """
        Returns the SHA-256 hash of the file.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The SHA-256 hash of the file.
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def monitor_directory(self) -> None:
        """
        Monitors the directory for changes.
        """
        self.file_hashes = {
            f: self.get_file_hash(os.path.join(self.directory, f))
            for f in os.listdir(self.directory)
        }
        while True:
            time.sleep(self.check_interval)
            for f in os.listdir(self.directory):
                file_path = os.path.join(self.directory, f)
                new_hash = self.get_file_hash(file_path)
                if f not in self.file_hashes:
                    print(f"New file detected: {f}")
                    self.file_hashes[f] = new_hash
                elif self.file_hashes[f] != new_hash:
                    print(f"File modified: {f}")
                    self.file_hashes[f] = new_hash
                    self.change_count += 1
                    if self.detect_anomaly():
                        self.rewrite_code()
                        self.recover_system()

    def detect_anomaly(self) -> bool:
        """
        Detects anomalies based on the threshold.

        Returns:
            bool: True if an anomaly is detected, False otherwise.
        """
        if self.change_count > self.threshold:
            print("Anomaly detected!")
            self.change_count = 0
            return True
        return False

    def rewrite_code(self) -> None:
        """
        Rewrites its code to maintain protection.
        """
        print("Rewriting code to maintain protection...")
        shutil.copy(
            os.path.join(self.backup_path, "ai_code.py"),
            os.path.abspath(__file__),
        )
        # Restart the script
        os.execv(sys.executable, ["python"] + sys.argv)

    def recover_system(self) -> None:
        """
        Recovers the system to a known good state.
        """
        print("Recovering system to a known good state...")
        backup_file = os.path.join(
            self.backup_path, "system_backup.tar.gz"
        )
        shutil.copy(backup_file, "/tmp/system_backup.tar.gz")
        subprocess.run(
            ["tar", "xzf", "/tmp/system_backup.tar.gz", "-C", "/"]
        )


# if __name__ == "__main__":
#     protector = HardDriveProtector(
#         directory="/path/to/directory",
#         backup_path="/path/to/backup",
#         threshold=5,
#         check_interval=10,
#     )
#     protector.monitor_directory()
