-- Table: suggests

-- DROP TABLE suggests;

CREATE TABLE suggests
(
  user_id text,
  id text NOT NULL,
  title text NOT NULL,
  description text,
  dataset_name text,
  suggest_columns text,
  open_time timestamp without time zone,
  views integer,
  close_time timestamp without time zone,
  closed boolean,
  org_id text,
  send_mail integer DEFAULT 0,
  CONSTRAINT suggests_pkey PRIMARY KEY (id , title )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE suggests
  OWNER TO ckan_default;



  -- Table: suggests_comments

-- DROP TABLE suggests_comments;

CREATE TABLE suggests_comments
(
  id text NOT NULL,
  user_id text,
  suggest_id text NOT NULL,
  "time" timestamp without time zone NOT NULL,
  comment text,
  CONSTRAINT suggests_comments_pkey PRIMARY KEY (id , suggest_id , "time" )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE suggests_comments
  OWNER TO ckan_default;
