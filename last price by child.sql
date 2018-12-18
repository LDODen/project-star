select chil.id, chil.name, chil.userid, pr1.groupid, pr1.price_date, pr1.price from children chil
left join (select pr.id, pr.groupid, pr.price_date, pr.price from (
select max(price_date) maxdate
from prices
where price_date<=date('2018-11-22')
group by groupid) maxdates
left join prices pr on maxdates.maxdate = pr.price_date
group by groupid) pr1 on chil.groupid = pr1.groupid
where chil.id = 3