DROP TABLE IF EXISTS feedbacks;

CREATE TABLE feedbacks (
  id SERIAL PRIMARY KEY, 
  email VARCHAR(280) not null, 
  title VARCHAR(80) not null, 
  service_preference VARCHAR(120), 
  area_interest VARCHAR(320) not null, 
  subject VARCHAR(200) not null, 
  message TEXT 
);

CREATE INDEX idx_feedbacks_email ON feedbacks (email);
