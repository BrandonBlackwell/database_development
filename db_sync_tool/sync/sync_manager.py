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
        if not self.masks:
            print("No table masks specified; all design tables will be synchronized.")
        process_design_sync(self.target_db, self.tables, self.directory, self.start_point, self.masks)
    
    async def sync_result(self):
        # User must specify start point for result sync
        if self.sync_mode == 'result' and 'fact' in self.tables and not self.start_point:
            raise ValueError("Start point must be specified when synchronizing 'fact' tables.")
        process_result_sync(self.target_db, self.tables, self.directory, self.start_point)
        
        #  This approach reduces the number of database calls and improves performance.
        # Example pseudocode for solution 2:
        source_db = connect_to_database(source_config)
        target_db = connect_to_database(target_config)
        prod_data = fetch_prod_data(source_db, start_point)
        
        # Batch processing of foreign keys
        fk_batches = {}
        for fact_record in prod_data:
            dim_keys = extract_dimension_keys(fact_record)  # e.g., {'dim_table1': fk1, 'dim_table2': fk2}
            
            for dim_table, fk in dim_keys.items():
                if dim_table not in fk_batches:
                    fk_batches[dim_table] = set().add(fk)
                else:
                    fk_batches[dim_table].add(fk)
        # Grab design fact data in bulk
        design_fact_data = fetch_design_fact_data_bulk(source_db, fk_batches["design"], fk_batches["device"])
        insert_design_fact_data_bulk(target_db, design_fact_data)
        
        # Gathers raw data for all required dimension tables in bulk
        dim_data = {}
        for dim_table, fks in fk_batches.items():
            # fetches all required dimension data in bulk
            dim_data[dim_table] = get_dim_data_bulk(dim_table, fks)
        # Inserts all dimension data into target db in bulk
        for dim_table, dim_data in dim_data.items():
            insert_dim_data_bulk(target_db, dim_table, dim_data[dim_table])
        # Finally, insert fact data referencing the pre-fetched dimension data
        insert_fact_data(target_db, fact_record, prod_data)


            
