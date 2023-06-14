CREATE TABLESPACE telegram_bot
	OWNER postgres
	LOCATION '/var/lib/postgresql/data/telegram-bot';

CREATE DATABASE my_database;

CREATE SCHEMA your_fast_toto_bot;
ALTER SCHEMA your_fast_toto_bot OWNER TO postgres;

SET search_path TO pg_catalog,public,your_fast_toto_bot;

CREATE TABLE your_fast_toto_bot."user" (
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	current_language varchar(4) NOT NULL,
	username varchar(64),
	email varchar(64),
	phone varchar(20),
	reg_date date NOT NULL,
	reg_time timestamp NOT NULL,
	upd_date date NOT NULL,
	upd_time timestamp NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (id)
)
TABLESPACE telegram_bot;
ALTER TABLE your_fast_toto_bot."user" OWNER TO postgres;

CREATE TABLE your_fast_toto_bot.task (
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	title varchar(64) NOT NULL,
	description varchar(256),
	reg_telegram_user_id bigint NOT NULL,
	reg_date date NOT NULL,
	reg_time timestamp NOT NULL,
	is_done boolean NOT NULL,
	is_exist boolean NOT NULL,
	id_user uuid,
	CONSTRAINT task_pk PRIMARY KEY (id)
)
TABLESPACE telegram_bot;
ALTER TABLE your_fast_toto_bot.task OWNER TO postgres;

ALTER TABLE your_fast_toto_bot.task ADD CONSTRAINT user_fk FOREIGN KEY (id_user)
REFERENCES your_fast_toto_bot."user" (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

CREATE TABLE your_fast_toto_bot.telegram_user (
	telegram_user_id bigint NOT NULL,
	id_user uuid NOT NULL
);

ALTER TABLE your_fast_toto_bot.telegram_user OWNER TO postgres;
