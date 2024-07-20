with raw_source as (

    select *
    from {{ source('sales_dataset', 'sales') }}

),

final as (

    select
        cast(Store as int64) as store_id,
        cast(Dept as int64) as dept_id,
        cast(Date as date) as date,
        cast(Weekly_Sales as float64) as weekly_sales,
        cast(IsHoliday as boolean) as isholiday

    from raw_source

)

select * from final
