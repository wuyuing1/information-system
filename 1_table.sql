SET client_encoding TO 'GBK';

DROP TABLE IF EXISTS sys_user;
CREATE TABLE IF NOT EXISTS sys_user (
    sn          INTEGER,
    user_sn     VARCHAR(10),
    user_name   TEXT,
    PRIMARY KEY(sn)
);

CREATE SEQUENCE seq_sys_user_sn
    START 10000 INCREMENT 1 OWNED BY sys_user.sn;
ALTER TABLE sys_user ALTER sn
    SET DEFAULT nextval('seq_sys_user_sn');

CREATE UNIQUE INDEX idx_sys_user_user_name ON sys_user(user_sn);

DROP TABLE IF EXISTS passwords;
CREATE TABLE IF NOT EXISTS passwords (
    user_sn     VARCHAR(10),
    password    TEXT,
    PRIMARY KEY(user_sn)
);

ALTER TABLE passwords
    ADD CONSTRAINT user_sn_fk FOREIGN KEY (user_sn) REFERENCES sys_user(user_sn);