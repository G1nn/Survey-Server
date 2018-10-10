drop table survey_data;

create table survey_data(
  survey_id SERIAL PRIMARY KEY,
  q1 varchar(20),
  q2 char(50),
  q3 char(20),
  q4 char(10),
  q5 varchar(50),
  ts text not null default NOW()
);
