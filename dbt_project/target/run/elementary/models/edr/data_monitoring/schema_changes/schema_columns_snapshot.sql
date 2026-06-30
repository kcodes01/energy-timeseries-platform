
        
  
    
    
    
        
        insert into `energy_marts`.`schema_columns_snapshot`
        ("column_state_id", "full_column_name", "full_table_name", "column_name", "data_type", "is_new", "detected_at", "created_at")


    select * from (
            select
            
                
        cast('dummy_string' as varchar(4096)) as column_state_id

,
                
        cast('dummy_string' as varchar(4096)) as full_column_name

,
                
        cast('dummy_string' as varchar(4096)) as full_table_name

,
                
        cast('dummy_string' as varchar(4096)) as column_name

,
                
        cast('dummy_string' as varchar(4096)) as data_type

,
                
        cast (True as boolean) as is_new

,
                cast('2091-02-17' as DateTime) as detected_at

,
                cast('2091-02-17' as DateTime) as created_at


        ) as empty_table
        where 1 = 0

  
    