select a.anonid , o."name" as questionnaire , a.question, q.clone clonedFrom , l.description  as questionText, a.val from anonidanswers a 
join anonidfilled a2 on a.anonid = a2.anonid and a.obsscenario = a2.obsscenario
join anonid a3 on a.anonid = a3.id
join question q on q.id = a.question 
join language l on l.textid = q.textid
join obsscenario o on o.id = a.obsscenario 
where a.obsscenario = 183 and l.lang = 'ITA' and a.anonid in (SELECT a.anonid
FROM anonidanswers a
JOIN anonidfilled a2 
    ON a.anonid = a2.anonid 
   AND a.obsscenario = a2.obsscenario
WHERE a.obsscenario IN (43,111,183)
GROUP BY a.anonid
HAVING COUNT(DISTINCT a.obsscenario) = 3)
order by a.anonid , a.obsscenario