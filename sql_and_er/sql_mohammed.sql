/*drop trigger not_belong_company on company;
drop function not_belong_company();

drop trigger not_belong_client on client;
drop function not_belong_client();


drop table offer;
drop table job_unique_view;
drop table application;
drop table job;
drop table practical_experiences;
drop table client;
drop table company;*/

drop table allusers;

create table allusers (
account varchar(100)not null ,
name varchar(100),
email varchar(100)not null,
logo varchar default '/media/default_logos/default_logo.jpg',
user_type varchar(10)check( user_type in ('client','company')),
password varchar(200)not null,
primary key(account)
);


insert into allusers values ('user','mohamed','email@gmail.com','/media/default_logos/default_logo.jpg','client');
insert into client values ('user','student',cast(now( as date)),'gaza','master','java python','Engineering iug','Computer eng','/media/defaut_cv.pdf');
create table client(
account varchar(100)not null,
client_type  varchar(10) check(client_type in ('student','graduate')) default 'student',--student or graduate
birthday date,
address varchar(300),
qualifications varchar(200),
skills varchar,
education varchar,
specialist varchar(500),
cv varchar default '/media/defaut_cv.pdf',
primary key(account),
foreign key(account)references allusers(account)
);




create table practical_experiences(
account varchar(100)not null,
title varchar(50),
about varchar, 
image varchar,
primary key (account,title),
foreign key(account)references client(account)
);

create table company(
account varchar(100)not null,
campany_name varchar(300),
address varchar(300),
salary_range_from numeric(8,3),
salary_range_to numeric(8,3),
num_of_employees int,
about_campany varchar,
about_campany_video varchar,
primary key(account),
foreign key(account)references allusers(account)
);



create table Job(
job_id varchar(200)not null check(job_id like concat(account,'_%')),
account varchar(300)not null,-- company account
job_title varchar(200),
job_description varchar,
post_time timestamp, 
num_of_views int,
status varchar(10) check( status in ('available','verified'))not null default'available' ,
job_type varchar(10) check( job_type in ('general','special')),
price_from numeric,
price_to numeric,
req_skill  varchar,
primary key(job_id),
foreign key(account)references company(account)
);




create table job_unique_view(
std_account varchar(100)not null,
job_id varchar(200)not null,
primary key (std_account,job_id),
foreign key (std_account)references client(account),
foreign key (job_id)references job(job_id)
);



create table Offer(
job_id varchar(200)not null,
std_account varchar(100)not null,
std_reply varchar(10) check( std_reply in ('accept','refuse','no_reply')) default 'no_reply',
primary key (job_id,std_account),
foreign key (std_account)references client(account),
foreign key (job_id)references job(job_id)
);


create table Application(
std_account varchar(100)not null,
job_id varchar(200)not null,
company_reply varchar(10) check( company_reply in ('accept','refuse','no_reply')) default 'no_reply',
company_massage varchar,
primary key (std_account,job_id),
foreign key (std_account)references client(account),
foreign key (job_id)references job(job_id)
);

create function not_belong_company()
returns trigger as
$m$
begin
	if not exists(
        select * from 
		allusers 
		where allusers.account = new.account
		)
		then raise exception
	'the user dose not exist in table allusers';
    elseif not exists(
        select * from 
		allusers  
		where allusers.account = new.account
		and allusers.user_type='company'
		)
		then raise exception
	'the user not a company type ';
end if;
	return new;
end;
$m$
language 'plpgsql';

create trigger not_belong_company
before insert or update 
on company 
for each row
execute procedure not_belong_company();


create function not_belong_client()
returns trigger as
$m$
begin
	if not exists(
        select * from 
		allusers 
		where allusers.account = new.account
		)
		then raise exception
	'the user dose not exist in table allusers';
    elseif not exists(
        select * from 
		allusers  
		where allusers.account = new.account
		and allusers.user_type='client'
		)
		then raise exception
	'the user not a client type ';
end if;
	return new;
end;
$m$
language 'plpgsql';

create trigger not_belong_client
before insert or update 
on client 
for each row
execute procedure not_belong_client();
