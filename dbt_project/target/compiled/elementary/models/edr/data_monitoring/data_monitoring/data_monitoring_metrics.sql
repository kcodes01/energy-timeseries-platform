


    
    
        
    
    select * from (
            select
            
                
        cast('dummy_string' as varchar(4096)) as id

,
                
        cast('dummy_string' as varchar(4096)) as full_table_name

,
                
        cast('dummy_string' as varchar(4096)) as column_name

,
                
        cast('dummy_string' as varchar(4096)) as metric_name

,
                
        cast(123456789.99 as Float32) as metric_value

,
                
        cast('dummy_string' as varchar(4096)) as source_value

,
                cast('2091-02-17' as DateTime) as bucket_start

,
                cast('2091-02-17' as DateTime) as bucket_end

,
                
        cast(123456789 as Int32) as bucket_duration_hours

,
                cast('2091-02-17' as DateTime) as updated_at

,
                
        cast('dummy_string' as varchar(4096)) as dimension

,
                
        cast('dummy_string' as varchar(4096)) as dimension_value

,
                
        cast('dummy_string' as varchar(4096)) as metric_properties

,
                cast('2091-02-17' as DateTime) as created_at


        ) as empty_table
        where 1 = 0
