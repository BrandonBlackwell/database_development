import os

from sync.design.data_syncs import process_design_sync
from sync.result.data_syncs import process_result_sync
class SyncManager:
    """
    Coordinates sync processes.
    Sync modes: Design, Result, All
    Sync modes can be synced via different methods.
    Result strats: Files or Direct table to table using a start point
    Design strats: Files or Direct table to table using mask chip
    User flows:
    1. User selects sync mode (design, result, all)
    2. User selects sync method (files, direct)
    3. User provides necessary parameters (e.g., start point, masks, chips)
    4. SyncManager initializes appropriate sync strategy based on user input
    5. SyncManager executes the sync process
    Design flow:
    - If design sync is selected, SyncManager uses the design sync strategy
      to sync design data based on provided masks and chips.
    Result flow:
    - If result sync is selected, SyncManager uses the result sync strategy
      to sync result data based on provided start point.
    All flow:
    - If all sync is selected, SyncManager sequentially executes both design
      and result sync strategies.
    Command-line scenarios:
    Sync mode is implicitly set to all when no specific mode is provided.
        python cli.py --start_point "2023-01-01T00:00:00Z"
        python cli.py --tables "fact" --start_point "2023-01-01T00:00:00Z"
        python cli.py --tables "fact"
    When sync mode is explicitly set to design, only design sync is performed.
        python cli.py --sync-mode design --masks "mask1,mask2" --chips "chipA,chipB" --m_ids "m1,m2"
    When sync mode is set to result and masks/chips/m_ids are provided, they are used for filtering result sync.
        python cli.py --sync-mode result --masks "mask1,mask2" --chips "chipA,chipB" --m_ids "m1,m2"
    When sync mode is set to all, a start point, a file, or a mask/chip/m_id combo is required.
        python cli.py --sync-mode "all" --start_point "2023-01-01T00:00:00Z"
    Sync's result using files located in ingest directory.
        python cli.py --sync-mode result --directory true
    Sync's design using files located in ingest directory.
        python cli.py --sync-mode design --directory true
    Other possible example commands:
        python cli.py --sync-mode result --start_point "2023-01-01T00:00:00Z"
        python cli.py --sync-mode result --target-db-url "mysql://user:pass@host/db" --db-type "maria" --tables "fact" --directory "/path/to/sync/dir" --start_point "2023-01-01T00:00:00Z"

    
    """
    def __init__(
        self,
        source_engine,
        target_engine,
        db_settings,
        db_type,
        target_db, 
        sync_mode, 
        tables=None, 
        directory=None, 
        start_point=None, 
        masks=None, 
        chips=None, 
        m_ids=None
    ):
        self.source_engine = source_engine
        self.target_engine = target_engine
        self.db_settings = db_settings
        self.db_type = db_type
        self.target_db = target_db
        self.sync_mode = sync_mode
        self.tables = tables
        self.directory = directory
        self.start_point = start_point
        self.masks = masks
        self.chips = chips
        self.m_ids = m_ids

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
        # design_data_source = fetch_design_data(source_db)
        # update_design_data_target(target_db, transformed_data)
        # Warn if no table masks are provided for design sync
        if not self.masks:
            print("No table masks specified; all design tables will be synchronized.")
        process_design_sync(self.target_db, self.tables, self.directory, self.masks, self.chips, self.m_ids)
        
    async def process_design_sync(target_db, tables, directory, masks, chips, m_ids):
        # Placeholder function to process design synchronization
        # Sync device tables
        sync_device_tables(target_db, tables, directory, chips, m_ids)
        # Sync design tables
        sync_design_tables(target_db, tables, directory, masks)
        # Sync design fact
        sync_design_fact(target_db, tables, directory, masks, chips, m_ids)
        print(f"Processing design sync for target_db: {target_db}, tables: {tables}, directory: {directory}, masks: {masks}, chips: {chips}, m_ids: {m_ids}")
    
    async def sync_result_v1(self):
        # FACT TO FACT SYNC OPTIMIZATION STRATEGY
        # User must specify start point for result sync
        if self.sync_mode == 'result' and 'fact' in self.tables and not self.start_point:
            raise ValueError("Start point must be specified when synchronizing 'fact' tables.")
        process_result_sync(self.target_db, self.tables, self.directory, self.start_point)
        """
        This approach reduces the number of database calls and improves performance.
        Grabs prod data in bulk and processes foreign keys in batches.
        We can implement one of the following two solutions:
        Solution 1: Pre-fetch all required dimension data before inserting fact data.
        
        Below is a pseudocode outline for Solution 1:
        Loads dimension data in bulk before inserting fact data.
        Example:
        source_db = connect_to_database(source_config)
        target_db = connect_to_database(target_config)
        prod_data = fetch_prod_data(source_db, start_point)
        """
        # Batch processing of foreign keys
        fk_batches = {}
        for fact_record in prod_data:
            dim_keys = extract_dimension_keys(fact_record)  # e.g., {'dim_table1': fk1, 'dim_table2': fk2}
            
            for dim_table, fk in dim_keys.items():
                if dim_table not in fk_batches:
                    fk_batches[dim_table] = set().add(fk)
                else:
                    fk_batches[dim_table].add(fk)
                    
        # Sync device tables
        sync_device_tables(source_db, target_db, fk_batches["device"])
        
        # Grab design fact data in bulk
        design_fact_data = fetch_design_fact_data_source(source_db, fk_batches["design"], fk_batches["device"])
        insert_design_fact_data_target(target_db, design_fact_data)
        
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

    async def sync_result_v2(self):
        """        
        Solution 2: Batch process foreign keys while inserting fact data.
        This approach processes foreign keys in batches during fact data insertion.
        Example pseudocode:
        source_db = connect_to_database(source_config)
        target_db = connect_to_database(target_config)
        prod_fact_data = fetch_prod_fact_data(source_db, start_point)
        insert_fact_data_batch(target_db, prod_data, batch_size=1000)
        get_dim_data_batch(dim_table, fk_batch)
        insert_dim_data_batch(target_db, dim_table, dim_data_batch)
        """
        pass

    async def sync_result_sql(self):
        # Uses sql dump files to sync result data
        # This function would handle the synchronization of result data
        # using SQL dump files to transfer data between databases.
        # For example:
        # 1. Generate SQL dump files from the source database.
        # 2. Transfer the SQL dump files to the target database environment.
        # 3. Execute the SQL dump files to insert or update data in the target database.
        # Example pseudocode:
        # generate_sql_dump(source_db, dump_file_path)
        # transfer_dump_to_target(dump_file_path, target_env)
        # execute_sql_dump(target_db, dump_file_path)
        sql_dir = 'migration_scripts/'

        for filename in os.listdir(sql_dir):
            if filename.endswith(".sql"):
                sql_path = os.path.join(sql_dir, filename)
                tmp_path = sql_path + ".tmp.sql"

                enable_fk_checks = "\nSET FOREIGN_KEY_CHECKS=1;\nCOMMIT;\n"
                disable_fk_checks = "SET FOREIGN_KEY_CHECKS=0;\n"

        with open(tmp_path, 'w') as tmp_file:
            tmp_file.write(disable_fk_checks)
            with open(sql_path, 'r') as sql_file:
                for line in sql_file:
                    tmp_file.write(line)
            tmp_file.write(enable_fk_checks)
            subprocess.run(['mysql', '-u', user, f'-p{password}', database_name], 
                           stdin=open(tmp_path, 'r'))
            
    async def sync_tables(self):
        """ Sync individual tables based on user selection """
        for table in self.tables:
            if table == 'table_one':
                sync_table_one(self.source_engine, self.target_engine, self.db_settings)
            if table == 'table_two':
                sync_table_two(self.source_engine, self.target_engine, self.db_settings)
            if table == 'table_three':
                sync_table_three(self.source_engine, self.target_engine, self.db_settings)
                