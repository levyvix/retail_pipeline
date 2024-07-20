with stores as (
	select *
	from {{ ref("int__stores")}}
)

select *
from stores

