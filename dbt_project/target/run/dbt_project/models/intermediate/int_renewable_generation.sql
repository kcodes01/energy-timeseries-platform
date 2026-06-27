

  create view `energy_marts_intermediate`.`int_renewable_generation__dbt_tmp` 
  
    
    
  as (
    with generation as (
    select * from `energy_marts_staging`.`stg_energy_timeseries`
    where category = 'generation'
    and filter_id in (4067, 4068, 1225)
)

select
    timestamp,
    date,
    hour_of_day,
    if(filter_id = 4067, value, 0)   as onshore_wind_mwh,
    if(filter_id = 4068, value, 0)   as solar_mwh,
    if(filter_id = 1225, value, 0)   as offshore_wind_mwh,
    value                             as total_renewable_mwh
from generation
  )