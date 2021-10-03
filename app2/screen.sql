create table actions (
ActionTitle text
, ActionStep integer
, ActionText text
, InsertTime datetime
, Note text
)

select distinct ActionTitle
from actions

select *
from actions
where ActionTitle = 'word2'

update actions
set ActionTitle = 'good'
where ActionTitle = 'word' and ActionStep = 2

update actions
set ActionTitle = 'word'
where ActionTitle = 'good'

select rowid, *
from actions

delete from actions where ActionTitle != 'word2'
delete from actions where rowid <= 25

update actions set ActionTitle = 'word' where ActionTitle = 'word2'
