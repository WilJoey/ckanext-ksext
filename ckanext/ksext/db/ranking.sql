-- Table: ranking

-- DROP TABLE ranking;

CREATE TABLE ranking
(
  user_id text NOT NULL,
  package_id text NOT NULL,
  stars integer NOT NULL DEFAULT 0,
  CONSTRAINT pk_ranking PRIMARY KEY (user_id , package_id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ranking
  OWNER TO ckan_default;
