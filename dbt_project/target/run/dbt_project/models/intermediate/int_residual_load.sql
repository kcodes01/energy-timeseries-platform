

  create or replace view `energy_marts_intermediate`.`int_residual_load` 
  
    
  
  
    
    
  as (
    with consumption as (
    select
        timestamp,
        date,
        hour_of_day,
        sumIf(value, filter_id = 410)   as total_load_mwh,
        sumIf(value, filter_id = 4359)  as residual_load_mwh
    from `energy_marts_staging`.`stg_energy_timeseries`
    where category = 'consumption'
    group by timestamp, date, hour_of_day
)

select
    timestamp,
    date,
    hour_of_day,
    total_load_mwh,
    residual_load_mwh,
    -- renewable coverage
    total_load_mwh - residual_load_mwh  as renewable_coverage_mwh,
    round(
        (total_load_mwh - residual_load_mwh) / nullIf(total_load_mwh, 0) * 100, 2
    )                                    as renewable_pct
from consumption
order by timestamp
    
  )
      
      
                    -- end_of_sql
                    
                    