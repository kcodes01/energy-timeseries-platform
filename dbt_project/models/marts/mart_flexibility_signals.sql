with prices as (
    select
        timestamp,
        date,
        hour_of_day,
        value as price_eur_mwh
    from {{ ref('stg_energy_timeseries') }}
    where category = 'price'
    and filter_id = 4169
),

residual as (
    select * from {{ ref('int_residual_load') }}
),

renewables as (
    select * from {{ ref('int_renewable_generation') }}
),

joined as (
    select
        p.timestamp                 as timestamp,
        p.date                      as date,
        p.hour_of_day               as hour_of_day,
        p.price_eur_mwh             as price_eur_mwh,
        r.residual_load_mwh         as residual_load_mwh,
        r.renewable_pct             as renewable_pct,
        rn.total_renewable_mwh      as total_renewable_mwh,
        multiIf(
            p.price_eur_mwh < 50 and r.renewable_pct > 50, 'OPTIMAL',
            p.price_eur_mwh < 80 and r.renewable_pct > 30, 'GOOD',
            p.price_eur_mwh > 150, 'AVOID',
            'NEUTRAL'
        )                           as consumption_signal
    from prices p
    left join residual r on p.timestamp = r.timestamp
    left join renewables rn on p.timestamp = rn.timestamp
)

select * from joined
order by joined.timestamp desc
