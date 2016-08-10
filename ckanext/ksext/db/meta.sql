#)table package add column meta_no
ALTER TABLE resource ADD COLUMN meta_no serial NOT NULL ;

#resource add column meta_no 
ALTER TABLE resource ADD COLUMN meta_no integer NOT NULL DEFAULT 0;

# resource update meta_no
CREATE TEMP TABLE temp1 AS
SELECT id AS rid, package_id, row_number() OVER (PARTITION BY package_id ORDER BY created) AS rnum
FROM resource
ORDER BY created;
UPDATE resource
SET meta_no = (SELECT rnum FROM temp1 WHERE temp1.rid=id);

DROP TABLE temp1;