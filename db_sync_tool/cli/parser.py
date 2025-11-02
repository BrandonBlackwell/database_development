import argparse
from db_sync_tool.sync.utils.logging import setup_logging
from db_sync_tool.sync.sync_manager import SyncManager
async def run_cli():
    setup_logging()
    print("Hello from the CLI parser!")
    argparse.ArgumentParser(description="Database Synchronization Tool")
    argparse.add_argument('sync_mode', type=str, choices=['result', 'design', 'all'], help='Synchronization mode')
    argparse.add_argument('--target-db', type=str, required=False, help='Target database connection string')
    argparse.add_argument('--db-type', type=str, choices=['maria', 'mongo', 'sqlite'], help='Type of the target database')
    argparse.add_argument('--tables', type=str, nargs='*', help='List of tables to synchronize')
    argparse.add_argument('--directory', type=str, help='Path to the synchronization directory')
    argparse.add_argument('--start_point', type=str, help='Starting point for synchronization (e.g., timestamp or version)')
    argparse.add_argument('--masks', type=str, help='Mask names to filter tables for design synchronization')

    
    args = argparse.parse_args()

    sync_manager = SyncManager(
        sync_mode=args.sync_mode,
        target_db=args.target_db,
        tables=args.tables,
        directory=args.directory,
        start_point=args.start_point
    )
        
    sync_manager.execute_sync()