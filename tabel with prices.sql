select tabel.date, tabel.childid, tabel.value, max(pric.price_date), pric.price, chil.name, chil.userid, chil.groupid from tabel
left join children chil on childid = chil.id, 
(Select price_date, price, groupid from prices) pric on date >= pric.price_date and chil.groupid = pric.groupid
where tabel.value = 1 and tabel.childid = 3 and tabel.date between date('2018-11-01') and date('2018-11-30')
group by tabel.date, tabel.childid, chil.userid, chil.groupid 