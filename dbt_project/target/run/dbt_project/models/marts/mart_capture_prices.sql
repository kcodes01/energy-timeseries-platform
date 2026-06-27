
  
    
    
    
        
        insert into `energy_marts_marts`.`mart_capture_prices__dbt_backup`
        ("date", "capture_price_eur_mwh", "avg_market_price_eur_mwh", "total_renewable_mwh", "solar_mwh", "onshore_wind_mwh", "offshore_wind_mwh")with base as (
    select
        p.date                                      as date,
        p.value                                     as price_eur_mwh,
        r.onshore_wind_mwh                          as onshore_wind_mwh,
        r.solar_mwh                                 as solar_mwh,
        r.offshore_wind_mwh                         as offshore_wind_mwh,
        r.total_renewable_mwh                       as total_renewable_mwh,
        p.value * r.total_renewable_mwh             as weighted_price
    from `energy_marts_staging`.`stg_energy_timeseries` p
    left join `energy_marts_intermediate`.`int_renewable_generation` r
        on p.timestamp = r.timestamp
    where p.category = 'price'
    and p.filter_id = 4169
),

aggregated as (
    select
        date,
        sum(weighted_price)         as sum_weighted_price,
        sum(total_renewable_mwh)    as sum_renewable_mwh,
        avg(price_eur_mwh)          as avg_price,
        sum(solar_mwh)              as sum_solar,
        sum(onshore_wind_mwh)       as sum_onshore,
        sum(offshore_wind_mwh)      as sum_offshore
    from base
    group by date
)

select
    date,
    round(sum_weighted_price / sum_renewable_mwh, 2)    as capture_price_eur_mwh,
    round(avg_price, 2)                                  as avg_market_price_eur_mwh,
    round(sum_renewable_mwh, 0)                         as total_renewable_mwh,
    round(sum_solar, 0)                                 as solar_mwh,
    round(sum_onshore, 0)                               as onshore_wind_mwh,
    round(sum_offshore, 0)                              as offshore_wind_mwh
from aggregated
order by date desc
  
  