-- Create a new database named 'creatathon'
CREATE DATABASE creatathon;

-- Switch to the newly created database
\c creatathon

-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;

CREATE TABLE IF NOT EXISTS public."User"
(
    user_id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    chart_id character varying(255) COLLATE pg_catalog."default",
    first_name character varying(255) COLLATE pg_catalog."default",
    email character varying(255) COLLATE pg_catalog."default",
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    telegram_id character varying(255) COLLATE pg_catalog."default",
    youtube_id integer,
    insta_id integer,
    CONSTRAINT "User_pkey" PRIMARY KEY (user_id),
    CONSTRAINT "User_email_key" UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.challengers
(
    id integer NOT NULL DEFAULT nextval('challenge_id_seq'::regclass),
    challenge_name character varying(255) COLLATE pg_catalog."default",
    task text COLLATE pg_catalog."default",
    links text COLLATE pg_catalog."default",
    taskon character varying(50) COLLATE pg_catalog."default",
    duration integer,
    prize text COLLATE pg_catalog."default",
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    challenge_task jsonb,
    CONSTRAINT challengers_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.fav_video
(
    insta_id character varying COLLATE pg_catalog."default" NOT NULL,
    tele_user character varying COLLATE pg_catalog."default",
    youtube_id character varying COLLATE pg_catalog."default",
    youtube_url character varying COLLATE pg_catalog."default",
    insta_url character varying COLLATE pg_catalog."default",
    CONSTRAINT fav_video_pkey PRIMARY KEY (insta_id)
);

CREATE TABLE IF NOT EXISTS public.guide
(
    id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    rules text COLLATE pg_catalog."default",
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT guide_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.instagram
(
    insta_id integer NOT NULL DEFAULT nextval('insta_id_seq'::regclass),
    username character varying(255) COLLATE pg_catalog."default",
    email character varying(255) COLLATE pg_catalog."default",
    name character varying(255) COLLATE pg_catalog."default",
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    followers integer,
    following integer,
    profile text COLLATE pg_catalog."default",
    CONSTRAINT instagram_pkey PRIMARY KEY (insta_id),
    CONSTRAINT instagram_email_key UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.progresstrack
(
    id integer NOT NULL DEFAULT nextval('progress_id_seq'::regclass),
    user_id integer,
    submit boolean DEFAULT false,
    link text COLLATE pg_catalog."default",
    challenge_day_id character varying COLLATE pg_catalog."default",
    submition_day timestamp with time zone,
    text character varying COLLATE pg_catalog."default",
    challenge_name character varying COLLATE pg_catalog."default",
    day character varying COLLATE pg_catalog."default",
    challenge_id integer,
    CONSTRAINT progresstrack_pkey PRIMARY KEY (id),
    CONSTRAINT unique_user_challenge_day UNIQUE (user_id, challenge_day_id)
);

CREATE TABLE IF NOT EXISTS public.winners
(
    id integer NOT NULL DEFAULT nextval('winner_id_seq'::regclass),
    challenge_id integer,
    user_id integer,
    status character varying(50) COLLATE pg_catalog."default",
    "timestamp" timestamp with time zone,
    CONSTRAINT winners_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.youtube
(
    youtube_id integer NOT NULL DEFAULT nextval('youtube_id_seq'::regclass),
    channel_name character varying(255) COLLATE pg_catalog."default",
    subscribers integer,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT youtube_pkey PRIMARY KEY (youtube_id)
);

ALTER TABLE IF EXISTS public."User"
    ADD CONSTRAINT "User_instragram_id_fkey" FOREIGN KEY (insta_id)
    REFERENCES public.instagram (insta_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public."User"
    ADD CONSTRAINT "User_youtube_id_fkey" FOREIGN KEY (youtube_id)
    REFERENCES public.youtube (youtube_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.winners
    ADD CONSTRAINT winners_challenge_id_fkey FOREIGN KEY (challenge_id)
    REFERENCES public.challengers (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;
