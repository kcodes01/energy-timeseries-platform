
        
  
    
    
    
        
        insert into `energy_marts`.`test_result_rows`
        ("elementary_test_results_id", "result_row", "detected_at", "created_at")

-- depends_on: `energy_marts`.`elementary_test_results`
select * from (
            select
            
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as elementary_test_results_id

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as result_row

,
                cast('2091-02-17' as DateTime) as detected_at

,
                cast('2091-02-17' as DateTime) as created_at


        ) as empty_table
        where 1 = 0
  
    