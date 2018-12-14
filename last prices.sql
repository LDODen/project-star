select pr.id, pr.groupid, pr.price_date, pr.price from (
select max(price_date) maxdate
from prices
where price_date<=date('2018-11-22')
group by groupid) maxdates
left join prices pr on maxdates.maxdate = pr.price_date
group by groupid
