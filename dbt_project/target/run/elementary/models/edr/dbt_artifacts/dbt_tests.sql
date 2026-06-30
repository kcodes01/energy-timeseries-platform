
        
  
    
    
    
        
        insert into `energy_marts`.`dbt_tests`
        ("unique_id", "database_name", "schema_name", "name", "short_name", "alias", "test_column_name", "severity", "warn_if", "error_if", "test_params", "test_namespace", "tags", "model_tags", "model_owners", "meta", "depends_on_macros", "depends_on_nodes", "parent_model_unique_id", "description", "package_name", "type", "original_path", "path", "generated_at", "metadata_hash", "quality_dimension")

select * from (
            select
            
                
        cast('dummy_string' as varchar(4096)) as unique_id

,
                
        cast('dummy_string' as varchar(4096)) as database_name

,
                
        cast('dummy_string' as varchar(4096)) as schema_name

,
                
        cast('dummy_string' as varchar(4096)) as name

,
                
        cast('dummy_string' as varchar(4096)) as short_name

,
                
        cast('dummy_string' as varchar(4096)) as alias

,
                
        cast('dummy_string' as varchar(4096)) as test_column_name

,
                
        cast('dummy_string' as varchar(4096)) as severity

,
                
        cast('dummy_string' as varchar(4096)) as warn_if

,
                
        cast('dummy_string' as varchar(4096)) as error_if

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as test_params

,
                
        cast('dummy_string' as varchar(4096)) as test_namespace

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as tags

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as model_tags

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as model_owners

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as meta

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as depends_on_macros

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as depends_on_nodes

,
                
        cast('dummy_string' as varchar(4096)) as parent_model_unique_id

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as description

,
                
        cast('dummy_string' as varchar(4096)) as package_name

,
                
        cast('dummy_string' as varchar(4096)) as type

,
                
        cast('this_is_just_a_long_dummy_string' as varchar(4096)) as original_path

,
                
        cast('dummy_string' as varchar(4096)) as path

,
                
        cast('dummy_string' as varchar(4096)) as generated_at

,
                
        cast('dummy_string' as varchar(4096)) as metadata_hash

,
                
        cast('dummy_string' as varchar(4096)) as quality_dimension


        ) as empty_table
        where 1 = 0
  
    