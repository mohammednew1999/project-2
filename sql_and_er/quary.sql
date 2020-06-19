select * from job join application using (job_id);
select * from allusers join company using (account);
select * from allusers join client using (account);
select * from client join practical_experiences using(account);
select count(*) as uniqe_view from job_unique_view where job_id='';
select count(*) from application where job_id='';
select * from offer join job using(job_id);
