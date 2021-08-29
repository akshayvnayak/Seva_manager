"""select s.*,m.start_yyyymm,IIF(f.sevadar_id=s.sevadar_id,TRUE,FALSE) as flexible,ga.group_id, a.*
from Sevadars s
left JOIN SevaStartMonths m ON s.sevadar_id = m.sevadar_id 
left join SevadarsFlexible f on s.sevadar_id = f.sevadar_id
left join SevadarAddress sa on s.sevadar_id = sa.sevadar_id
left join (Groups natural join GroupDetails) ga on ga.sevadar_id = s.sevadar_id
left join Addresses a on a.address_id = ga.address_id or a.address_id = sa.address_id
;
"""