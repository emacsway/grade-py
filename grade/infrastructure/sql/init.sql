
-- Domain Model


CREATE TABLE event_log (
    tenant_id varchar(128) NOT NULL,
    stream_type varchar(128) NOT NULL,
    stream_id varchar(255) NOT NULL,
    stream_position integer NOT NULL,
    event_type varchar(60) NOT NULL,
    event_version smallint NOT NULL,
    payload jsonb NOT NULL,
    metadata jsonb NULL,
    CONSTRAINT event_log_pk PRIMARY KEY (tenant_id, stream_type, stream_id, stream_position)
);
CREATE UNIQUE INDEX event_log__id_uniq ON event_log(stream_type, stream_id, stream_position);
CREATE UNIQUE INDEX event_log__event_id_uniq ON event_log( ((metadata->>'event_id')::uuid) );

