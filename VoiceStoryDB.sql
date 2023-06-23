--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.2

-- Started on 2023-06-23 11:43:04 CEST

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

DROP DATABASE "VoiceStory";
--
-- TOC entry 3683 (class 1262 OID 16389)
-- Name: VoiceStory; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "VoiceStory" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = icu LOCALE = 'en_US.UTF-8' ICU_LOCALE = 'en-US';


ALTER DATABASE "VoiceStory" OWNER TO postgres;

\connect "VoiceStory"

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
-- TOC entry 226 (class 1255 OID 16552)
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

--
-- TOC entry 228 (class 1255 OID 16562)
-- Name: set_selected_to_false(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.set_selected_to_false() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE voix
    SET selected = FALSE
    WHERE id_utilisateur = NEW.id_utilisateur AND id_voix <> NEW.id_voix;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.set_selected_to_false() OWNER TO postgres;

--
-- TOC entry 227 (class 1255 OID 16559)
-- Name: update_selected(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_selected() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Set selected=True for the newly inserted row
    NEW.selected = TRUE;

    -- Set selected=False for all other rows
    UPDATE voix SET selected = FALSE WHERE id_utilisateur = NEW.id_utilisateur AND id_voix != NEW.id_voix;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_selected() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 225 (class 1259 OID 24753)
-- Name: clone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clone (
    id_clone integer NOT NULL,
    chemin_fichier character varying(255),
    nom_file character varying(255),
    date_ajout timestamp without time zone DEFAULT CURRENT_TIMESTAMP(0),
    id_utilisateur integer,
    id_histoire integer
);


ALTER TABLE public.clone OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 24752)
-- Name: clone_id_clone_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clone_id_clone_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clone_id_clone_seq OWNER TO postgres;

--
-- TOC entry 3684 (class 0 OID 0)
-- Dependencies: 224
-- Name: clone_id_clone_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clone_id_clone_seq OWNED BY public.clone.id_clone;


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
-- TOC entry 3685 (class 0 OID 0)
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
-- TOC entry 3686 (class 0 OID 0)
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
-- TOC entry 3687 (class 0 OID 0)
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
    password character varying(255),
    email character varying(255)
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
-- TOC entry 3688 (class 0 OID 0)
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
    nom_file character varying(255),
    date_ajout timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP,
    selected boolean DEFAULT true
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
-- TOC entry 3689 (class 0 OID 0)
-- Dependencies: 216
-- Name: voix_id_voix_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.voix_id_voix_seq OWNED BY public.voix.id_voix;


--
-- TOC entry 3498 (class 2604 OID 24756)
-- Name: clone id_clone; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clone ALTER COLUMN id_clone SET DEFAULT nextval('public.clone_id_clone_seq'::regclass);


--
-- TOC entry 3497 (class 2604 OID 16535)
-- Name: favoris id_favori; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris ALTER COLUMN id_favori SET DEFAULT nextval('public.favoris_id_favori_seq'::regclass);


--
-- TOC entry 3496 (class 2604 OID 16521)
-- Name: histoires id_histoire; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.histoires ALTER COLUMN id_histoire SET DEFAULT nextval('public.histoires_id_histoire_seq'::regclass);


--
-- TOC entry 3495 (class 2604 OID 16514)
-- Name: thèmes id_thème; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."thèmes" ALTER COLUMN "id_thème" SET DEFAULT nextval('public."thèmes_id_thème_seq"'::regclass);


--
-- TOC entry 3491 (class 2604 OID 16493)
-- Name: utilisateurs id_utilisateur; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateurs ALTER COLUMN id_utilisateur SET DEFAULT nextval('public.utilisateurs_id_utilisateur_seq'::regclass);


--
-- TOC entry 3492 (class 2604 OID 16502)
-- Name: voix id_voix; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voix ALTER COLUMN id_voix SET DEFAULT nextval('public.voix_id_voix_seq'::regclass);


--
-- TOC entry 3677 (class 0 OID 24753)
-- Dependencies: 225
-- Data for Name: clone; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (1, '/Users/mac/Desktop/Cloning_test/fa44469b-b35b-4ec9-a84b-5936a9490c48.wav', 'Mamounel016.wav', '2023-06-08 22:39:06', 48, NULL);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (2, '/Users/mac/Desktop/Cloning_test/templates/dist/output/c1116ce9-ed3a-479d-819f-91e32d681ef9.wav', 'Mamouneez5l.wav', '2023-06-08 22:40:48', 48, NULL);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (3, '/Users/mac/Desktop/Cloning_test/templates/dist/output/15d71ad1-7e06-4b10-bb55-0fa300fb4dc2.wav', 'Mamoune1m8n.wav', '2023-06-08 23:01:59', 48, NULL);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (4, '/Users/mac/Desktop/Cloning_test/templates/dist/output/ff97aa62-074d-4319-8de8-3892aacf791d.wav', 'Mamounezw98.wav', '2023-06-08 23:05:31', 48, NULL);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (5, '/Users/mac/Desktop/Cloning_test/templates/dist/output/7172029a-edb1-401a-8d93-e284bd1c50e7.wav', 'Mamoune3tsu.wav', '2023-06-09 14:43:54', 48, NULL);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (6, '/Users/mac/Desktop/Cloning_test/templates/dist/output/2cbb7634-0c5f-4144-8b06-aa70b443cf59.wav', 'Mamounei6bn.wav', '2023-06-11 17:53:17', 48, NULL);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (7, '/Users/mac/Desktop/Cloning_test/templates/dist/output/30cd1a16-7fe7-4ebf-880b-de89cb0a1828.wav', 'Mamounew48i.wav', '2023-06-11 17:53:47', 48, NULL);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (8, '/Users/mac/Desktop/Cloning_test/templates/dist/output/c840ac93-1824-4381-91b8-70c6773a59db.wav', 'Mehdipdal.wav', '2023-06-11 23:27:55', 49, NULL);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (9, '/Users/mac/Desktop/Cloning_test/templates/dist/output/d4cc8fcb-8d37-48fa-ba9b-06d370c55e17.wav', 'Mamouneyy7z.wav', '2023-06-12 15:37:47', 48, 1);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (10, '/Users/mac/Desktop/Cloning_test/templates/dist/output/08e3c5d6-0549-45de-a98a-21ae0ea17cf6.wav', 'Mamounemltu.wav', '2023-06-12 15:38:48', 48, 8);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (11, '/Users/mac/Desktop/Cloning_test/templates/dist/output/458363e8-6b3b-4b54-8e03-c2d002ab2e1b.wav', 'Mamoune682d.wav', '2023-06-12 17:35:47', 48, 5);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (12, '/Users/mac/Desktop/Cloning_test/templates/dist/output/6538c929-6b9a-4036-a657-fccac54f0d5c.wav', 'Mamounesjgt.wav', '2023-06-12 17:38:40', 48, 9);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (13, '/Users/mac/Desktop/Cloning_test/templates/dist/output/7ad54406-31a9-4765-9d26-0ffd4a2aa2d0.wav', 'ashraf11i2.wav', '2023-06-13 18:09:41', 50, 3);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (14, '/Users/mac/Desktop/Cloning_test/templates/dist/output/5e1e363d-4183-48ba-92cb-ae88adea8cd3.wav', 'Mamouneg6qe.wav', '2023-06-20 16:05:34', 48, 9);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (15, '/Users/mac/Desktop/Cloning_test/templates/dist/output/5813b061-059f-4607-81a4-49b36dcce47b.wav', 'Mamounewg4i.wav', '2023-06-20 16:06:57', 48, 9);
INSERT INTO public.clone (id_clone, chemin_fichier, nom_file, date_ajout, id_utilisateur, id_histoire) VALUES (16, '/Users/mac/Desktop/Cloning_test/templates/dist/output/eefb35c7-54fc-4eb0-b5ca-83672ca02b6c.wav', 'Mamounebzcj.wav', '2023-06-20 16:11:55', 48, 9);


--
-- TOC entry 3675 (class 0 OID 16532)
-- Dependencies: 223
-- Data for Name: favoris; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (316, 48, 2, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (317, 48, 3, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (320, 48, 6, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (321, 48, 7, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (318, 48, 4, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (324, 49, 1, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (325, 49, 2, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (326, 49, 3, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (329, 49, 6, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (330, 49, 7, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (331, 49, 8, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (332, 49, 9, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (327, 49, 4, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (328, 49, 5, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (315, 48, 1, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (333, 50, 1, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (334, 50, 2, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (336, 50, 4, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (337, 50, 5, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (339, 50, 7, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (340, 50, 8, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (341, 50, 9, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (338, 50, 6, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (335, 50, 3, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (342, 52, 1, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (343, 52, 2, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (344, 52, 3, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (345, 52, 4, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (346, 52, 5, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (347, 52, 6, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (348, 52, 7, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (349, 52, 8, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (350, 52, 9, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (351, 54, 1, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (352, 54, 2, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (353, 54, 3, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (354, 54, 4, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (355, 54, 5, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (356, 54, 6, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (357, 54, 7, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (358, 54, 8, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (359, 54, 9, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (319, 48, 5, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (322, 48, 8, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (323, 48, 9, true);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (360, 55, 1, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (361, 55, 2, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (362, 55, 3, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (363, 55, 4, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (364, 55, 5, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (365, 55, 6, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (366, 55, 7, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (367, 55, 8, false);
INSERT INTO public.favoris (id_favori, id_utilisateur, id_histoire, is_favori) VALUES (368, 55, 9, false);


--
-- TOC entry 3673 (class 0 OID 16518)
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
INSERT INTO public.histoires (id_histoire, titre, "id_thème", img, description, texte) VALUES (9, 'Once Upon a time', 1, 'https://picsum.photos/500/300/?image=10', 'Example', 'Once upon a time in a peaceful village nestled amidst lush green fields, there lived a young boy named Ethan. He was known for his adventurous spirit and curious nature. One sunny day, while exploring the outskirts of the village, Ethan stumbled upon a hidden pathway leading deep into an enchanted forest. Intrigued by the unknown, he decided to venture into the mysterious woods, unaware of the magical journey that awaited him. As he delved deeper into the forest, strange creatures and enchanting sights surrounded him, unraveling a world beyond his wildest dreams.');


--
-- TOC entry 3671 (class 0 OID 16511)
-- Dependencies: 219
-- Data for Name: thèmes; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."thèmes" ("id_thème", "nom_thème", img) VALUES (1, 'comptes et autres', '/img/duck.png');
INSERT INTO public."thèmes" ("id_thème", "nom_thème", img) VALUES (2, 'fable mythe et literature', '/img/duck.png');
INSERT INTO public."thèmes" ("id_thème", "nom_thème", img) VALUES (3, 'heroine et heros', '/img/duck.png');
INSERT INTO public."thèmes" ("id_thème", "nom_thème", img) VALUES (4, 'les animaux', '/img/duck.png');


--
-- TOC entry 3667 (class 0 OID 16490)
-- Dependencies: 215
-- Data for Name: utilisateurs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.utilisateurs (id_utilisateur, username, password, email) VALUES (48, 'Mamoune', 'Hello2', 'mandalouss@hotmail.fr');
INSERT INTO public.utilisateurs (id_utilisateur, username, password, email) VALUES (49, 'Mehdi', 'Hello2', 'Thaili.mehdi1@gmail.com');
INSERT INTO public.utilisateurs (id_utilisateur, username, password, email) VALUES (50, 'ashraf', 'Hello2', 'chkon552@gmail.com');
INSERT INTO public.utilisateurs (id_utilisateur, username, password, email) VALUES (52, 'Mamoune234', 'Hello2', 'azejkazbjazr@hotmail.fr');
INSERT INTO public.utilisateurs (id_utilisateur, username, password, email) VALUES (54, 'Mamoune2994', 'Hello2', 'ERTYUAIKE@hotmail.fr');
INSERT INTO public.utilisateurs (id_utilisateur, username, password, email) VALUES (55, 'azrlkahzr', 'Hello2', 'azlkrhazo@hotmail.fr');


--
-- TOC entry 3669 (class 0 OID 16499)
-- Dependencies: 217
-- Data for Name: voix; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.voix (id_voix, id_utilisateur, chemin_fichier, nom_file, date_ajout, selected) VALUES (90, 48, '/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix/5bdb8e86-8e66-4480-9442-5b48dd642284.wav', '.mp3', '2023-06-20 16:06:30', false);
INSERT INTO public.voix (id_voix, id_utilisateur, chemin_fichier, nom_file, date_ajout, selected) VALUES (89, 48, '/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix/0c755bf5-1a5c-44b5-8996-4ba2153e9833.wav', 'No.mp3', '2023-06-20 16:05:12', false);
INSERT INTO public.voix (id_voix, id_utilisateur, chemin_fichier, nom_file, date_ajout, selected) VALUES (87, 48, '/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix/6e943ef3-b80b-47a3-95de-1d78c7f15641.wav', 'Hatim.mp3', '2023-06-12 17:38:19', false);
INSERT INTO public.voix (id_voix, id_utilisateur, chemin_fichier, nom_file, date_ajout, selected) VALUES (85, 48, '/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix/07727985-d51a-4009-8944-87dd172139cd.wav', 'Mams.mp3', '2023-06-09 14:43:42', false);
INSERT INTO public.voix (id_voix, id_utilisateur, chemin_fichier, nom_file, date_ajout, selected) VALUES (84, 48, '/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix/1c85b9ec-6c76-4c4f-a444-d211e0c7eff3.wav', 'hey234.mp3', '2023-06-08 22:20:51', false);
INSERT INTO public.voix (id_voix, id_utilisateur, chemin_fichier, nom_file, date_ajout, selected) VALUES (91, 48, '/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix/c69cc9e7-0fed-4e1e-af1d-9b265238ce5e.wav', 'Basha.mp3', '2023-06-20 16:11:35', true);
INSERT INTO public.voix (id_voix, id_utilisateur, chemin_fichier, nom_file, date_ajout, selected) VALUES (83, 48, '/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix/c10d605b-7c9e-4f0b-b6fb-a4defffca515.wav', 'Hey2.mp3', '2023-06-08 22:20:17', false);
INSERT INTO public.voix (id_voix, id_utilisateur, chemin_fichier, nom_file, date_ajout, selected) VALUES (82, 48, '/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix/545b495a-2294-4391-b190-10cc69259128.wav', 'hey.mp3', '2023-06-08 22:17:04', false);


--
-- TOC entry 3690 (class 0 OID 0)
-- Dependencies: 224
-- Name: clone_id_clone_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clone_id_clone_seq', 16, true);


--
-- TOC entry 3691 (class 0 OID 0)
-- Dependencies: 222
-- Name: favoris_id_favori_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.favoris_id_favori_seq', 368, true);


--
-- TOC entry 3692 (class 0 OID 0)
-- Dependencies: 220
-- Name: histoires_id_histoire_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.histoires_id_histoire_seq', 9, true);


--
-- TOC entry 3693 (class 0 OID 0)
-- Dependencies: 218
-- Name: thèmes_id_thème_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."thèmes_id_thème_seq"', 4, true);


--
-- TOC entry 3694 (class 0 OID 0)
-- Dependencies: 214
-- Name: utilisateurs_id_utilisateur_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.utilisateurs_id_utilisateur_seq', 55, true);


--
-- TOC entry 3695 (class 0 OID 0)
-- Dependencies: 216
-- Name: voix_id_voix_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.voix_id_voix_seq', 91, true);


-- Completed on 2023-06-23 11:43:04 CEST

--
-- PostgreSQL database dump complete
--

