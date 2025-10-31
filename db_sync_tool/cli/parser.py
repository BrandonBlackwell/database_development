import argparse
from db_sync_tool.sync.utils.logging import setup_logging
from db_sync_tool.sync.sync_manager import SyncManager
def run_cli():
    setup_logging()
    print("Hello from the CLI parser!")
    argparse.ArgumentParser(description="Database Synchronization Tool")
    argparse.add_argument('--target', type=str, required=False, help='Target database connection string')
    argparse.add_argument('sync_mode', type=str, choices=['result', 'design', 'all'], help='Synchronization mode')
    argparse.add_argument('--tables', type=str, nargs='*', help='List of tables to synchronize')
    argparse.add_argument('--file_path', type=str, help='Path to the synchronization file')
    argparse.add_argument('--start_point', type=str, help='Starting point for synchronization (e.g., timestamp or version)')
    
    args = argparse.parse_args()

    sync_manager = SyncManager(
        target=args.target,
        sync_mode=args.sync_mode,
        tables=args.tables,
        file_path=args.file_path,
        start_point=args.start_point
    )
    sync_manager.execute_sync()