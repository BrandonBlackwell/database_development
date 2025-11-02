from sync.design.data_syncs import process_design_sync
from sync.result.data_syncs import process_result_sync
class SyncManager:
    def __init__(self, target_db, sync_mode, tables=None, directory=None, start_point=None, masks=None):
        self.target_db = target_db
        self.sync_mode = sync_mode
        self.tables = tables
        self.directory = directory
        self.start_point = start_point
        self.masks = masks

    # Use the Strategy design pattern to select the sync strategy based on sync_mode
    async def execute_sync(self):
        strategies = {
            'design': self.sync_design,
            'result': self.sync_result,
            'all': self._sync_all
        }
        strategy = strategies.get(self.sync_mode)
        if strategy:
            await strategy()
        else:
            raise ValueError(f"Unknown sync mode: {self.sync_mode}")

    async def _sync_all(self):
        await self.sync_design()
        await self.sync_result()
    
    
    async def sync_design(self):
        # Placeholder for design synchronization logic
        # This function would handle the synchronization of design data
        # between different database systems or environments.
        # For example:
        # 1. Connect to source and target databases using configuration settings.
        # 2. Fetch design data from the source database.
        # 3. Transform the data if necessary to match the target database schema.
        # 4. Insert or update the design data in the target database.
        # Example pseudocode:
        # source_db = connect_to_database(source_config)
        # target_db = connect_to_database(target_config)
        # design_data = fetch_design_data(source_db)
        # transformed_data = transform_design_data(design_data)
        # update_design_data(target_db, transformed_data)
        # Warn if no table masks are provided for design sync
        if self.sync_mode == 'design' and not self.masks:
            print("No table masks specified; all design tables will be synchronized.")
        process_design_sync(self.target_db, self.tables, self.directory, self.start_point, self.masks)
    
    async def sync_result(self):
        # Placeholder for result synchronization logic
        # This function would handle the synchronization of result data
        # between different database systems or environments.
        # Similar steps as in sync_design would be followed here.
        # User must specify start point for result sync
        if self.sync_mode == 'result' and 'fact' in self.tables and not self.start_point:
            raise ValueError("Start point must be specified when synchronizing 'fact' tables.")
        process_result_sync(self.target_db, self.tables, self.directory, self.start_point)
