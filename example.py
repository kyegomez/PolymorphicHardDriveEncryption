from phdsp.main import HardDriveProtector


protector = HardDriveProtector(
    directory="/path/to/directory",
    backup_path="/path/to/backup",
    threshold=5,
    check_interval=10,
)
protector.monitor_directory()
