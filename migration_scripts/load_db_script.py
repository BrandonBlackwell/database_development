import os
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

    
    