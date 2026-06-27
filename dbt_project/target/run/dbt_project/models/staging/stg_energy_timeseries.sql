

  create view `energy_marts_staging`.`stg_energy_timeseries__dbt_tmp` 
  
    
    
  as (
    with source as (
    select * from `energy`.`raw_energy___energy_timeseries`
),

cleaned as (
    select
        timestamp,
        filter_id,
        filter_name,
        value,
        unit,
        category,
        region,
        resolution,
        ingested_at,
        -- derived columns
        toDate(timestamp)           as date,
        toHour(timestamp)           as hour_of_day,
        toDayOfWeek(timestamp)      as day_of_week,
        toMonth(timestamp)          as month,
        toYear(timestamp)           as year
    from source
    where value is not null
)

select * from cleaned
  )