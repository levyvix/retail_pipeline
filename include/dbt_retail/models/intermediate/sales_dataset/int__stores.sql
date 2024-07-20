with store as (
	select *
	from {{ ref("stg__stores")}}

)

select
	*
from store