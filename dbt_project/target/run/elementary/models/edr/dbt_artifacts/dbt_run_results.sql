
        
  
    
    
    
        
        insert into `energy_marts`.`dbt_run_results`
        ("model_execution_id", "unique_id", "invocation_id", "generated_at", "created_at", "name", "message", "status", "resource_type", "execution_time", "execute_started_at", "execute_completed_at", "compile_started_at", "compile_completed_at", "rows_affected", "full_refresh", "compiled_code", "failures", "query_id", "thread_id", "materialization", "adapter_response")

select * from (
            select
            
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as model_execution_id

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as unique_id

,
                
        cast('dummy_string' as varchar(4096)) as invocation_id

,
                
        cast('dummy_string' as varchar(4096)) as generated_at

,
                cast('2091-02-17' as DateTime) as created_at

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as name

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as message

,
                
        cast('dummy_string' as varchar(4096)) as status

,
                
        cast('dummy_string' as varchar(4096)) as resource_type

,
                
        cast(123456789.99 as Float32) as execution_time

,
                
        cast('dummy_string' as varchar(4096)) as execute_started_at

,
                
        cast('dummy_string' as varchar(4096)) as execute_completed_at

,
                
        cast('dummy_string' as varchar(4096)) as compile_started_at

,
                
        cast('dummy_string' as varchar(4096)) as compile_completed_at

,
                
        cast(31474836478 as bigint) as rows_affected

,
                
        cast (True as boolean) as full_refresh

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as compiled_code

,
                
        cast(31474836478 as bigint) as failures

,
                
        cast('dummy_string' as varchar(4096)) as query_id

,
                
        cast('dummy_string' as varchar(4096)) as thread_id

,
                
        cast('dummy_string' as varchar(4096)) as materialization

,
                
        cast('dummy_string' as varchar(4096)) as adapter_response


        ) as empty_table
        where 1 = 0
  
    