with raw_source as (

    select *
    from {{ source('sales_dataset', 'stores') }}

),

final as (

    select
        cast(Store as int64) as store_id,
        cast(Type as string) as type,
        cast(Size as int64) as size

    from raw_source

)

select * from final
