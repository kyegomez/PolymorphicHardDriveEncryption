from phdsp.main import HardDriveProtector


protector = HardDriveProtector(
    directory="scripts",
    backup_path="scripts",
    threshold=5,
    check_interval=10,
)

protector.monitor_directory()
