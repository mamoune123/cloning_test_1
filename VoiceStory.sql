--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.2

-- Started on 2023-05-26 23:58:40 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 224 (class 1255 OID 16552)
-- Name: add_favorite_rows(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.add_favorite_rows() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  INSERT INTO favoris (id_utilisateur, id_histoire, is_favori)
  SELECT NEW.id_utilisateur, id_histoire, false
  FROM histoires;
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.add_favorite_rows() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 223 (class 1259 OID 16532)
-- Name: favoris; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favoris (
    id_favori integer NOT NULL,
    id_utilisateur integer,
    id_histoire integer,
    is_favori boolean
);


ALTER TABLE public.favoris OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16531)
-- Name: favoris_id_favori_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.favoris_id_favori_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.favoris_id_favori_seq OWNER TO postgres;

--
-- TOC entry 3661 (class 0 OID 0)
-- Dependencies: 222
-- Name: favoris_id_favori_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.favoris_id_favori_seq OWNED BY public.favoris.id_favori;


--
-- TOC entry 221 (class 1259 OID 16518)
-- Name: histoires; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.histoires (
    id_histoire integer NOT NULL,
    titre character varying(255),
    "id_thème" integer,
    img character varying(255),
    description character varying(255),
    texte text
);


ALTER TABLE public.histoires OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16517)
-- Name: histoires_id_histoire_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.histoires_id_histoire_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.histoires_id_histoire_seq OWNER TO postgres;

--
-- TOC entry 3662 (class 0 OID 0)
-- Dependencies: 220
-- Name: histoires_id_histoire_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.histoires_id_histoire_seq OWNED BY public.histoires.id_histoire;


--
-- TOC entry 219 (class 1259 OID 16511)
-- Name: thèmes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."thèmes" (
    "id_thème" integer NOT NULL,
    "nom_thème" character varying(255),
    img character varying(255)
);


ALTER TABLE public."thèmes" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16510)
-- Name: thèmes_id_thème_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."thèmes_id_thème_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."thèmes_id_thème_seq" OWNER TO postgres;

--
-- TOC entry 3663 (class 0 OID 0)
-- Dependencies: 218
-- Name: thèmes_id_thème_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."thèmes_id_thème_seq" OWNED BY public."thèmes"."id_thème";


--
-- TOC entry 215 (class 1259 OID 16490)
-- Name: utilisateurs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.utilisateurs (
    id_utilisateur integer NOT NULL,
    username character varying(255),
    password character varying(255)
);


ALTER TABLE public.utilisateurs OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16489)
-- Name: utilisateurs_id_utilisateur_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.utilisateurs_id_utilisateur_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.utilisateurs_id_utilisateur_seq OWNER TO postgres;

--
-- TOC entry 3664 (class 0 OID 0)
-- Dependencies: 214
-- Name: utilisateurs_id_utilisateur_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.utilisateurs_id_utilisateur_seq OWNED BY public.utilisateurs.id_utilisateur;


--
-- TOC entry 217 (class 1259 OID 16499)
-- Name: voix; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.voix (
    id_voix integer NOT NULL,
    id_utilisateur integer,
    chemin_fichier character varying(255),
    nom_file character varying(255)
);


ALTER TABLE public.voix OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16498)
-- Name: voix_id_voix_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.voix_id_voix_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.voix_id_voix_seq OWNER TO postgres;

--
-- TOC entry 3665 (class 0 OID 0)
-- Dependencies: 216
-- Name: voix_id_voix_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.voix_id_voix_seq OWNED BY public.voix.id_voix;


--
-- TOC entry 3488 (class 2604 OID 16535)
-- Name: favoris id_favori; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris ALTER COLUMN id_favori SET DEFAULT nextval('public.favoris_id_favori_seq'::regclass);


--
-- TOC entry 3487 (class 2604 OID 16521)
-- Name: histoires id_histoire; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.histoires ALTER COLUMN id_histoire SET DEFAULT nextval('public.histoires_id_histoire_seq'::regclass);


--
-- TOC entry 3486 (class 2604 OID 16514)
-- Name: thèmes id_thème; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."thèmes" ALTER COLUMN "id_thème" SET DEFAULT nextval('public."thèmes_id_thème_seq"'::regclass);


--
-- TOC entry 3484 (class 2604 OID 16493)
-- Name: utilisateurs id_utilisateur; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateurs ALTER COLUMN id_utilisateur SET DEFAULT nextval('public.utilisateurs_id_utilisateur_seq'::regclass);


--
-- TOC entry 3485 (class 2604 OID 16502)
-- Name: voix id_voix; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voix ALTER COLUMN id_voix SET DEFAULT nextval('public.voix_id_voix_seq'::regclass);


--
-- TOC entry 3655 (class 0 OID 16532)
-- Dependencies: 223
-- Data for Name: favoris; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (7, 2, 7, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (2, 2, 2, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (14, 3, 6, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (15, 3, 7, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (16, 3, 8, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (13, 3, 5, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (11, 3, 3, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (12, 3, 4, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (9, 3, 1, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (10, 3, 2, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (3, 2, 3, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (6, 2, 6, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (5, 2, 5, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (4, 2, 4, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (1, 2, 1, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (8, 2, 8, true);


--
-- TOC entry 3653 (class 0 OID 16518)
-- Dependencies: 221
-- Data for Name: histoires; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (1, 'The Lion and the Mouse', 2, 'https://picsum.photos/500/300/?image=10', 'A lion helps a mouse', 'Hoy en mi ventana brilla el sol. Y el corazón se pone triste contemplando la ciudad');
INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (2, 'The Tortoise and the Hare', 3, 'https://picsum.photos/500/300/?image=10', 'A slow tortoise wins a race against a fast hare', 'the tortoise is speedy');
INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (3, 'The Boy Who Cried Wolf', 4, 'https://picsum.photos/500/300/?image=10', 'A boy learns the consequences of lying', 'HELP ! HELP ! there is a wolf !');
INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (4, 'The Ant and the Grasshopper', 1, 'https://picsum.photos/500/300/?image=10', 'Creative genius', 'An ant prepares for winter while a grasshopper enjoys the summer');
INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (5, 'The Ugly Duckling', 1, 'https://picsum.photos/500/300/?image=10', 'A duckling discovers its true identity', 'A duckling discovers its true identity');
INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (6, 'The Little Mermaid', 4, 'https://picsum.photos/500/300/?image=10', 'A young mermaid''s sacrifice for love', 'Under the sea, a magical tale unfolds');
INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (7, 'Cinderella', 3, 'https://picsum.photos/500/300/?image=10', 'A girl''s journey from rags to riches', 'With glass slippers, dreams come true');
INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (8, 'Rapunzel', 2, 'https://picsum.photos/500/300/?image=10', 'A girl with long, golden hair locked in a tower', 'Let down your hair, let''s embark on an adventure');


--
-- TOC entry 3651 (class 0 OID 16511)
-- Dependencies: 219
-- Data for Name: thèmes; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."thèmes" ("id_thème", "nom_thème", img) VALUES (1, 'comptes et autres', '/img/duck.png');
INSERT INTO public."thèmes" ("id_thème", "nom_thème", img) VALUES (2, 'fable mythe et literature', '/img/duck.png');
INSERT INTO public."thèmes" ("id_thème", "nom_thème", img) VALUES (3, 'heroine et heros', '/img/duck.png');
INSERT INTO public."thèmes" ("id_thème", "nom_thème", img) VALUES (4, 'les animaux', '/img/duck.png');


--
-- TOC entry 3647 (class 0 OID 16490)
-- Dependencies: 215
-- Data for Name: utilisateurs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.utilisateurs (id_utilisateur, username, password) VALUES (1, 'Mamoune2', 'HAWHAW');
INSERT INTO public.utilisateurs (id_utilisateur, username, password) VALUES (2, 'Mamoune', 'Password');
INSERT INTO public.utilisateurs (id_utilisateur, username, password) VALUES (3, 'Nizar', 'SAMSAM');


--
-- TOC entry 3649 (class 0 OID 16499)
-- Dependencies: 217
-- Data for Name: voix; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3666 (class 0 OID 0)
-- Dependencies: 222
-- Name: favoris_id_favori_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.favoris_id_favori_seq', 16, true);


--
-- TOC entry 3667 (class 0 OID 0)
-- Dependencies: 220
-- Name: histoires_id_histoire_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.histoires_id_histoire_seq', 9, true);


--
-- TOC entry 3668 (class 0 OID 0)
-- Dependencies: 218
-- Name: thèmes_id_thème_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."thèmes_id_thème_seq"', 4, true);


--
-- TOC entry 3669 (class 0 OID 0)
-- Dependencies: 214
-- Name: utilisateurs_id_utilisateur_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.utilisateurs_id_utilisateur_seq', 3, true);


--
-- TOC entry 3670 (class 0 OID 0)
-- Dependencies: 216
-- Name: voix_id_voix_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.voix_id_voix_seq', 1, false);


--
-- TOC entry 3498 (class 2606 OID 16537)
-- Name: favoris favoris_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris
    ADD CONSTRAINT favoris_pkey PRIMARY KEY (id_favori);


--
-- TOC entry 3496 (class 2606 OID 16525)
-- Name: histoires histoires_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.histoires
    ADD CONSTRAINT histoires_pkey PRIMARY KEY (id_histoire);


--
-- TOC entry 3494 (class 2606 OID 16516)
-- Name: thèmes thèmes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."thèmes"
    ADD CONSTRAINT "thèmes_pkey" PRIMARY KEY ("id_thème");


--
-- TOC entry 3490 (class 2606 OID 16497)
-- Name: utilisateurs utilisateurs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateurs
    ADD CONSTRAINT utilisateurs_pkey PRIMARY KEY (id_utilisateur);


--
-- TOC entry 3492 (class 2606 OID 16504)
-- Name: voix voix_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voix
    ADD CONSTRAINT voix_pkey PRIMARY KEY (id_voix);


--
-- TOC entry 3503 (class 2620 OID 16553)
-- Name: utilisateurs add_favorite_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER add_favorite_trigger AFTER INSERT ON public.utilisateurs FOR EACH ROW EXECUTE FUNCTION public.add_favorite_rows();


--
-- TOC entry 3501 (class 2606 OID 16543)
-- Name: favoris favoris_id_histoire_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris
    ADD CONSTRAINT favoris_id_histoire_fkey FOREIGN KEY (id_histoire) REFERENCES public.histoires(id_histoire);


--
-- TOC entry 3502 (class 2606 OID 16538)
-- Name: favoris favoris_id_utilisateur_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris
    ADD CONSTRAINT favoris_id_utilisateur_fkey FOREIGN KEY (id_utilisateur) REFERENCES public.utilisateurs(id_utilisateur);


--
-- TOC entry 3500 (class 2606 OID 16526)
-- Name: histoires histoires_id_thème_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.histoires
    ADD CONSTRAINT "histoires_id_thème_fkey" FOREIGN KEY ("id_thème") REFERENCES public."thèmes"("id_thème");


--
-- TOC entry 3499 (class 2606 OID 16505)
-- Name: voix voix_id_utilisateur_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voix
    ADD CONSTRAINT voix_id_utilisateur_fkey FOREIGN KEY (id_utilisateur) REFERENCES public.utilisateurs(id_utilisateur);


-- Completed on 2023-05-26 23:58:41 CEST

--
-- PostgreSQL database dump complete
--

