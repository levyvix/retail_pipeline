with raw_source as (

    select *
    from {{ source('sales_dataset', 'features') }}

),

final as (

    select
        cast(Store as int64) as store_id,
        cast(Date as date) as date,
        cast(Temperature as float64) as temperature,
        cast(Fuel_Price as float64) as fuel_price,
        cast(MarkDown1 as string) as markdown1,
        cast(MarkDown2 as string) as markdown2,
        cast(MarkDown3 as string) as markdown3,
        cast(MarkDown4 as string) as markdown4,
        cast(MarkDown5 as string) as markdown5,
        cast(CPI as string) as cpi,
        cast(Unemployment as string) as unemployment,
        cast(IsHoliday as boolean) as isholiday

    from raw_source

)

select * from final
