CREATE TABLE  "SYSLOG" 
   (	"ID" NUMBER, 
	"REMOTEIP" VARCHAR2(250), 
	"APPNAME" VARCHAR2(50), 
	"ZEIT" VARCHAR2(40), 
	"HOSTNAME" VARCHAR2(250), 
	"PID" NUMBER, 
	"PRIORITY" NUMBER, 
	"MESSAGE" VARCHAR2(2000), 
	"SYSDATUM" TIMESTAMP (6), 
	"GUID" VARCHAR2(40), 
	 CONSTRAINT "SYSLOG_PK" PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )   NO INMEMORY
/


CREATE OR REPLACE EDITIONABLE TRIGGER  "BI_SYSLOG" 
  before insert on "SYSLOG"               
  for each row  
begin 
  if :NEW."ID" is null then 
    select "SYSLOG_SEQ1".nextval into :NEW."ID" from sys.dual; 
    :NEW."SYSDATUM" := systimestamp;
  end if; 
end; 

/
ALTER TRIGGER  "BI_SYSLOG" ENABLE
/


