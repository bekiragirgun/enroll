--
-- PostgreSQL database dump
--

\restrict yqCWc2ZmUZPSyUb6pd2H2mQ2gdySlBVVDujICwFFBJOOaRkF06pfQMo0sDwyFdU

-- Dumped from database version 15.15 (Debian 15.15-1.pgdg13+1)
-- Dumped by pg_dump version 15.15 (Debian 15.15-1.pgdg13+1)

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

ALTER TABLE IF EXISTS ONLY public.yoklama DROP CONSTRAINT IF EXISTS yoklama_pkey;
ALTER TABLE IF EXISTS ONLY public.yoklama_override DROP CONSTRAINT IF EXISTS yoklama_override_pkey;
ALTER TABLE IF EXISTS ONLY public.yoklama_override DROP CONSTRAINT IF EXISTS yoklama_override_numara_hafta_key;
ALTER TABLE IF EXISTS ONLY public.yardim_talepleri DROP CONSTRAINT IF EXISTS yardim_talepleri_pkey;
ALTER TABLE IF EXISTS ONLY public.terminal_guvenlik_log DROP CONSTRAINT IF EXISTS terminal_guvenlik_log_pkey;
ALTER TABLE IF EXISTS ONLY public.sorular DROP CONSTRAINT IF EXISTS sorular_pkey;
ALTER TABLE IF EXISTS ONLY public.soru_cikti_iliskisi DROP CONSTRAINT IF EXISTS soru_cikti_iliskisi_pkey;
ALTER TABLE IF EXISTS ONLY public.siniflar DROP CONSTRAINT IF EXISTS siniflar_pkey;
ALTER TABLE IF EXISTS ONLY public.siniflar DROP CONSTRAINT IF EXISTS siniflar_ad_key;
ALTER TABLE IF EXISTS ONLY public.sinavlar DROP CONSTRAINT IF EXISTS sinavlar_pkey;
ALTER TABLE IF EXISTS ONLY public.sinav_ihlaller DROP CONSTRAINT IF EXISTS sinav_ihlaller_pkey;
ALTER TABLE IF EXISTS ONLY public.secenekler DROP CONSTRAINT IF EXISTS secenekler_pkey;
ALTER TABLE IF EXISTS ONLY public.seb_cikis_talepleri DROP CONSTRAINT IF EXISTS seb_cikis_talepleri_pkey;
ALTER TABLE IF EXISTS ONLY public.seb_cikis_log DROP CONSTRAINT IF EXISTS seb_cikis_log_pkey;
ALTER TABLE IF EXISTS ONLY public.sahte_giris_log DROP CONSTRAINT IF EXISTS sahte_giris_log_pkey;
ALTER TABLE IF EXISTS ONLY public.ogrenme_ciktilari DROP CONSTRAINT IF EXISTS ogrenme_ciktilari_pkey;
ALTER TABLE IF EXISTS ONLY public.ogrenciler DROP CONSTRAINT IF EXISTS ogrenciler_pkey;
ALTER TABLE IF EXISTS ONLY public.ogrenciler DROP CONSTRAINT IF EXISTS ogrenciler_numara_key;
ALTER TABLE IF EXISTS ONLY public.ogrenci_cikis_log DROP CONSTRAINT IF EXISTS ogrenci_cikis_log_pkey;
ALTER TABLE IF EXISTS ONLY public.ogrenci_cevaplari DROP CONSTRAINT IF EXISTS ogrenci_cevaplari_pkey;
ALTER TABLE IF EXISTS ONLY public.ogrenci_aktivite_log DROP CONSTRAINT IF EXISTS ogrenci_aktivite_log_pkey;
ALTER TABLE IF EXISTS ONLY public.ayarlar DROP CONSTRAINT IF EXISTS ayarlar_pkey;
ALTER TABLE IF EXISTS public.yoklama_override ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.yoklama ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.yardim_talepleri ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.terminal_guvenlik_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.sorular ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.soru_cikti_iliskisi ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.siniflar ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.sinavlar ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.sinav_ihlaller ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.secenekler ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.seb_cikis_talepleri ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.seb_cikis_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.sahte_giris_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.ogrenme_ciktilari ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.ogrenciler ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.ogrenci_cikis_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.ogrenci_cevaplari ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.ogrenci_aktivite_log ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.yoklama_override_id_seq;
DROP TABLE IF EXISTS public.yoklama_override;
DROP SEQUENCE IF EXISTS public.yoklama_id_seq;
DROP TABLE IF EXISTS public.yoklama;
DROP SEQUENCE IF EXISTS public.yardim_talepleri_id_seq;
DROP TABLE IF EXISTS public.yardim_talepleri;
DROP SEQUENCE IF EXISTS public.terminal_guvenlik_log_id_seq;
DROP TABLE IF EXISTS public.terminal_guvenlik_log;
DROP SEQUENCE IF EXISTS public.sorular_id_seq;
DROP TABLE IF EXISTS public.sorular;
DROP SEQUENCE IF EXISTS public.soru_cikti_iliskisi_id_seq;
DROP TABLE IF EXISTS public.soru_cikti_iliskisi;
DROP SEQUENCE IF EXISTS public.siniflar_id_seq;
DROP TABLE IF EXISTS public.siniflar;
DROP SEQUENCE IF EXISTS public.sinavlar_id_seq;
DROP TABLE IF EXISTS public.sinavlar;
DROP SEQUENCE IF EXISTS public.sinav_ihlaller_id_seq;
DROP TABLE IF EXISTS public.sinav_ihlaller;
DROP SEQUENCE IF EXISTS public.secenekler_id_seq;
DROP TABLE IF EXISTS public.secenekler;
DROP SEQUENCE IF EXISTS public.seb_cikis_talepleri_id_seq;
DROP TABLE IF EXISTS public.seb_cikis_talepleri;
DROP SEQUENCE IF EXISTS public.seb_cikis_log_id_seq;
DROP TABLE IF EXISTS public.seb_cikis_log;
DROP SEQUENCE IF EXISTS public.sahte_giris_log_id_seq;
DROP TABLE IF EXISTS public.sahte_giris_log;
DROP SEQUENCE IF EXISTS public.ogrenme_ciktilari_id_seq;
DROP TABLE IF EXISTS public.ogrenme_ciktilari;
DROP SEQUENCE IF EXISTS public.ogrenciler_id_seq;
DROP TABLE IF EXISTS public.ogrenciler;
DROP SEQUENCE IF EXISTS public.ogrenci_cikis_log_id_seq;
DROP TABLE IF EXISTS public.ogrenci_cikis_log;
DROP SEQUENCE IF EXISTS public.ogrenci_cevaplari_id_seq;
DROP TABLE IF EXISTS public.ogrenci_cevaplari;
DROP SEQUENCE IF EXISTS public.ogrenci_aktivite_log_id_seq;
DROP TABLE IF EXISTS public.ogrenci_aktivite_log;
DROP TABLE IF EXISTS public.ayarlar;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ayarlar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ayarlar (
    anahtar text NOT NULL,
    deger text NOT NULL
);


ALTER TABLE public.ayarlar OWNER TO postgres;

--
-- Name: ogrenci_aktivite_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ogrenci_aktivite_log (
    id integer NOT NULL,
    numara text NOT NULL,
    ip text NOT NULL,
    aktivite_tipi text NOT NULL,
    detay text,
    tarih text NOT NULL,
    saat text NOT NULL
);


ALTER TABLE public.ogrenci_aktivite_log OWNER TO postgres;

--
-- Name: ogrenci_aktivite_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ogrenci_aktivite_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ogrenci_aktivite_log_id_seq OWNER TO postgres;

--
-- Name: ogrenci_aktivite_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ogrenci_aktivite_log_id_seq OWNED BY public.ogrenci_aktivite_log.id;


--
-- Name: ogrenci_cevaplari; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ogrenci_cevaplari (
    id integer NOT NULL,
    sinav_id integer NOT NULL,
    ogrenci_numara text NOT NULL,
    soru_id integer NOT NULL,
    verilen_cevap text NOT NULL,
    puan integer DEFAULT 0,
    cevap_zamani timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    taslak integer DEFAULT 0
);


ALTER TABLE public.ogrenci_cevaplari OWNER TO postgres;

--
-- Name: ogrenci_cevaplari_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ogrenci_cevaplari_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ogrenci_cevaplari_id_seq OWNER TO postgres;

--
-- Name: ogrenci_cevaplari_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ogrenci_cevaplari_id_seq OWNED BY public.ogrenci_cevaplari.id;


--
-- Name: ogrenci_cikis_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ogrenci_cikis_log (
    id integer NOT NULL,
    tarih text NOT NULL,
    saat text NOT NULL,
    numara text NOT NULL,
    ad_soyad text NOT NULL,
    paket text NOT NULL,
    ip text DEFAULT ''::text NOT NULL,
    kaynak text DEFAULT 'ogrenci'::text NOT NULL
);


ALTER TABLE public.ogrenci_cikis_log OWNER TO postgres;

--
-- Name: ogrenci_cikis_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ogrenci_cikis_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ogrenci_cikis_log_id_seq OWNER TO postgres;

--
-- Name: ogrenci_cikis_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ogrenci_cikis_log_id_seq OWNED BY public.ogrenci_cikis_log.id;


--
-- Name: ogrenciler; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ogrenciler (
    id integer NOT NULL,
    sinif_id integer NOT NULL,
    numara text NOT NULL,
    ad text NOT NULL,
    soyad text NOT NULL,
    sifre text DEFAULT ''::text NOT NULL
);


ALTER TABLE public.ogrenciler OWNER TO postgres;

--
-- Name: ogrenciler_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ogrenciler_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ogrenciler_id_seq OWNER TO postgres;

--
-- Name: ogrenciler_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ogrenciler_id_seq OWNED BY public.ogrenciler.id;


--
-- Name: ogrenme_ciktilari; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ogrenme_ciktilari (
    id integer NOT NULL,
    sinav_id integer NOT NULL,
    numara integer NOT NULL,
    metin text NOT NULL
);


ALTER TABLE public.ogrenme_ciktilari OWNER TO postgres;

--
-- Name: ogrenme_ciktilari_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ogrenme_ciktilari_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ogrenme_ciktilari_id_seq OWNER TO postgres;

--
-- Name: ogrenme_ciktilari_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ogrenme_ciktilari_id_seq OWNED BY public.ogrenme_ciktilari.id;


--
-- Name: sahte_giris_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sahte_giris_log (
    id integer NOT NULL,
    tarih text NOT NULL,
    saat text NOT NULL,
    ip text NOT NULL,
    gercek_numara text NOT NULL,
    gercek_ad text NOT NULL,
    denenen_numara text DEFAULT ''::text NOT NULL,
    denenen_ad text DEFAULT ''::text NOT NULL,
    sinif text DEFAULT ''::text NOT NULL
);


ALTER TABLE public.sahte_giris_log OWNER TO postgres;

--
-- Name: sahte_giris_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sahte_giris_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sahte_giris_log_id_seq OWNER TO postgres;

--
-- Name: sahte_giris_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sahte_giris_log_id_seq OWNED BY public.sahte_giris_log.id;


--
-- Name: seb_cikis_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seb_cikis_log (
    id integer NOT NULL,
    tarih text NOT NULL,
    saat text NOT NULL,
    numara text NOT NULL,
    ad_soyad text NOT NULL,
    ip text NOT NULL
);


ALTER TABLE public.seb_cikis_log OWNER TO postgres;

--
-- Name: seb_cikis_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seb_cikis_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seb_cikis_log_id_seq OWNER TO postgres;

--
-- Name: seb_cikis_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seb_cikis_log_id_seq OWNED BY public.seb_cikis_log.id;


--
-- Name: seb_cikis_talepleri; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seb_cikis_talepleri (
    id integer NOT NULL,
    tarih text NOT NULL,
    saat text NOT NULL,
    numara text NOT NULL,
    ad_soyad text NOT NULL,
    durum text DEFAULT 'bekliyor'::text
);


ALTER TABLE public.seb_cikis_talepleri OWNER TO postgres;

--
-- Name: seb_cikis_talepleri_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seb_cikis_talepleri_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seb_cikis_talepleri_id_seq OWNER TO postgres;

--
-- Name: seb_cikis_talepleri_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seb_cikis_talepleri_id_seq OWNED BY public.seb_cikis_talepleri.id;


--
-- Name: secenekler; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.secenekler (
    id integer NOT NULL,
    soru_id integer NOT NULL,
    metin text NOT NULL,
    dogru_mu integer DEFAULT 0
);


ALTER TABLE public.secenekler OWNER TO postgres;

--
-- Name: secenekler_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.secenekler_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.secenekler_id_seq OWNER TO postgres;

--
-- Name: secenekler_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.secenekler_id_seq OWNED BY public.secenekler.id;


--
-- Name: sinav_ihlaller; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sinav_ihlaller (
    id integer NOT NULL,
    sinav_id integer NOT NULL,
    ogrenci_numara text NOT NULL,
    sebep text DEFAULT 'fullscreen_exit'::text NOT NULL,
    aciklama text DEFAULT ''::text,
    zaman timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    durum text DEFAULT 'beklemede'::text NOT NULL
);


ALTER TABLE public.sinav_ihlaller OWNER TO postgres;

--
-- Name: sinav_ihlaller_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sinav_ihlaller_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sinav_ihlaller_id_seq OWNER TO postgres;

--
-- Name: sinav_ihlaller_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sinav_ihlaller_id_seq OWNED BY public.sinav_ihlaller.id;


--
-- Name: sinavlar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sinavlar (
    id integer NOT NULL,
    baslik text NOT NULL,
    aktif integer DEFAULT 0,
    olusturma_tarihi text NOT NULL
);


ALTER TABLE public.sinavlar OWNER TO postgres;

--
-- Name: sinavlar_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sinavlar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sinavlar_id_seq OWNER TO postgres;

--
-- Name: sinavlar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sinavlar_id_seq OWNED BY public.sinavlar.id;


--
-- Name: siniflar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.siniflar (
    id integer NOT NULL,
    ad text NOT NULL
);


ALTER TABLE public.siniflar OWNER TO postgres;

--
-- Name: siniflar_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.siniflar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.siniflar_id_seq OWNER TO postgres;

--
-- Name: siniflar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.siniflar_id_seq OWNED BY public.siniflar.id;


--
-- Name: soru_cikti_iliskisi; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.soru_cikti_iliskisi (
    id integer NOT NULL,
    soru_id integer NOT NULL,
    cikti_id integer NOT NULL
);


ALTER TABLE public.soru_cikti_iliskisi OWNER TO postgres;

--
-- Name: soru_cikti_iliskisi_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.soru_cikti_iliskisi_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.soru_cikti_iliskisi_id_seq OWNER TO postgres;

--
-- Name: soru_cikti_iliskisi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.soru_cikti_iliskisi_id_seq OWNED BY public.soru_cikti_iliskisi.id;


--
-- Name: sorular; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sorular (
    id integer NOT NULL,
    sinav_id integer NOT NULL,
    metin text NOT NULL,
    tip text DEFAULT 'cok_secmeli'::text NOT NULL,
    puan integer DEFAULT 10,
    bloom_seviyesi text DEFAULT ''::text,
    zorluk text DEFAULT ''::text
);


ALTER TABLE public.sorular OWNER TO postgres;

--
-- Name: sorular_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sorular_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sorular_id_seq OWNER TO postgres;

--
-- Name: sorular_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sorular_id_seq OWNED BY public.sorular.id;


--
-- Name: terminal_guvenlik_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.terminal_guvenlik_log (
    id integer NOT NULL,
    tarih text NOT NULL,
    saat text NOT NULL,
    ip text NOT NULL,
    session_numara text NOT NULL,
    session_ad text NOT NULL,
    girilen_numara text NOT NULL,
    durum text NOT NULL,
    uyari_gonderildi integer DEFAULT 0
);


ALTER TABLE public.terminal_guvenlik_log OWNER TO postgres;

--
-- Name: terminal_guvenlik_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.terminal_guvenlik_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.terminal_guvenlik_log_id_seq OWNER TO postgres;

--
-- Name: terminal_guvenlik_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.terminal_guvenlik_log_id_seq OWNED BY public.terminal_guvenlik_log.id;


--
-- Name: yardim_talepleri; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.yardim_talepleri (
    id integer NOT NULL,
    tarih text NOT NULL,
    saat text NOT NULL,
    numara text NOT NULL,
    ad_soyad text NOT NULL,
    durum text DEFAULT 'bekliyor'::text,
    kategori text DEFAULT ''::text
);


ALTER TABLE public.yardim_talepleri OWNER TO postgres;

--
-- Name: yardim_talepleri_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.yardim_talepleri_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.yardim_talepleri_id_seq OWNER TO postgres;

--
-- Name: yardim_talepleri_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.yardim_talepleri_id_seq OWNED BY public.yardim_talepleri.id;


--
-- Name: yoklama; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.yoklama (
    id integer NOT NULL,
    tarih text NOT NULL,
    ad_soyad text NOT NULL,
    numara text NOT NULL,
    saat text NOT NULL,
    sinif text DEFAULT ''::text NOT NULL,
    paket text DEFAULT '—'::text NOT NULL,
    ip text DEFAULT ''::text NOT NULL,
    kaynak text DEFAULT 'web'::text NOT NULL
);


ALTER TABLE public.yoklama OWNER TO postgres;

--
-- Name: yoklama_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.yoklama_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.yoklama_id_seq OWNER TO postgres;

--
-- Name: yoklama_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.yoklama_id_seq OWNED BY public.yoklama.id;


--
-- Name: yoklama_override; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.yoklama_override (
    id integer NOT NULL,
    numara text NOT NULL,
    hafta integer NOT NULL,
    durum text DEFAULT 'katildi'::text NOT NULL,
    tarih text NOT NULL,
    ogretmen text DEFAULT ''::text
);


ALTER TABLE public.yoklama_override OWNER TO postgres;

--
-- Name: yoklama_override_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.yoklama_override_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.yoklama_override_id_seq OWNER TO postgres;

--
-- Name: yoklama_override_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.yoklama_override_id_seq OWNED BY public.yoklama_override.id;


--
-- Name: ogrenci_aktivite_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenci_aktivite_log ALTER COLUMN id SET DEFAULT nextval('public.ogrenci_aktivite_log_id_seq'::regclass);


--
-- Name: ogrenci_cevaplari id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenci_cevaplari ALTER COLUMN id SET DEFAULT nextval('public.ogrenci_cevaplari_id_seq'::regclass);


--
-- Name: ogrenci_cikis_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenci_cikis_log ALTER COLUMN id SET DEFAULT nextval('public.ogrenci_cikis_log_id_seq'::regclass);


--
-- Name: ogrenciler id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenciler ALTER COLUMN id SET DEFAULT nextval('public.ogrenciler_id_seq'::regclass);


--
-- Name: ogrenme_ciktilari id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenme_ciktilari ALTER COLUMN id SET DEFAULT nextval('public.ogrenme_ciktilari_id_seq'::regclass);


--
-- Name: sahte_giris_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sahte_giris_log ALTER COLUMN id SET DEFAULT nextval('public.sahte_giris_log_id_seq'::regclass);


--
-- Name: seb_cikis_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seb_cikis_log ALTER COLUMN id SET DEFAULT nextval('public.seb_cikis_log_id_seq'::regclass);


--
-- Name: seb_cikis_talepleri id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seb_cikis_talepleri ALTER COLUMN id SET DEFAULT nextval('public.seb_cikis_talepleri_id_seq'::regclass);


--
-- Name: secenekler id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.secenekler ALTER COLUMN id SET DEFAULT nextval('public.secenekler_id_seq'::regclass);


--
-- Name: sinav_ihlaller id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sinav_ihlaller ALTER COLUMN id SET DEFAULT nextval('public.sinav_ihlaller_id_seq'::regclass);


--
-- Name: sinavlar id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sinavlar ALTER COLUMN id SET DEFAULT nextval('public.sinavlar_id_seq'::regclass);


--
-- Name: siniflar id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.siniflar ALTER COLUMN id SET DEFAULT nextval('public.siniflar_id_seq'::regclass);


--
-- Name: soru_cikti_iliskisi id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soru_cikti_iliskisi ALTER COLUMN id SET DEFAULT nextval('public.soru_cikti_iliskisi_id_seq'::regclass);


--
-- Name: sorular id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sorular ALTER COLUMN id SET DEFAULT nextval('public.sorular_id_seq'::regclass);


--
-- Name: terminal_guvenlik_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.terminal_guvenlik_log ALTER COLUMN id SET DEFAULT nextval('public.terminal_guvenlik_log_id_seq'::regclass);


--
-- Name: yardim_talepleri id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.yardim_talepleri ALTER COLUMN id SET DEFAULT nextval('public.yardim_talepleri_id_seq'::regclass);


--
-- Name: yoklama id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.yoklama ALTER COLUMN id SET DEFAULT nextval('public.yoklama_id_seq'::regclass);


--
-- Name: yoklama_override id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.yoklama_override ALTER COLUMN id SET DEFAULT nextval('public.yoklama_override_id_seq'::regclass);


--
-- Data for Name: ayarlar; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ayarlar (anahtar, deger) FROM stdin;
ogretmen_sifre	1234
chroot_host	10.211.55.27
chroot_port	22
chroot_user	bekir
chroot_pass	123123
system_host	
terminal_url	/terminal
kiosk_modu	0
ip_kontrol	0
cikis_izni	1
ders_gunleri	1
slayt_klasoru	/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/01_SUNUMLAR/html
db_type	postgres
db_host	db
db_port	5432
db_user	postgres
db_pass	postgres_pass
db_name	ders_takip
devamsizlik_esik	3
\.


--
-- Data for Name: ogrenci_aktivite_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ogrenci_aktivite_log (id, numara, ip, aktivite_tipi, detay, tarih, saat) FROM stdin;
\.


--
-- Data for Name: ogrenci_cevaplari; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ogrenci_cevaplari (id, sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan, cevap_zamani, taslak) FROM stdin;
1	1	25904011	1	1	10	2026-04-12 19:13:01.132805	0
2	1	25905009	1	2	0	2026-04-12 19:13:01.132805	0
3	1	25901010	1	3	0	2026-04-12 19:13:01.132805	0
4	1	123	1	4	0	2026-04-12 19:13:01.132805	0
7	1	25901013	1	1	10	2026-04-12 19:13:01.132805	0
8	1	25901013	4	rm	15	2026-04-12 19:13:01.132805	0
9	3	test1	6	14	0	2026-04-12 19:13:01.132805	0
10	3	test1	7	15	20	2026-04-12 19:13:01.132805	0
11	3	test1	8	20	0	2026-04-12 19:13:01.132805	0
12	3	test1	9	rm	25	2026-04-12 19:13:01.132805	0
13	3	test1	10	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
14	3	test2	6	12	0	2026-04-12 19:13:01.132805	0
15	3	test2	7	18	0	2026-04-12 19:13:01.132805	0
16	3	test2	8	20	0	2026-04-12 19:13:01.132805	0
17	3	test2	9	rm	25	2026-04-12 19:13:01.132805	0
18	3	test2	10	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
19	3	test3	6	14	0	2026-04-12 19:13:01.132805	0
20	3	test3	7	17	0	2026-04-12 19:13:01.132805	0
21	3	test3	8	20	0	2026-04-12 19:13:01.132805	0
22	3	test3	9	rm	25	2026-04-12 19:13:01.132805	0
23	3	test3	10	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
24	3	test4	6	13	0	2026-04-12 19:13:01.132805	0
25	3	test4	7	17	0	2026-04-12 19:13:01.132805	0
26	3	test4	8	20	0	2026-04-12 19:13:01.132805	0
27	3	test4	9	del	0	2026-04-12 19:13:01.132805	0
28	3	test4	10	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
29	3	test5	6	12	0	2026-04-12 19:13:01.132805	0
30	3	test5	7	15	20	2026-04-12 19:13:01.132805	0
31	3	test5	8	19	10	2026-04-12 19:13:01.132805	0
32	3	test5	9	del	0	2026-04-12 19:13:01.132805	0
33	3	test5	10	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
34	4	test1	11	22	20	2026-04-12 19:13:01.132805	0
35	4	test1	12	26	20	2026-04-12 19:13:01.132805	0
36	4	test1	13	31	0	2026-04-12 19:13:01.132805	0
37	4	test1	14	rm	25	2026-04-12 19:13:01.132805	0
38	4	test1	15	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
39	4	test2	11	22	20	2026-04-12 19:13:01.132805	0
40	4	test2	12	28	0	2026-04-12 19:13:01.132805	0
41	4	test2	13	30	10	2026-04-12 19:13:01.132805	0
42	4	test2	14	delete	0	2026-04-12 19:13:01.132805	0
43	4	test2	15	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
44	4	test3	11	24	0	2026-04-12 19:13:01.132805	0
45	4	test3	12	29	0	2026-04-12 19:13:01.132805	0
46	4	test3	13	30	10	2026-04-12 19:13:01.132805	0
47	4	test3	14	rm	25	2026-04-12 19:13:01.132805	0
48	4	test3	15	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
49	4	test4	11	25	0	2026-04-12 19:13:01.132805	0
50	4	test4	12	26	20	2026-04-12 19:13:01.132805	0
51	4	test4	13	31	0	2026-04-12 19:13:01.132805	0
52	4	test4	14	rm	25	2026-04-12 19:13:01.132805	0
53	4	test4	15	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
54	4	test5	11	24	0	2026-04-12 19:13:01.132805	0
55	4	test5	12	28	0	2026-04-12 19:13:01.132805	0
56	4	test5	13	31	0	2026-04-12 19:13:01.132805	0
57	4	test5	14	rm	25	2026-04-12 19:13:01.132805	0
58	4	test5	15	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
59	5	test1	16	33	20	2026-04-12 19:13:01.132805	0
60	5	test1	17	38	0	2026-04-12 19:13:01.132805	0
61	5	test1	18	42	0	2026-04-12 19:13:01.132805	0
62	5	test1	19	rm	25	2026-04-12 19:13:01.132805	0
63	5	test1	20	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
64	5	test2	16	34	0	2026-04-12 19:13:01.132805	0
65	5	test2	17	40	0	2026-04-12 19:13:01.132805	0
66	5	test2	18	42	0	2026-04-12 19:13:01.132805	0
67	5	test2	19	del	0	2026-04-12 19:13:01.132805	0
68	5	test2	20	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
69	5	test3	16	34	0	2026-04-12 19:13:01.132805	0
70	5	test3	17	37	20	2026-04-12 19:13:01.132805	0
71	5	test3	18	41	10	2026-04-12 19:13:01.132805	0
72	5	test3	19	delete	0	2026-04-12 19:13:01.132805	0
73	5	test3	20	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
74	5	test4	16	35	0	2026-04-12 19:13:01.132805	0
75	5	test4	17	40	0	2026-04-12 19:13:01.132805	0
76	5	test4	18	42	0	2026-04-12 19:13:01.132805	0
77	5	test4	19	delete	0	2026-04-12 19:13:01.132805	0
78	5	test4	20	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
79	5	test5	16	33	20	2026-04-12 19:13:01.132805	0
80	5	test5	17	39	0	2026-04-12 19:13:01.132805	0
81	5	test5	18	42	0	2026-04-12 19:13:01.132805	0
82	5	test5	19	rm	25	2026-04-12 19:13:01.132805	0
83	5	test5	20	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
84	6	test1	21	46	0	2026-04-12 19:13:01.132805	0
85	6	test1	22	48	20	2026-04-12 19:13:01.132805	0
86	6	test1	23	52	10	2026-04-12 19:13:01.132805	0
87	6	test1	24	del	0	2026-04-12 19:13:01.132805	0
88	6	test1	25	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
89	6	test2	21	46	0	2026-04-12 19:13:01.132805	0
90	6	test2	22	50	0	2026-04-12 19:13:01.132805	0
91	6	test2	23	52	10	2026-04-12 19:13:01.132805	0
92	6	test2	24	del	0	2026-04-12 19:13:01.132805	0
93	6	test2	25	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
94	6	test3	21	45	0	2026-04-12 19:13:01.132805	0
95	6	test3	22	50	0	2026-04-12 19:13:01.132805	0
96	6	test3	23	52	10	2026-04-12 19:13:01.132805	0
97	6	test3	24	rm	25	2026-04-12 19:13:01.132805	0
98	6	test3	25	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
99	6	test4	21	46	0	2026-04-12 19:13:01.132805	0
100	6	test4	22	51	0	2026-04-12 19:13:01.132805	0
101	6	test4	23	52	10	2026-04-12 19:13:01.132805	0
102	6	test4	24	rm	25	2026-04-12 19:13:01.132805	0
103	6	test4	25	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
104	6	test5	21	45	0	2026-04-12 19:13:01.132805	0
105	6	test5	22	50	0	2026-04-12 19:13:01.132805	0
106	6	test5	23	53	0	2026-04-12 19:13:01.132805	0
107	6	test5	24	rm	25	2026-04-12 19:13:01.132805	0
108	6	test5	25	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
109	7	test1	26	55	20	2026-04-12 19:13:01.132805	0
110	7	test1	27	59	20	2026-04-12 19:13:01.132805	0
111	7	test1	28	64	0	2026-04-12 19:13:01.132805	0
112	7	test1	29	del	0	2026-04-12 19:13:01.132805	0
113	7	test1	30	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
114	7	test2	26	58	0	2026-04-12 19:13:01.132805	0
115	7	test2	27	62	0	2026-04-12 19:13:01.132805	0
116	7	test2	28	63	10	2026-04-12 19:13:01.132805	0
117	7	test2	29	rm	25	2026-04-12 19:13:01.132805	0
118	7	test2	30	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
119	7	test3	26	57	0	2026-04-12 19:13:01.132805	0
120	7	test3	27	59	20	2026-04-12 19:13:01.132805	0
121	7	test3	28	64	0	2026-04-12 19:13:01.132805	0
122	7	test3	29	rm	25	2026-04-12 19:13:01.132805	0
123	7	test3	30	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
124	7	test4	26	58	0	2026-04-12 19:13:01.132805	0
125	7	test4	27	60	0	2026-04-12 19:13:01.132805	0
126	7	test4	28	63	10	2026-04-12 19:13:01.132805	0
127	7	test4	29	rm	25	2026-04-12 19:13:01.132805	0
128	7	test4	30	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
129	7	test5	26	57	0	2026-04-12 19:13:01.132805	0
130	7	test5	27	61	0	2026-04-12 19:13:01.132805	0
131	7	test5	28	63	10	2026-04-12 19:13:01.132805	0
132	7	test5	29	rm	25	2026-04-12 19:13:01.132805	0
133	7	test5	30	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
134	8	test1	31	68	0	2026-04-12 19:13:01.132805	0
135	8	test1	32	71	0	2026-04-12 19:13:01.132805	0
136	8	test1	33	74	10	2026-04-12 19:13:01.132805	0
137	8	test1	34	rm	25	2026-04-12 19:13:01.132805	0
138	8	test1	35	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
139	8	test2	31	69	0	2026-04-12 19:13:01.132805	0
140	8	test2	32	72	0	2026-04-12 19:13:01.132805	0
141	8	test2	33	74	10	2026-04-12 19:13:01.132805	0
142	8	test2	34	delete	0	2026-04-12 19:13:01.132805	0
143	8	test2	35	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
144	8	test3	31	66	20	2026-04-12 19:13:01.132805	0
145	8	test3	32	72	0	2026-04-12 19:13:01.132805	0
146	8	test3	33	75	0	2026-04-12 19:13:01.132805	0
147	8	test3	34	del	0	2026-04-12 19:13:01.132805	0
148	8	test3	35	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
149	8	test4	31	67	0	2026-04-12 19:13:01.132805	0
150	8	test4	32	71	0	2026-04-12 19:13:01.132805	0
151	8	test4	33	75	0	2026-04-12 19:13:01.132805	0
152	8	test4	34	rm	25	2026-04-12 19:13:01.132805	0
153	8	test4	35	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
154	8	test5	31	68	0	2026-04-12 19:13:01.132805	0
155	8	test5	32	71	0	2026-04-12 19:13:01.132805	0
156	8	test5	33	75	0	2026-04-12 19:13:01.132805	0
157	8	test5	34	del	0	2026-04-12 19:13:01.132805	0
158	8	test5	35	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
159	9	test1	36	80	0	2026-04-12 19:13:01.132805	0
160	9	test1	37	83	0	2026-04-12 19:13:01.132805	0
161	9	test1	38	86	0	2026-04-12 19:13:01.132805	0
162	9	test1	39	rm	25	2026-04-12 19:13:01.132805	0
163	9	test1	40	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
164	9	test2	36	78	0	2026-04-12 19:13:01.132805	0
165	9	test2	37	81	20	2026-04-12 19:13:01.132805	0
166	9	test2	38	86	0	2026-04-12 19:13:01.132805	0
167	9	test2	39	del	0	2026-04-12 19:13:01.132805	0
168	9	test2	40	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
169	9	test3	36	79	0	2026-04-12 19:13:01.132805	0
170	9	test3	37	84	0	2026-04-12 19:13:01.132805	0
171	9	test3	38	86	0	2026-04-12 19:13:01.132805	0
172	9	test3	39	rm	25	2026-04-12 19:13:01.132805	0
173	9	test3	40	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
174	9	test4	36	80	0	2026-04-12 19:13:01.132805	0
175	9	test4	37	81	20	2026-04-12 19:13:01.132805	0
176	9	test4	38	85	10	2026-04-12 19:13:01.132805	0
177	9	test4	39	rm	25	2026-04-12 19:13:01.132805	0
178	9	test4	40	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
179	9	test5	36	79	0	2026-04-12 19:13:01.132805	0
180	9	test5	37	83	0	2026-04-12 19:13:01.132805	0
181	9	test5	38	86	0	2026-04-12 19:13:01.132805	0
182	9	test5	39	rm	25	2026-04-12 19:13:01.132805	0
183	9	test5	40	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
184	10	test1	41	91	0	2026-04-12 19:13:01.132805	0
185	10	test1	42	94	0	2026-04-12 19:13:01.132805	0
186	10	test1	43	97	0	2026-04-12 19:13:01.132805	0
187	10	test1	44	rm	25	2026-04-12 19:13:01.132805	0
188	10	test1	45	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
189	10	test2	41	89	0	2026-04-12 19:13:01.132805	0
190	10	test2	42	95	0	2026-04-12 19:13:01.132805	0
191	10	test2	43	96	10	2026-04-12 19:13:01.132805	0
192	10	test2	44	rm	25	2026-04-12 19:13:01.132805	0
193	10	test2	45	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
194	10	test3	41	90	0	2026-04-12 19:13:01.132805	0
195	10	test3	42	93	0	2026-04-12 19:13:01.132805	0
196	10	test3	43	97	0	2026-04-12 19:13:01.132805	0
197	10	test3	44	rm	25	2026-04-12 19:13:01.132805	0
198	10	test3	45	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
199	10	test4	41	91	0	2026-04-12 19:13:01.132805	0
200	10	test4	42	94	0	2026-04-12 19:13:01.132805	0
201	10	test4	43	96	10	2026-04-12 19:13:01.132805	0
202	10	test4	44	delete	0	2026-04-12 19:13:01.132805	0
203	10	test4	45	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
204	10	test5	41	88	20	2026-04-12 19:13:01.132805	0
205	10	test5	42	94	0	2026-04-12 19:13:01.132805	0
206	10	test5	43	97	0	2026-04-12 19:13:01.132805	0
207	10	test5	44	rm	25	2026-04-12 19:13:01.132805	0
208	10	test5	45	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
209	11	test4	46	102	0	2026-04-12 19:13:01.132805	0
210	12	test1	47	104	0	2026-04-12 19:13:01.132805	0
211	12	test1	48	109	0	2026-04-12 19:13:01.132805	0
212	12	test1	49	111	10	2026-04-12 19:13:01.132805	0
213	12	test1	50	delete	0	2026-04-12 19:13:01.132805	0
214	12	test1	51	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
215	12	test2	47	104	0	2026-04-12 19:13:01.132805	0
216	12	test2	48	107	20	2026-04-12 19:13:01.132805	0
217	12	test2	49	112	0	2026-04-12 19:13:01.132805	0
218	12	test2	50	del	0	2026-04-12 19:13:01.132805	0
219	12	test2	51	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
220	12	test3	47	104	0	2026-04-12 19:13:01.132805	0
221	12	test3	48	108	0	2026-04-12 19:13:01.132805	0
222	12	test3	49	112	0	2026-04-12 19:13:01.132805	0
223	12	test3	50	del	0	2026-04-12 19:13:01.132805	0
224	12	test3	51	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
225	12	test4	47	106	0	2026-04-12 19:13:01.132805	0
226	12	test4	48	109	0	2026-04-12 19:13:01.132805	0
227	12	test4	49	111	10	2026-04-12 19:13:01.132805	0
228	12	test4	50	del	0	2026-04-12 19:13:01.132805	0
229	12	test4	51	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
230	12	test5	47	103	20	2026-04-12 19:13:01.132805	0
231	12	test5	48	107	20	2026-04-12 19:13:01.132805	0
232	12	test5	49	111	10	2026-04-12 19:13:01.132805	0
233	12	test5	50	rm	25	2026-04-12 19:13:01.132805	0
234	12	test5	51	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
235	13	test1	52	116	0	2026-04-12 19:13:01.132805	0
236	13	test1	53	121	0	2026-04-12 19:13:01.132805	0
237	13	test1	54	123	0	2026-04-12 19:13:01.132805	0
238	13	test1	55	rm	25	2026-04-12 19:13:01.132805	0
239	13	test1	56	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
240	13	test2	52	116	0	2026-04-12 19:13:01.132805	0
241	13	test2	53	120	0	2026-04-12 19:13:01.132805	0
242	13	test2	54	122	10	2026-04-12 19:13:01.132805	0
243	13	test2	55	delete	0	2026-04-12 19:13:01.132805	0
244	13	test2	56	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
245	13	test3	52	115	0	2026-04-12 19:13:01.132805	0
246	13	test3	53	119	0	2026-04-12 19:13:01.132805	0
247	13	test3	54	123	0	2026-04-12 19:13:01.132805	0
248	13	test3	55	rm	25	2026-04-12 19:13:01.132805	0
249	13	test3	56	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
250	13	test4	52	117	0	2026-04-12 19:13:01.132805	0
251	13	test4	53	119	0	2026-04-12 19:13:01.132805	0
252	13	test4	54	122	10	2026-04-12 19:13:01.132805	0
253	13	test4	55	delete	0	2026-04-12 19:13:01.132805	0
254	13	test4	56	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
255	13	test5	52	116	0	2026-04-12 19:13:01.132805	0
256	13	test5	53	119	0	2026-04-12 19:13:01.132805	0
257	13	test5	54	123	0	2026-04-12 19:13:01.132805	0
258	13	test5	55	rm	25	2026-04-12 19:13:01.132805	0
259	13	test5	56	/ kök dizin, /home kullanıcılar, /etc ayarlar...	0	2026-04-12 19:13:01.132805	0
260	11	001	46	99	10	2026-04-12 19:13:01.132805	0
261	11	test1	46	101	0	2026-04-12 19:13:01.132805	0
262	11	test5	46	102	0	2026-04-12 19:13:01.132805	0
263	11	test2	46	101	0	2026-04-12 19:13:01.132805	0
\.


--
-- Data for Name: ogrenci_cikis_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ogrenci_cikis_log (id, tarih, saat, numara, ad_soyad, paket, ip, kaynak) FROM stdin;
1	2026-03-29	23:56:33	123	TEST TEST	—	ogretmen	force
2	2026-03-30	09:19:00	25904005	SUDE ELMAS AYKIRI	1. Paket (09:00-11:35)	172.16.0.177	ogrenci
3	2026-03-30	09:31:19	25905009	VEYSEL KAAN DÜMAN	1. Paket (09:00-11:35)	172.16.0.62	ogrenci
4	2026-03-30	09:40:08	25901003	FURKAN SAFA ÇÜRÜTTÜ	1. Paket (09:00-11:35)	172.16.0.23	ogrenci
5	2026-03-30	10:34:31	25902002	ENES ÖZTÜRK	1. Paket (09:00-11:35)	172.16.0.70	ogrenci
6	2026-03-30	10:57:34	25902001	İLKAY ŞIK	1. Paket (09:00-11:35)	172.16.0.47	ogrenci
7	2026-03-30	10:57:53	25901011	EFEKAN İÇÖZ	1. Paket (09:00-11:35)	172.16.0.26	ogrenci
8	2026-03-30	10:58:17	25902001	İLKAY ŞIK	1. Paket (09:00-11:35)	172.16.0.47	ogrenci
9	2026-03-30	11:07:25	25903015	SEVİM ÇELİK	1. Paket (09:00-11:35)	172.16.0.41	ogrenci
10	2026-03-30	11:18:15	25902004	EYLÜL KAYA	1. Paket (09:00-11:35)	172.16.0.112	ogrenci
11	2026-03-30	11:18:36	25903015	SEVİM ÇELİK	1. Paket (09:00-11:35)	172.16.0.41	ogrenci
12	2026-03-30	11:18:37	25905009	VEYSEL KAAN DÜMAN	1. Paket (09:00-11:35)	172.16.0.62	ogrenci
13	2026-03-30	11:18:38	24090003	EFE BARAN DEMIRHAN	1. Paket (09:00-11:35)	172.16.0.14	ogrenci
14	2026-03-30	11:18:39	25903006	ESMANUR DİNÇER	1. Paket (09:00-11:35)	172.16.0.179	ogrenci
15	2026-03-30	11:18:40	25905001	AHMET BAŞOĞLU	1. Paket (09:00-11:35)	172.16.0.104	ogrenci
16	2026-03-30	11:18:44	25905003	DİLEK KARAÇE	1. Paket (09:00-11:35)	172.16.0.120	ogrenci
17	2026-03-30	11:18:46	25901005	SALİH BİLAL KORKMAZ	1. Paket (09:00-11:35)	172.16.0.10	ogrenci
18	2026-03-30	11:18:46	25904002	SALİH GÖKAY KÖKSAL	1. Paket (09:00-11:35)	172.16.0.66	ogrenci
19	2026-03-30	11:18:48	25904005	SUDE ELMAS AYKIRI	1. Paket (09:00-11:35)	172.16.0.177	ogrenci
20	2026-03-30	11:18:49	25904032	AGAH ABDULLAH SARSILMAZ	1. Paket (09:00-11:35)	172.16.0.84	ogrenci
21	2026-03-30	11:18:51	25902001	İLKAY ŞIK	1. Paket (09:00-11:35)	172.16.0.47	ogrenci
22	2026-03-30	11:18:53	25904026	ONUR YENİPAZARLI	1. Paket (09:00-11:35)	172.16.0.72	ogrenci
23	2026-03-30	11:18:54	25903012	MUHAMMED HAKTAN SAZÇALAN	1. Paket (09:00-11:35)	172.16.0.63	ogrenci
24	2026-03-30	11:18:54	25905011	KAMURAN İNAN AYDOĞAN	1. Paket (09:00-11:35)	172.16.0.113	ogrenci
25	2026-03-30	11:18:55	25901010	KAZIM EFE TAŞDEMİR	1. Paket (09:00-11:35)	172.16.0.10	ogrenci
26	2026-03-30	11:18:56	25901007	ARDA KARATAŞ	1. Paket (09:00-11:35)	172.16.0.114	ogrenci
27	2026-03-30	11:19:01	25904035	GÖKTUĞ ERDEM PEHLİVAN	1. Paket (09:00-11:35)	172.16.0.57	ogrenci
28	2026-03-30	11:19:24	25904006	İREM GENEŞ	1. Paket (09:00-11:35)	172.16.0.107	ogrenci
29	2026-03-30	13:13:35	25902024	EFEHAN EKINCI	2. Paket (12:40-15:15)	172.16.0.179	ogrenci
30	2026-03-30	13:44:56	25905002	TUANNA ALTIN	2. Paket (12:40-15:15)	172.16.0.125	ogrenci
31	2026-03-30	13:50:00	25905002	TUANNA ALTIN	2. Paket (12:40-15:15)	172.16.0.125	ogrenci
32	2026-03-30	13:50:58	25905002	TUANNA ALTIN	2. Paket (12:40-15:15)	172.16.0.125	ogrenci
33	2026-03-30	14:32:39	25905002	TUANNA ALTIN	2. Paket (12:40-15:15)	172.16.0.125	ogrenci
34	2026-03-30	14:37:55	25903002	İREM UYSAL	2. Paket (12:40-15:15)	ogretmen	force
35	2026-03-30	14:38:20	25905002	TUANNA ALTIN	2. Paket (12:40-15:15)	172.16.0.125	ogrenci
36	2026-03-30	14:48:11	25903013	AHMET MERT KÖYBAŞI	2. Paket (12:40-15:15)	172.16.0.41	ogrenci
37	2026-03-30	14:51:03	25903004	MİRAY KAMİLE TİRAŞ	2. Paket (12:40-15:15)	172.16.0.139	ogrenci
38	2026-03-30	14:53:00	25904025	ÖYKÜM NİLDENİZ AKPINAR	2. Paket (12:40-15:15)	172.16.0.113	ogrenci
39	2026-03-30	14:54:31	25904027	YUSUF ŞAHBAZ	2. Paket (12:40-15:15)	172.16.0.182	ogrenci
40	2026-03-30	14:54:52	25903011	SEMİH ÇELİKEL	2. Paket (12:40-15:15)	172.16.0.63	ogrenci
41	2026-03-30	14:55:07	25903013	AHMET MERT KÖYBAŞI	2. Paket (12:40-15:15)	172.16.0.41	ogrenci
42	2026-03-30	14:55:15	25903002	İREM UYSAL	2. Paket (12:40-15:15)	172.16.0.61	ogrenci
43	2026-03-30	14:55:16	25904019	YUSUF ENES BİLGİN	2. Paket (12:40-15:15)	172.16.0.108	ogrenci
44	2026-03-30	14:55:20	25903010	AZRA ŞAHİN	2. Paket (12:40-15:15)	172.16.0.39	ogrenci
45	2026-03-30	14:55:22	25904025	ÖYKÜM NİLDENİZ AKPINAR	2. Paket (12:40-15:15)	172.16.0.113	ogrenci
46	2026-03-30	14:55:24	25904017	SAFA HASOĞLU	2. Paket (12:40-15:15)	172.16.0.118	ogrenci
47	2026-03-30	14:55:27	25904010	EMİRHAN ESENOĞLU	2. Paket (12:40-15:15)	172.16.0.66	ogrenci
48	2026-03-30	14:55:31	25904014	AHMET TAYLAN ERDEN	2. Paket (12:40-15:15)	172.16.0.44	ogrenci
49	2026-03-30	14:55:34	25903004	MİRAY KAMİLE TİRAŞ	2. Paket (12:40-15:15)	172.16.0.139	ogrenci
50	2026-03-30	14:55:37	25904030	AYŞE DEMİRKAYA	2. Paket (12:40-15:15)	172.16.0.70	ogrenci
51	2026-03-30	14:56:00	25903008	HATİCE ÖZLÜ	2. Paket (12:40-15:15)	172.16.0.120	ogrenci
52	2026-03-30	14:56:04	25903007	TUĞBA GÜLMEZ	2. Paket (12:40-15:15)	172.16.0.112	ogrenci
53	2026-03-30	14:56:44	25902025	BURAK AYYILDIZ	2. Paket (12:40-15:15)	172.16.0.121	ogrenci
54	2026-03-30	15:59:16	25904028	BÜNYAMİN EFE BULUT	3. Paket (15:25-18:00)	172.16.0.57	ogrenci
55	2026-03-30	16:00:28	25905028	YASİN BOLAT	3. Paket (15:25-18:00)	172.16.0.14	ogrenci
56	2026-03-30	16:01:46	25904037	MUHAMMED EFENDİ AYHANOĞLU	3. Paket (15:25-18:00)	172.16.0.72	ogrenci
57	2026-03-30	16:29:56	25146901	SAMI KARACA	3. Paket (15:25-18:00)	172.16.0.139	ogrenci
58	2026-03-30	16:31:20	25146901	SAMI KARACA	3. Paket (15:25-18:00)	172.16.0.139	ogrenci
59	2026-03-30	17:07:04	25905017	MEHMET ARDA YENENER	3. Paket (15:25-18:00)	172.16.0.62	ogrenci
60	2026-03-30	17:07:12	25904024	SUDE ÖZTÜRK	3. Paket (15:25-18:00)	172.16.0.39	ogrenci
61	2026-03-30	17:10:31	25904043	HASAN BERK KOCA	3. Paket (15:25-18:00)	172.16.0.84	ogrenci
62	2026-03-30	17:10:34	25904037	MUHAMMED EFENDİ AYHANOĞLU	3. Paket (15:25-18:00)	172.16.0.72	ogrenci
63	2026-03-30	17:11:53	25904028	BÜNYAMİN EFE BULUT	3. Paket (15:25-18:00)	172.16.0.57	ogrenci
64	2026-03-30	17:12:00	25904037	MUHAMMED EFENDİ AYHANOĞLU	3. Paket (15:25-18:00)	172.16.0.72	ogrenci
65	2026-03-30	17:12:32	25904022	MEHMET KAYRA AKKUŞ	3. Paket (15:25-18:00)	172.16.0.113	ogrenci
66	2026-03-30	17:39:46	25146901	SAMI KARACA	3. Paket (15:25-18:00)	172.16.0.47	ogrenci
67	2026-03-30	17:44:19	25905017	MEHMET ARDA YENENER	3. Paket (15:25-18:00)	172.16.0.62	ogrenci
68	2026-03-30	17:44:47	25905017	MEHMET ARDA YENENER	3. Paket (15:25-18:00)	172.16.0.62	ogrenci
69	2026-03-30	17:49:35	25904016	MEHMET ENES KAYA	3. Paket (15:25-18:00)	172.16.0.179	ogrenci
70	2026-03-30	17:49:37	25904022	MEHMET KAYRA AKKUŞ	3. Paket (15:25-18:00)	172.16.0.113	ogrenci
71	2026-03-30	17:49:38	25904004	SÜLEYMAN ESER DİNÇ	3. Paket (15:25-18:00)	172.16.0.118	ogrenci
72	2026-03-30	17:49:41	25904007	ERTÜMEN YAYLA	3. Paket (15:25-18:00)	172.16.0.104	ogrenci
73	2026-03-30	17:49:45	25905017	MEHMET ARDA YENENER	3. Paket (15:25-18:00)	172.16.0.62	ogrenci
74	2026-04-01	16:14:39	123	TEST TEST	3. Paket (15:25-18:00)	127.0.0.1	ogrenci
75	2026-04-02	22:45:51	001	A B	—	192.168.111.53	ogrenci
76	2026-04-02	22:46:20	test1	Öğrenci-1 TEST	—	192.168.111.53	ogrenci
77	2026-04-02	22:47:31	test4	Öğrenci-4 TEST	—	192.168.111.53	ogrenci
78	2026-04-02	22:48:23	test5	Öğrenci-5 TEST	—	192.168.111.53	ogrenci
79	2026-04-02	23:13:21	test1	Öğrenci-1 TEST	—	192.168.111.53	ogrenci
80	2026-04-02	23:14:08	test2	Öğrenci-2 TEST	—	192.168.111.53	ogrenci
81	2026-04-02	23:15:14	test1	Öğrenci-1 TEST	—	192.168.111.53	ogrenci
82	2026-04-02	23:57:52	test1	Öğrenci-1 TEST	—	192.168.111.53	ogrenci
83	2026-04-03	00:02:10	test1	Öğrenci-1 TEST	—	127.0.0.1	ogrenci
84	2026-04-06	09:51:19	25902004	EYLÜL KAYA	1. Paket (09:00-11:35)	172.16.0.112	ogrenci
85	2026-04-06	09:59:33	25904029	EFZA KAÇMAZ	1. Paket (09:00-11:35)	172.16.0.101	ogrenci
86	2026-04-06	10:26:35	25904011	FURKAN İLİK	1. Paket (09:00-11:35)	172.16.0.118	ogrenci
87	2026-04-06	10:28:09	25905001	AHMET BAŞOĞLU	1. Paket (09:00-11:35)	172.16.0.108	ogrenci
88	2026-04-06	10:28:16	25904011	FURKAN İLİK	1. Paket (09:00-11:35)	172.16.0.118	ogrenci
89	2026-04-06	10:29:30	25904011	FURKAN İLİK	1. Paket (09:00-11:35)	172.16.0.118	ogrenci
90	2026-04-06	12:59:54	25902014	ZÜBEYİR CUMA YILMAZ	2. Paket (12:40-15:15)	172.16.0.104	ogrenci
91	2026-04-06	13:04:07	25902014	ZÜBEYİR CUMA YILMAZ	2. Paket (12:40-15:15)	172.16.0.104	ogrenci
92	2026-04-06	13:54:54	25904003	SÜHEYLA TUĞÇE GÜN	2. Paket (12:40-15:15)	172.16.0.18	ogrenci
93	2026-04-06	14:29:07	25901006	EREN GÜLER	2. Paket (12:40-15:15)	172.16.0.121	ogrenci
94	2026-04-06	14:29:20	25904039	ÖMER FARUK GÖKSU	2. Paket (12:40-15:15)	172.16.0.55	ogrenci
95	2026-04-06	14:29:48	25901010	KAZIM EFE TAŞDEMİR	2. Paket (12:40-15:15)	172.16.0.61	ogrenci
96	2026-04-06	14:38:53	25902009	RESUL EKREM ÖZCAN	2. Paket (12:40-15:15)	172.16.0.126	ogrenci
97	2026-04-06	14:38:55	25901010	KAZIM EFE TAŞDEMİR	2. Paket (12:40-15:15)	172.16.0.61	ogrenci
98	2026-04-06	14:38:55	25902008	MUSTAFA ÇETİN	2. Paket (12:40-15:15)	172.16.0.23	ogrenci
99	2026-04-06	14:38:57	25903013	AHMET MERT KÖYBAŞI	2. Paket (12:40-15:15)	172.16.0.182	ogrenci
100	2026-04-06	14:38:57	25903001	AHMET MAHLİ	2. Paket (12:40-15:15)	172.16.0.118	ogrenci
101	2026-04-06	14:38:59	25904039	ÖMER FARUK GÖKSU	2. Paket (12:40-15:15)	172.16.0.55	ogrenci
102	2026-04-06	14:38:59	25902012	FAHRİ ARDA KARATAŞ	2. Paket (12:40-15:15)	172.16.0.26	ogrenci
103	2026-04-06	14:38:59	25905012	ERKAM SONUÇ	2. Paket (12:40-15:15)	172.16.0.139	ogrenci
104	2026-04-06	14:39:12	25904006	İREM GENEŞ	2. Paket (12:40-15:15)	172.16.0.107	ogrenci
105	2026-04-06	14:39:25	25905011	KAMURAN İNAN AYDOĞAN	2. Paket (12:40-15:15)	172.16.0.114	ogrenci
106	2026-04-06	14:40:11	25901007	ARDA KARATAŞ	2. Paket (12:40-15:15)	172.16.0.41	ogrenci
107	2026-04-06	14:41:57	25902014	ZÜBEYİR CUMA YILMAZ	2. Paket (12:40-15:15)	172.16.0.104	ogrenci
108	2026-04-06	14:55:29	25905013	ATA ÇAĞAN KESKİN	2. Paket (12:40-15:15)	ogretmen	force
109	2026-04-06	15:04:38	123	TEST TEST	2. Paket (12:40-15:15)	127.0.0.1	ogrenci
110	2026-04-06	15:28:33	25904031	SELAHATTİN EFE SORGUN	3. Paket (15:25-18:00)	172.16.0.26	ogrenci
111	2026-04-06	15:35:34	25901012	NİSA NUR ÇELİK	3. Paket (15:25-18:00)	172.16.0.101	ogrenci
112	2026-04-06	15:36:39	25901016	MUZAFFER TAHA GÜL	3. Paket (15:25-18:00)	172.16.0.101	ogrenci
113	2026-04-06	15:36:43	25903005	IŞIL KORKMAZ	3. Paket (15:25-18:00)	172.16.0.118	ogrenci
114	2026-04-06	15:37:11	25905020	BERAT ALİ ERİŞ	3. Paket (15:25-18:00)	172.16.0.63	ogrenci
115	2026-04-06	16:49:51	25901012	NİSA NUR ÇELİK	3. Paket (15:25-18:00)	172.16.0.101	ogrenci
116	2026-04-12	20:41:22	123	TEST TEST	—	ogretmen	force
\.


--
-- Data for Name: ogrenciler; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ogrenciler (id, sinif_id, numara, ad, soyad, sifre) FROM stdin;
1	1	25901002	BEHİÇ ARDA	DEMİRER	
2	1	25901003	FURKAN SAFA	ÇÜRÜTTÜ	
3	1	25901004	ALPEREN	DURKUT	
4	1	25901005	SALİH BİLAL	KORKMAZ	
5	1	25901006	EREN	GÜLER	
6	1	25901007	ARDA	KARATAŞ	
7	1	25901008	EZGİ	YILDIZ	
8	1	25901010	KAZIM EFE	TAŞDEMİR	
9	1	25901011	EFEKAN	İÇÖZ	
10	1	25901012	NİSA NUR	ÇELİK	
11	1	25901013	BUSENUR	ALTAN	
12	1	25901016	MUZAFFER TAHA	GÜL	
13	1	25901017	ÖMER	YEŞİLYURT	
14	1	25901018	ZEHRA	YILDIRIM	
15	2	25902001	İLKAY	ŞIK	
16	2	25902002	ENES	ÖZTÜRK	
17	2	25902003	ARİF SEVBAN	KIRIT	
18	2	25902004	EYLÜL	KAYA	
19	2	25902007	MEHMET CAN	ERŞEN	
20	2	25902008	MUSTAFA	ÇETİN	
21	2	25902009	RESUL EKREM	ÖZCAN	
22	2	25902010	AHMET FARUK	YÜKSEL	
23	2	25902012	FAHRİ ARDA	KARATAŞ	
24	2	25902013	MUSTAFA	ŞAHİN	
25	2	25902014	ZÜBEYİR CUMA	YILMAZ	
26	2	25902017	TARIK BUĞRA	BODUR	
27	2	25902020	DOĞUKAN	DURAN	
28	2	25902021	ESRA	BAYRAM	
29	2	25902023	EFEHAN	KULU	
30	2	25902025	BURAK	AYYILDIZ	
31	3	25905001	AHMET	BAŞOĞLU	
32	3	25905002	TUANNA	ALTIN	
33	3	25905003	DİLEK	KARAÇE	
34	3	25905004	MUSTAFA	AVCI	
35	3	25905006	RECEP FURKAN	ÇELİK	
36	3	25905007	SEFA YUSUF	KÜTÜK	
37	3	25905008	FATMA RANA	GÖKDEMİR	
38	3	25905009	VEYSEL KAAN	DÜMAN	
39	3	25905011	KAMURAN İNAN	AYDOĞAN	
40	3	25905012	ERKAM	SONUÇ	
41	3	25905013	ATA ÇAĞAN	KESKİN	
42	3	25905014	MUZAFFER	KARSLIOĞLU	
43	3	25905015	YUNUS EGE	MÖNÜR	
44	3	25905016	BAHRİ	AYDOĞDU	
45	3	25905017	MEHMET ARDA	YENENER	
46	3	25905018	EREN	DUMRUL	
47	3	25905019	TUĞRA	TAŞ	
48	3	25905020	BERAT ALİ	ERİŞ	
49	3	25905024	RÜZGAR	KAYA	
50	3	25905027	İNCİ	HALICI	
51	3	25905028	YASİN	BOLAT	
52	4	25903001	AHMET	MAHLİ	
53	4	25903002	İREM	UYSAL	
54	4	25903003	BÜŞRA SENA	MUTLU	
55	4	25903004	MİRAY KAMİLE	TİRAŞ	
56	4	25903005	IŞIL	KORKMAZ	
57	4	25903006	ESMANUR	DİNÇER	
58	4	25903007	TUĞBA	GÜLMEZ	
59	4	25903008	HATİCE	ÖZLÜ	
60	4	25903009	CEMRE SU	GENÇ	
61	4	25903010	AZRA	ŞAHİN	
62	4	25903011	SEMİH	ÇELİKEL	
63	4	25903012	MUHAMMED HAKTAN	SAZÇALAN	
64	4	25903013	AHMET MERT	KÖYBAŞI	
65	4	25903014	RANA BEDRİYE	DAĞTEKİN	
66	4	25903015	SEVİM	ÇELİK	
67	5	25904001	ALAATTİN EFE	YURTERİ	
68	5	25904002	SALİH GÖKAY	KÖKSAL	
69	5	25904003	SÜHEYLA TUĞÇE	GÜN	
70	5	25904004	SÜLEYMAN ESER	DİNÇ	
71	5	25904005	SUDE ELMAS	AYKIRI	
72	5	25904006	İREM	GENEŞ	
73	5	25904007	ERTÜMEN	YAYLA	
74	5	25904008	ZEHRA	ÇALIK	
75	5	25904009	AYBÜKE	TERCAN	
76	5	25904010	EMİRHAN	ESENOĞLU	
77	5	25904011	FURKAN	İLİK	
78	5	25904012	MEHMET EREN	BODUROĞLU	
79	5	25904014	AHMET TAYLAN	ERDEN	
80	5	25904016	MEHMET ENES	KAYA	
81	5	25904017	SAFA	HASOĞLU	
82	5	25904018	YAVUZ SELİM	SEZER	
83	5	25904019	YUSUF ENES	BİLGİN	
84	5	25904020	ALMILA FATMA	ÖZER	
85	5	25904021	ÖMER	YILDIZ	
86	5	25904022	MEHMET KAYRA	AKKUŞ	
87	5	25904023	HASAN ARDA	TAHTACI	
88	5	25904024	SUDE	ÖZTÜRK	
89	5	25904025	ÖYKÜM NİLDENİZ	AKPINAR	
90	5	25904026	ONUR	YENİPAZARLI	
91	5	25904027	YUSUF	ŞAHBAZ	
92	5	25904028	BÜNYAMİN EFE	BULUT	
93	5	25904029	EFZA	KAÇMAZ	
94	5	25904030	AYŞE	DEMİRKAYA	
95	5	25904031	SELAHATTİN EFE	SORGUN	
96	5	25904032	AGAH ABDULLAH	SARSILMAZ	
97	5	25904033	SAHRA	GÜNDOĞDU	
98	5	25904034	ÖZGÜR	YILDIZ	
99	5	25904035	GÖKTUĞ ERDEM	PEHLİVAN	
100	5	25904036	ZEREN	NEBİOĞLU	
101	5	25904037	MUHAMMED EFENDİ	AYHANOĞLU	
102	5	25904038	YUNUS EMRE	KARAKEÇİLİ	
103	5	25904039	ÖMER FARUK	GÖKSU	
104	5	25904040	ENES	İNCE	
105	5	25904041	İSMET HALİT	DEMİRCİ	
106	5	25904043	HASAN BERK	KOCA	
109	6	123	TEST	TEST	123
110	1	24090901	AMINJON	PRIMOV	24090901
111	3	24118904	ABDELRAHMAN	KHALIL	24118904
112	2	25902024	EFEHAN	EKINCI	25902024
113	1	24090003	EFE BARAN	DEMIRHAN	24090003
114	3	25905022	ISMAIL KAAN	YÜKSEKER	25905022
115	5	25904401	SALIH	DEMIRTAŞ	25904401
116	1	25146901	SAMI	KARACA	25146901
117	7	test1	Öğrenci-1	TEST	1234
118	7	test2	Öğrenci-2	TEST	1234
119	7	test3	Öğrenci-3	TEST	1234
120	7	test4	Öğrenci-4	TEST	1234
121	7	test5	Öğrenci-5	TEST	1234
167	7	001	A	B	001
\.


--
-- Data for Name: ogrenme_ciktilari; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ogrenme_ciktilari (id, sinav_id, numara, metin) FROM stdin;
1	1	1	Dosya yönetim komutlarını bilir ve uygular
2	1	2	Arşivleme araçlarını bilir
3	3	1	Dosya yönetim komutlarını bilir ve uygular
4	3	2	Dizin oluşturma ve yönetmeyi bilir
5	3	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
6	4	1	Dosya yönetim komutlarını bilir ve uygular
7	4	2	Dizin oluşturma ve yönetmeyi bilir
8	4	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
9	5	1	Dosya yönetim komutlarını bilir ve uygular
10	5	2	Dizin oluşturma ve yönetmeyi bilir
11	5	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
12	6	1	Dosya yönetim komutlarını bilir ve uygular
13	6	2	Dizin oluşturma ve yönetmeyi bilir
14	6	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
15	7	1	Dosya yönetim komutlarını bilir ve uygular
16	7	2	Dizin oluşturma ve yönetmeyi bilir
17	7	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
18	8	1	Dosya yönetim komutlarını bilir ve uygular
19	8	2	Dizin oluşturma ve yönetmeyi bilir
20	8	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
21	9	1	Dosya yönetim komutlarını bilir ve uygular
22	9	2	Dizin oluşturma ve yönetmeyi bilir
23	9	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
24	10	1	Dosya yönetim komutlarını bilir ve uygular
25	10	2	Dizin oluşturma ve yönetmeyi bilir
26	10	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
27	11	1	dosya asdasdşlkşlaksdf
28	11	2	asdasşdlkşkşkasdasf
29	12	1	Dosya yönetim komutlarını bilir ve uygular
30	12	2	Dizin oluşturma ve yönetmeyi bilir
31	12	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
32	13	1	Dosya yönetim komutlarını bilir ve uygular
33	13	2	Dizin oluşturma ve yönetmeyi bilir
34	13	3	Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular
\.


--
-- Data for Name: sahte_giris_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sahte_giris_log (id, tarih, saat, ip, gercek_numara, gercek_ad, denenen_numara, denenen_ad, sinif) FROM stdin;
8	2026-03-02	10:54:39	172.16.0.120	25905017	Aynı IP	25905024	RÜZGAR KAYA	Yazılım Geliştirme
9	2026-03-02	10:55:38	172.16.0.120	25905017	Aynı IP	25905024	RÜZGAR KAYA	Yazılım Geliştirme
10	2026-03-02	12:53:39	172.16.0.112	25905015	Aynı IP	25904027	YUSUF ŞAHBAZ	Yapay Zeka ve Makine Öğrenmesi
11	2026-03-02	12:53:55	172.16.0.120	25905017	Aynı IP	25904021	ÖMER YILDIZ	Yapay Zeka ve Makine Öğrenmesi
12	2026-03-02	12:54:01	172.16.0.112	25905015	Aynı IP	25904027	YUSUF ŞAHBAZ	Yapay Zeka ve Makine Öğrenmesi
13	2026-03-02	12:54:41	172.16.0.120	25905017	Aynı IP	25904021	ÖMER YILDIZ	Yapay Zeka ve Makine Öğrenmesi
14	2026-03-02	12:55:31	172.16.0.112	25905015	Aynı IP	25904027	YUSUF ŞAHBAZ	Yapay Zeka ve Makine Öğrenmesi
15	2026-03-02	12:57:06	172.16.0.120	25905017	Aynı IP	25904021	ÖMER YILDIZ	Yapay Zeka ve Makine Öğrenmesi
16	2026-03-02	12:57:09	172.16.0.120	25905017	Aynı IP	25904021	ÖMER YILDIZ	Yapay Zeka ve Makine Öğrenmesi
17	2026-03-02	12:57:19	172.16.0.120	25905017	Aynı IP	25904021	ÖMER YILDIZ	Yapay Zeka ve Makine Öğrenmesi
18	2026-03-02	12:58:41	172.16.0.112	25905015	Aynı IP	25904027	YUSUF ŞAHBAZ	Yapay Zeka ve Makine Öğrenmesi
19	2026-03-02	12:58:53	172.16.0.112	25905015	Aynı IP	25904027	YUSUF ŞAHBAZ	Yapay Zeka ve Makine Öğrenmesi
20	2026-03-02	13:01:33	172.16.0.120	25905017	Aynı IP	25904021	ÖMER YILDIZ	Yapay Zeka ve Makine Öğrenmesi
21	2026-03-02	13:03:10	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
22	2026-03-02	13:03:33	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
23	2026-03-02	13:03:45	172.16.0.120	25905017	Aynı IP	25904021	ÖMER YILDIZ	Yapay Zeka ve Makine Öğrenmesi
24	2026-03-02	13:04:49	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
25	2026-03-02	13:05:00	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
26	2026-03-02	13:05:03	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
27	2026-03-02	13:05:18	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
28	2026-03-02	13:06:14	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
29	2026-03-02	13:06:44	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
30	2026-03-02	13:07:27	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
31	2026-03-02	13:08:55	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
32	2026-03-02	13:12:49	172.16.0.118	25901013	Aynı IP	25904030	AYŞE DEMİRKAYA	Yapay Zeka ve Makine Öğrenmesi
33	2026-03-03	13:51:59	127.0.0.1	123	Aynı IP	124	TEST2 TEST2	TEST
34	2026-03-09	11:56:16	172.16.0.14	124	Aynı IP	123	TEST TEST	TEST
35	2026-03-09	12:20:00	172.16.0.14	124	Aynı IP	123	TEST TEST	TEST
\.


--
-- Data for Name: seb_cikis_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seb_cikis_log (id, tarih, saat, numara, ad_soyad, ip) FROM stdin;
1	2026-03-09	10:54:29	25901011	EFEKAN İÇÖZ	172.16.0.26
2	2026-03-09	10:55:19	25903015	SEVİM ÇELİK	172.16.0.38
3	2026-03-09	10:55:26	25903006	ESMANUR DİNÇER	172.16.0.107
4	2026-03-09	11:25:44	25905020	BERAT ALİ ERİŞ	172.16.0.118
5	2026-03-09	11:27:24	25905028	YASİN BOLAT	172.16.0.9
6	2026-03-09	11:30:18	25902023	EFEHAN KULU	172.16.0.100
7	2026-03-09	11:30:21	25904029	EFZA KAÇMAZ	172.16.0.125
8	2026-03-09	11:30:22	25904032	AGAH ABDULLAH SARSILMAZ	172.16.0.13
9	2026-03-09	11:30:22	25901002	BEHİÇ ARDA DEMİRER	172.16.0.29
10	2026-03-09	11:30:30	25901010	KAZIM EFE TAŞDEMİR	172.16.0.126
11	2026-03-09	11:30:34	25901004	ALPEREN DURKUT	172.16.0.139
12	2026-03-09	11:30:35	25901016	MUZAFFER TAHA GÜL	172.16.0.25
13	2026-03-09	11:30:36	25904005	SUDE ELMAS AYKIRI	172.16.0.177
14	2026-03-09	11:30:36	25901011	EFEKAN İÇÖZ	172.16.0.26
15	2026-03-09	11:30:38	25905001	AHMET BAŞOĞLU	172.16.0.19
16	2026-03-09	11:30:38	25902003	ARİF SEVBAN KIRIT	172.16.0.43
17	2026-03-09	11:30:38	25905009	VEYSEL KAAN DÜMAN	172.16.0.36
18	2026-03-09	11:30:42	25905013	ATA ÇAĞAN KESKİN	172.16.0.72
19	2026-03-09	11:30:42	25905008	FATMA RANA GÖKDEMİR	172.16.0.179
20	2026-03-09	11:30:47	25905002	TUANNA ALTIN	172.16.0.182
21	2026-03-09	11:30:47	25901007	ARDA KARATAŞ	172.16.0.114
22	2026-03-09	11:31:00	25901003	FURKAN SAFA ÇÜRÜTTÜ	172.16.0.20
23	2026-03-09	12:22:47	25905018	EREN DUMRUL	172.16.0.39
24	2026-03-09	12:42:58	25902007	MEHMET CAN ERŞEN	172.16.0.101
25	2026-03-09	12:42:58	25902007	MEHMET CAN ERŞEN	172.16.0.101
26	2026-03-09	12:42:59	25902007	MEHMET CAN ERŞEN	172.16.0.101
27	2026-03-09	12:42:59	25902007	MEHMET CAN ERŞEN	172.16.0.101
28	2026-03-09	12:42:59	25902007	MEHMET CAN ERŞEN	172.16.0.101
29	2026-03-09	12:43:00	25902007	MEHMET CAN ERŞEN	172.16.0.101
30	2026-03-09	12:43:00	25902007	MEHMET CAN ERŞEN	172.16.0.101
31	2026-03-09	12:43:00	25902007	MEHMET CAN ERŞEN	172.16.0.101
32	2026-03-09	12:43:00	25902007	MEHMET CAN ERŞEN	172.16.0.101
33	2026-03-09	12:43:00	25902007	MEHMET CAN ERŞEN	172.16.0.101
34	2026-03-09	12:43:00	25902007	MEHMET CAN ERŞEN	172.16.0.101
35	2026-03-09	12:43:00	25902007	MEHMET CAN ERŞEN	172.16.0.101
36	2026-03-09	12:43:03	25902007	MEHMET CAN ERŞEN	172.16.0.101
37	2026-03-09	12:43:23	25902007	MEHMET CAN ERŞEN	172.16.0.101
38	2026-03-09	12:43:27	25902007	MEHMET CAN ERŞEN	172.16.0.101
39	2026-03-09	12:43:51	25902007	MEHMET CAN ERŞEN	172.16.0.101
40	2026-03-09	12:43:51	25902007	MEHMET CAN ERŞEN	172.16.0.101
41	2026-03-09	12:43:51	25902007	MEHMET CAN ERŞEN	172.16.0.101
42	2026-03-09	12:43:51	25902007	MEHMET CAN ERŞEN	172.16.0.101
43	2026-03-09	12:43:51	25902007	MEHMET CAN ERŞEN	172.16.0.101
44	2026-03-09	12:43:52	25902007	MEHMET CAN ERŞEN	172.16.0.101
45	2026-03-09	12:43:52	25902007	MEHMET CAN ERŞEN	172.16.0.101
46	2026-03-09	12:43:52	25902007	MEHMET CAN ERŞEN	172.16.0.101
47	2026-03-09	12:43:52	25902007	MEHMET CAN ERŞEN	172.16.0.101
48	2026-03-09	12:43:52	25902007	MEHMET CAN ERŞEN	172.16.0.101
49	2026-03-09	12:43:52	25902007	MEHMET CAN ERŞEN	172.16.0.101
50	2026-03-09	12:43:53	25902007	MEHMET CAN ERŞEN	172.16.0.101
51	2026-03-09	12:43:53	25902007	MEHMET CAN ERŞEN	172.16.0.101
52	2026-03-09	12:43:53	25902007	MEHMET CAN ERŞEN	172.16.0.101
53	2026-03-09	14:11:14	25902010	AHMET FARUK YÜKSEL	172.16.0.9
54	2026-03-09	14:22:54	25902010	AHMET FARUK YÜKSEL	172.16.0.9
55	2026-03-09	14:25:30	25903011	SEMİH ÇELİKEL	172.16.0.61
56	2026-03-09	14:25:30	25902017	TARIK BUĞRA BODUR	172.16.0.126
57	2026-03-09	14:25:31	25902010	AHMET FARUK YÜKSEL	172.16.0.9
58	2026-03-09	14:25:31	25901008	EZGİ YILDIZ	172.16.0.25
59	2026-03-09	14:25:31	25904018	YAVUZ SELİM SEZER	172.16.0.113
60	2026-03-09	14:25:31	25904018	YAVUZ SELİM SEZER	172.16.0.113
61	2026-03-09	14:25:31	25903001	AHMET MAHLİ	172.16.0.177
62	2026-03-09	14:25:34	25903013	AHMET MERT KÖYBAŞI	172.16.0.121
63	2026-03-09	14:25:35	25903011	SEMİH ÇELİKEL	172.16.0.61
64	2026-03-09	14:25:36	25905012	ERKAM SONUÇ	172.16.0.20
65	2026-03-09	14:25:37	25901008	EZGİ YILDIZ	172.16.0.25
66	2026-03-09	14:25:37	25903011	SEMİH ÇELİKEL	172.16.0.61
67	2026-03-09	14:25:38	25903011	SEMİH ÇELİKEL	172.16.0.61
68	2026-03-09	14:25:38	25903011	SEMİH ÇELİKEL	172.16.0.61
69	2026-03-09	14:25:38	25903011	SEMİH ÇELİKEL	172.16.0.61
70	2026-03-09	14:25:38	25903011	SEMİH ÇELİKEL	172.16.0.61
71	2026-03-09	14:25:38	25903011	SEMİH ÇELİKEL	172.16.0.61
72	2026-03-09	14:25:39	25904018	YAVUZ SELİM SEZER	172.16.0.113
73	2026-03-09	14:25:47	25901013	BUSENUR ALTAN	172.16.0.100
74	2026-03-09	14:39:21	25904018	YAVUZ SELİM SEZER	172.16.0.113
75	2026-03-09	14:54:03	25904018	YAVUZ SELİM SEZER	172.16.0.113
76	2026-03-09	14:54:04	25903003	BÜŞRA SENA MUTLU	172.16.0.107
77	2026-03-09	14:54:07	25903013	AHMET MERT KÖYBAŞI	172.16.0.121
78	2026-03-09	14:54:10	25904012	MEHMET EREN BODUROĞLU	172.16.0.118
79	2026-03-09	14:54:15	25903004	MİRAY KAMİLE TİRAŞ	172.16.0.29
80	2026-03-09	14:54:17	25903011	SEMİH ÇELİKEL	172.16.0.61
81	2026-03-09	14:54:19	25903009	CEMRE SU GENÇ	172.16.0.47
82	2026-03-09	14:54:19	25904027	YUSUF ŞAHBAZ	172.16.0.182
83	2026-03-09	14:54:33	25902012	FAHRİ ARDA KARATAŞ	172.16.0.43
84	2026-03-09	14:54:38	25905011	KAMURAN İNAN AYDOĞAN	172.16.0.101
85	2026-03-09	14:54:41	25901008	EZGİ YILDIZ	172.16.0.25
86	2026-03-09	14:54:41	25903001	AHMET MAHLİ	172.16.0.177
87	2026-03-09	14:54:42	25904019	YUSUF ENES BİLGİN	172.16.0.108
88	2026-03-09	14:54:43	25903010	AZRA ŞAHİN	172.16.0.125
89	2026-03-09	14:54:45	25901013	BUSENUR ALTAN	172.16.0.100
90	2026-03-09	14:54:45	25904030	AYŞE DEMİRKAYA	172.16.0.178
91	2026-03-09	14:54:49	25902009	RESUL EKREM ÖZCAN	172.16.0.72
92	2026-03-09	14:54:51	25902002	ENES ÖZTÜRK	172.16.0.178
93	2026-03-09	14:54:57	25905012	ERKAM SONUÇ	172.16.0.20
94	2026-03-09	16:11:35	25904043	HASAN BERK KOCA	172.16.0.139
95	2026-03-09	16:45:41	25904010	EMİRHAN ESENOĞLU	172.16.0.114
96	2026-03-09	16:45:42	25901018	ZEHRA YILDIRIM	172.16.0.125
97	2026-03-09	16:45:42	25904016	MEHMET ENES KAYA	172.16.0.120
98	2026-03-09	16:45:43	25904037	MUHAMMED EFENDİ AYHANOĞLU	172.16.0.20
99	2026-03-09	16:45:43	25904037	MUHAMMED EFENDİ AYHANOĞLU	172.16.0.20
100	2026-03-09	16:45:50	25902025	BURAK AYYILDIZ	172.16.0.118
101	2026-03-09	16:45:50	25905017	MEHMET ARDA YENENER	172.16.0.47
102	2026-03-09	16:45:54	25904004	SÜLEYMAN ESER DİNÇ	172.16.0.101
103	2026-03-09	16:45:55	25903002	İREM UYSAL	172.16.0.178
104	2026-03-09	16:45:58	25904007	ERTÜMEN YAYLA	172.16.0.43
105	2026-03-09	16:46:04	25904022	MEHMET KAYRA AKKUŞ	172.16.0.39
106	2026-03-09	16:46:08	25901012	NİSA NUR ÇELİK	172.16.0.38
107	2026-03-09	16:46:08	25902021	ESRA BAYRAM	172.16.0.107
108	2026-03-09	16:46:19	25902021	ESRA BAYRAM	172.16.0.107
109	2026-03-29	23:57:04	123	TEST TEST	127.0.0.1
110	2026-03-29	23:57:26	123	TEST TEST	127.0.0.1
111	2026-03-30	09:18:45	24090003	EFE BARAN DEMIRHAN	172.16.0.14
112	2026-03-30	09:19:04	24090003	EFE BARAN DEMIRHAN	172.16.0.14
113	2026-03-30	11:04:30	25901011	EFEKAN İÇÖZ	172.16.0.26
114	2026-03-30	11:04:30	25901011	EFEKAN İÇÖZ	172.16.0.26
115	2026-03-30	11:14:41	25904002	SALİH GÖKAY KÖKSAL	172.16.0.66
116	2026-03-30	11:16:29	25901003	FURKAN SAFA ÇÜRÜTTÜ	172.16.0.23
117	2026-03-30	11:18:34	25902007	MEHMET CAN ERŞEN	172.16.0.4
118	2026-03-30	11:18:41	25904041	İSMET HALİT DEMİRCİ	172.16.0.108
119	2026-03-30	11:18:44	25901006	EREN GÜLER	172.16.0.61
120	2026-03-30	11:18:53	25901004	ALPEREN DURKUT	172.16.0.139
121	2026-03-30	11:18:58	25904033	SAHRA GÜNDOĞDU	172.16.0.125
122	2026-03-30	11:18:58	25904033	SAHRA GÜNDOĞDU	172.16.0.125
123	2026-03-30	13:11:25	25905002	TUANNA ALTIN	172.16.0.125
124	2026-03-30	13:21:19	25901013	BUSENUR ALTAN	172.16.0.126
125	2026-03-30	14:44:26	25903002	İREM UYSAL	172.16.0.61
126	2026-03-30	14:55:21	25904021	ÖMER YILDIZ	172.16.0.104
127	2026-03-30	14:55:21	25904021	ÖMER YILDIZ	172.16.0.104
128	2026-03-30	14:55:24	25904006	İREM GENEŞ	172.16.0.113
129	2026-03-30	14:55:24	25904006	İREM GENEŞ	172.16.0.113
130	2026-03-30	14:55:30	25904012	MEHMET EREN BODUROĞLU	172.16.0.72
131	2026-03-30	14:55:31	25904018	YAVUZ SELİM SEZER	172.16.0.100
132	2026-03-30	14:55:59	25903001	AHMET MAHLİ	172.16.0.47
133	2026-03-30	15:20:33	25902010	AHMET FARUK YÜKSEL	172.16.0.100
134	2026-03-30	15:53:51	25904043	HASAN BERK KOCA	172.16.0.84
135	2026-03-30	15:53:56	25904043	HASAN BERK KOCA	172.16.0.84
136	2026-03-30	15:54:04	25904043	HASAN BERK KOCA	172.16.0.84
137	2026-03-30	15:58:25	25902020	DOĞUKAN DURAN	172.16.0.121
138	2026-03-30	15:58:25	25902020	DOĞUKAN DURAN	172.16.0.121
139	2026-03-30	16:00:17	25905028	YASİN BOLAT	172.16.0.14
140	2026-03-30	16:00:17	25905028	YASİN BOLAT	172.16.0.14
141	2026-03-30	16:02:04	25904037	MUHAMMED EFENDİ AYHANOĞLU	172.16.0.72
142	2026-03-30	16:02:05	25904037	MUHAMMED EFENDİ AYHANOĞLU	172.16.0.72
143	2026-03-30	16:02:06	25904037	MUHAMMED EFENDİ AYHANOĞLU	172.16.0.72
144	2026-03-30	16:03:00	25904022	MEHMET KAYRA AKKUŞ	172.16.0.113
145	2026-03-30	16:06:13	25901018	ZEHRA YILDIRIM	172.16.0.41
146	2026-03-30	16:06:13	25901018	ZEHRA YILDIRIM	172.16.0.41
147	2026-03-30	16:11:01	25904037	MUHAMMED EFENDİ AYHANOĞLU	172.16.0.72
148	2026-03-30	16:20:39	25146901	SAMI KARACA	172.16.0.139
149	2026-03-30	16:32:48	25146901	SAMI KARACA	172.16.0.139
150	2026-03-30	17:10:49	25904007	ERTÜMEN YAYLA	172.16.0.104
151	2026-03-30	17:10:49	25904007	ERTÜMEN YAYLA	172.16.0.104
152	2026-03-30	17:10:57	25904004	SÜLEYMAN ESER DİNÇ	172.16.0.118
153	2026-03-30	17:10:59	25904004	SÜLEYMAN ESER DİNÇ	172.16.0.118
154	2026-03-30	17:10:59	25904004	SÜLEYMAN ESER DİNÇ	172.16.0.118
155	2026-03-30	17:11:00	25904004	SÜLEYMAN ESER DİNÇ	172.16.0.118
156	2026-03-30	17:49:35	25902023	EFEHAN KULU	172.16.0.4
157	2026-03-30	17:49:35	25902023	EFEHAN KULU	172.16.0.4
158	2026-04-01	16:11:28	123	TEST TEST	127.0.0.1
159	2026-04-02	14:24:40	123	TEST TEST	127.0.0.1
160	2026-04-02	21:41:59	test4	Öğrenci-4 TEST	192.168.111.53
161	2026-04-02	21:44:08	test4	Öğrenci-4 TEST	192.168.111.53
162	2026-04-02	22:39:22	001	A B	192.168.111.53
163	2026-04-02	23:12:40	test1	Öğrenci-1 TEST	192.168.111.53
164	2026-04-06	12:49:49	25904002	SALİH GÖKAY KÖKSAL	172.16.0.113
165	2026-04-06	12:50:38	25904002	SALİH GÖKAY KÖKSAL	172.16.0.113
166	2026-04-06	12:52:00	25904027	YUSUF ŞAHBAZ	172.16.0.56
167	2026-04-06	12:52:01	25904027	YUSUF ŞAHBAZ	172.16.0.56
168	2026-04-06	13:54:43	25904003	SÜHEYLA TUĞÇE GÜN	172.16.0.18
169	2026-04-06	13:54:45	25904003	SÜHEYLA TUĞÇE GÜN	172.16.0.18
170	2026-04-06	13:56:48	25904020	ALMILA FATMA ÖZER	172.16.0.84
171	2026-04-06	14:18:27	25903007	TUĞBA GÜLMEZ	172.16.0.75
172	2026-04-06	14:20:05	25901006	EREN GÜLER	172.16.0.121
173	2026-04-06	14:20:15	25901010	KAZIM EFE TAŞDEMİR	172.16.0.61
174	2026-04-06	14:20:16	25901010	KAZIM EFE TAŞDEMİR	172.16.0.61
175	2026-04-06	14:28:50	25901006	EREN GÜLER	172.16.0.121
176	2026-04-06	14:28:55	25901010	KAZIM EFE TAŞDEMİR	172.16.0.61
177	2026-04-06	14:28:55	25901010	KAZIM EFE TAŞDEMİR	172.16.0.61
178	2026-04-06	14:29:06	25901010	KAZIM EFE TAŞDEMİR	172.16.0.61
179	2026-04-06	14:29:31	25901010	KAZIM EFE TAŞDEMİR	172.16.0.61
180	2026-04-06	14:38:54	25903010	AZRA ŞAHİN	172.16.0.108
181	2026-04-06	14:38:54	25905009	VEYSEL KAAN DÜMAN	172.16.0.85
182	2026-04-06	14:38:56	25901006	EREN GÜLER	172.16.0.121
183	2026-04-06	14:38:57	25902010	AHMET FARUK YÜKSEL	172.16.0.78
184	2026-04-06	14:39:00	25904036	ZEREN NEBİOĞLU	172.16.0.11
185	2026-04-06	14:39:00	25905015	YUNUS EGE MÖNÜR	172.16.0.100
186	2026-04-06	14:39:01	25904012	MEHMET EREN BODUROĞLU	172.16.0.100
187	2026-04-06	14:39:04	25904021	ÖMER YILDIZ	172.16.0.63
188	2026-04-06	14:39:04	25904021	ÖMER YILDIZ	172.16.0.63
189	2026-04-06	14:39:04	25904020	ALMILA FATMA ÖZER	172.16.0.84
190	2026-04-06	14:39:05	25904030	AYŞE DEMİRKAYA	172.16.0.84
191	2026-04-06	14:39:05	25903004	MİRAY KAMİLE TİRAŞ	172.16.0.73
192	2026-04-06	14:39:06	25904024	SUDE ÖZTÜRK	172.16.0.101
193	2026-04-06	15:37:42	25905024	RÜZGAR KAYA	172.16.0.63
194	2026-04-06	15:37:42	25905024	RÜZGAR KAYA	172.16.0.63
195	2026-04-06	16:40:48	25904043	HASAN BERK KOCA	172.16.0.14
196	2026-04-06	16:47:48	25904043	HASAN BERK KOCA	172.16.0.14
197	2026-04-06	16:47:50	25904043	HASAN BERK KOCA	172.16.0.14
198	2026-04-06	16:50:26	25905020	BERAT ALİ ERİŞ	172.16.0.54
199	2026-04-12	20:11:24	123	TEST TEST	167.82.4.223
200	2026-04-12	20:41:04	123	TEST TEST	167.82.4.223
201	2026-04-12	20:41:04	123	TEST TEST	167.82.4.223
202	2026-04-12	20:42:51	123	TEST TEST	167.82.4.223
\.


--
-- Data for Name: seb_cikis_talepleri; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seb_cikis_talepleri (id, tarih, saat, numara, ad_soyad, durum) FROM stdin;
1	2026-03-09	10:21:20	25904029	EFZA KAÇMAZ	onaylandi
2	2026-03-09	10:55:16	25903006	ESMANUR DİNÇER	onaylandi
3	2026-03-09	10:55:17	25903015	SEVİM ÇELİK	onaylandi
4	2026-03-09	11:09:25	25905009	VEYSEL KAAN DÜMAN	onaylandi
5	2026-03-09	11:14:28	25902002	ENES ÖZTÜRK	onaylandi
6	2026-03-09	11:20:55	25902023	EFEHAN KULU	onaylandi
7	2026-03-09	11:25:37	25905020	BERAT ALİ ERİŞ	onaylandi
8	2026-03-09	11:27:25	25904005	SUDE ELMAS AYKIRI	onaylandi
9	2026-03-09	11:30:20	25901002	BEHİÇ ARDA DEMİRER	onaylandi
10	2026-03-09	11:30:39	25905013	ATA ÇAĞAN KESKİN	onaylandi
11	2026-03-09	11:30:45	25905002	TUANNA ALTIN	onaylandi
12	2026-03-09	11:30:46	25901007	ARDA KARATAŞ	onaylandi
13	2026-03-09	12:42:52	25902007	MEHMET CAN ERŞEN	onaylandi
14	2026-03-09	14:18:13	25903003	BÜŞRA SENA MUTLU	onaylandi
15	2026-03-09	14:22:41	123	TEST TEST	onaylandi
16	2026-03-09	14:22:53	25902017	TARIK BUĞRA BODUR	onaylandi
17	2026-03-09	14:53:59	25904018	YAVUZ SELİM SEZER	onaylandi
18	2026-03-09	14:54:38	25904030	AYŞE DEMİRKAYA	onaylandi
19	2026-03-09	14:54:40	25901008	EZGİ YILDIZ	onaylandi
20	2026-03-09	14:54:54	25905012	ERKAM SONUÇ	onaylandi
21	2026-03-09	15:29:22	25904036	ZEREN NEBİOĞLU	onaylandi
22	2026-03-09	15:32:15	25904020	ALMILA FATMA ÖZER	onaylandi
23	2026-03-09	16:44:19	25905017	MEHMET ARDA YENENER	bekliyor
24	2026-03-09	16:44:41	25904037	MUHAMMED EFENDİ AYHANOĞLU	bekliyor
25	2026-03-09	16:45:38	25904010	EMİRHAN ESENOĞLU	bekliyor
26	2026-03-09	16:45:39	25901018	ZEHRA YILDIRIM	bekliyor
27	2026-03-09	16:45:41	25904016	MEHMET ENES KAYA	bekliyor
28	2026-03-09	16:45:49	25902020	DOĞUKAN DURAN	bekliyor
29	2026-03-09	16:45:53	25904004	SÜLEYMAN ESER DİNÇ	bekliyor
30	2026-03-09	16:45:54	25903002	İREM UYSAL	bekliyor
31	2026-03-09	16:45:56	25904007	ERTÜMEN YAYLA	bekliyor
\.


--
-- Data for Name: secenekler; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.secenekler (id, soru_id, metin, dogru_mu) FROM stdin;
1	1	a	1
2	1	s	0
3	1	d	0
4	1	f	0
5	2	Dosya kopyalar	1
6	2	Dosya siler	0
7	2	Dosya taşır	0
8	3	Doğru	1
9	3	Yanlış	0
10	4	rm	1
11	6	Dosya kopyalar	1
12	6	Dosya siler	0
13	6	Dosya taşır	0
14	6	Klasör listeler	0
15	7	mkdir	1
16	7	touch	0
17	7	rmdir	0
18	7	ls	0
19	8	Doğru	1
20	8	Yanlış	0
21	9	rm	1
22	11	Dosya kopyalar	1
23	11	Dosya siler	0
24	11	Dosya taşır	0
25	11	Klasör listeler	0
26	12	mkdir	1
27	12	touch	0
28	12	rmdir	0
29	12	ls	0
30	13	Doğru	1
31	13	Yanlış	0
32	14	rm	1
33	16	Dosya kopyalar	1
34	16	Dosya siler	0
35	16	Dosya taşır	0
36	16	Klasör listeler	0
37	17	mkdir	1
38	17	touch	0
39	17	rmdir	0
40	17	ls	0
41	18	Doğru	1
42	18	Yanlış	0
43	19	rm	1
44	21	Dosya kopyalar	1
45	21	Dosya siler	0
46	21	Dosya taşır	0
47	21	Klasör listeler	0
48	22	mkdir	1
49	22	touch	0
50	22	rmdir	0
51	22	ls	0
52	23	Doğru	1
53	23	Yanlış	0
54	24	rm	1
55	26	Dosya kopyalar	1
56	26	Dosya siler	0
57	26	Dosya taşır	0
58	26	Klasör listeler	0
59	27	mkdir	1
60	27	touch	0
61	27	rmdir	0
62	27	ls	0
63	28	Doğru	1
64	28	Yanlış	0
65	29	rm	1
66	31	Dosya kopyalar	1
67	31	Dosya siler	0
68	31	Dosya taşır	0
69	31	Klasör listeler	0
70	32	mkdir	1
71	32	touch	0
72	32	rmdir	0
73	32	ls	0
74	33	Doğru	1
75	33	Yanlış	0
76	34	rm	1
77	36	Dosya kopyalar	1
78	36	Dosya siler	0
79	36	Dosya taşır	0
80	36	Klasör listeler	0
81	37	mkdir	1
82	37	touch	0
83	37	rmdir	0
84	37	ls	0
85	38	Doğru	1
86	38	Yanlış	0
87	39	rm	1
88	41	Dosya kopyalar	1
89	41	Dosya siler	0
90	41	Dosya taşır	0
91	41	Klasör listeler	0
92	42	mkdir	1
93	42	touch	0
94	42	rmdir	0
95	42	ls	0
96	43	Doğru	1
97	43	Yanlış	0
98	44	rm	1
99	46	asd	1
100	46	asdasd	0
101	46	asdasdsd	0
102	46	asdasdvvb	0
103	47	Dosya kopyalar	1
104	47	Dosya siler	0
105	47	Dosya taşır	0
106	47	Klasör listeler	0
107	48	mkdir	1
108	48	touch	0
109	48	rmdir	0
110	48	ls	0
111	49	Doğru	1
112	49	Yanlış	0
113	50	rm	1
114	52	Dosya kopyalar	1
115	52	Dosya siler	0
116	52	Dosya taşır	0
117	52	Klasör listeler	0
118	53	mkdir	1
119	53	touch	0
120	53	rmdir	0
121	53	ls	0
122	54	Doğru	1
123	54	Yanlış	0
124	55	rm	1
125	57	A	1
126	57	B	0
\.


--
-- Data for Name: sinav_ihlaller; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sinav_ihlaller (id, sinav_id, ogrenci_numara, sebep, aciklama, zaman, durum) FROM stdin;
1	1	25901013	fullscreen_exit	Yanlışlıkla ESC bastım	2026-04-02 08:41:35	onaylandi
2	1	25901013	fullscreen_exit	İkinci kez çıktım	2026-04-02 08:41:50	reddedildi
3	9	test4	fullscreen_exit		2026-04-02 18:36:51	onaylandi
4	11	test4	fullscreen_exit		2026-04-02 18:43:07	reddedildi
5	11	test4	fullscreen_exit		2026-04-02 18:46:01	reddedildi
\.


--
-- Data for Name: sinavlar; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sinavlar (id, baslik, aktif, olusturma_tarihi) FROM stdin;
1	ünite1-Quiz	0	2026-03-06
2	Test Sınavı 1	0	2026-04-02
3	İşletim Sistemleri Quiz	0	2026-04-02
4	İşletim Sistemleri Quiz	0	2026-04-02
5	İşletim Sistemleri Quiz	0	2026-04-02
6	İşletim Sistemleri Quiz	0	2026-04-02
7	İşletim Sistemleri Quiz	0	2026-04-02
8	İşletim Sistemleri Quiz	0	2026-04-02
9	İşletim Sistemleri Quiz	0	2026-04-02
10	İşletim Sistemleri Quiz	0	2026-04-02
11	quiz 22	0	2026-04-02
12	İşletim Sistemleri Quiz	1	2026-04-02
13	İşletim Sistemleri Quiz	0	2026-04-02
14	Test	0	2026-04-02
\.


--
-- Data for Name: siniflar; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.siniflar (id, ad) FROM stdin;
1	Bilgi Güvenliği Teknolojisi
2	Bilişim Sistemleri ve Teknolojileri
3	Yazılım Geliştirme
4	Veri Bilimi ve Analitiği
5	Yapay Zeka ve Makine Öğrenmesi
6	TEST
7	Test Sınıfı (5 Kişi)
\.


--
-- Data for Name: soru_cikti_iliskisi; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.soru_cikti_iliskisi (id, soru_id, cikti_id) FROM stdin;
1	2	1
2	3	2
3	4	1
4	4	2
5	5	1
6	6	3
7	7	4
8	8	5
9	9	3
10	9	4
11	10	3
12	11	6
13	12	7
14	13	8
15	14	6
16	14	7
17	15	6
18	16	9
19	17	10
20	18	11
21	19	9
22	19	10
23	20	9
24	21	12
25	22	13
26	23	14
27	24	12
28	24	13
29	25	12
30	26	15
31	27	16
32	28	17
33	29	15
34	29	16
35	30	15
36	31	18
37	32	19
38	33	20
39	34	18
40	34	19
41	35	18
42	36	21
43	37	22
44	38	23
45	39	21
46	39	22
47	40	21
48	41	24
49	42	25
50	43	26
51	44	24
52	44	25
53	45	24
54	47	29
55	48	30
56	49	31
57	50	29
58	50	30
59	51	29
60	52	32
61	53	33
62	54	34
63	55	32
64	55	33
65	56	32
\.


--
-- Data for Name: sorular; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sorular (id, sinav_id, metin, tip, puan, bloom_seviyesi, zorluk) FROM stdin;
1	1	X nedir	cok_secmeli	10		
2	1	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
3	1	tar komutu dosya sıkıştırmak için kullanılır	dogru_yanlis	10	kavrama	cok_kolay
4	1	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	15	uygulama	orta
5	1	Linux dosya sistemi hiyerarşisini açıklayın	acik_uclu	25	analiz	zor
6	3	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
7	3	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
8	3	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
9	3	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
10	3	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
11	4	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
12	4	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
13	4	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
14	4	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
15	4	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
16	5	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
17	5	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
18	5	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
19	5	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
20	5	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
21	6	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
22	6	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
23	6	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
24	6	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
25	6	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
26	7	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
27	7	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
28	7	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
29	7	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
30	7	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
31	8	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
32	8	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
33	8	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
34	8	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
35	8	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
36	9	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
37	9	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
38	9	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
39	9	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
40	9	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
41	10	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
42	10	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
43	10	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
44	10	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
45	10	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
46	11	asdşasd	cok_secmeli	10	bilgi	kolay
47	12	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
48	12	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
49	12	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
50	12	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
51	12	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
52	13	cp komutu ne işe yarar?	cok_secmeli	20	bilgi	kolay
53	13	Hangi komut dizin oluşturur?	cok_secmeli	20	kavrama	kolay
54	13	tar komutu dosyaları arşivlemek için kullanılır	dogru_yanlis	10	bilgi	cok_kolay
55	13	Dosya silmek için kullanılan komut: ___	bosluk_doldurma	25	uygulama	orta
56	13	Linux dosya sistemi hiyerarşisini kısaca açıklayın	acik_uclu	25	analiz	zor
57	1	Test?	cok_secmeli	10		
\.


--
-- Data for Name: terminal_guvenlik_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.terminal_guvenlik_log (id, tarih, saat, ip, session_numara, session_ad, girilen_numara, durum, uyari_gonderildi) FROM stdin;
1	2026-03-05	23:12:57	192.168.111.52	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
2	2026-03-05	23:23:52	127.0.0.1	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
3	2026-03-06	01:45:03	127.0.0.1	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
4	2026-03-06	01:48:09	192.168.111.52	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
5	2026-03-06	02:06:38	192.168.111.52	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
6	2026-03-06	02:14:00	192.168.111.52	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
7	2026-03-09	10:15:22	172.16.0.139	25901004	ALPEREN DURKUT	25901004	OTOMATIK_GIRIS	0
8	2026-03-09	10:15:45	172.16.0.36	25905009	VEYSEL KAAN DÜMAN	25905009	OTOMATIK_GIRIS	0
9	2026-03-09	10:15:45	172.16.0.178	25902002	ENES ÖZTÜRK	25902002	OTOMATIK_GIRIS	0
10	2026-03-09	10:16:29	172.16.0.72	25905013	ATA ÇAĞAN KESKİN	25905013	OTOMATIK_GIRIS	0
11	2026-03-09	10:16:36	172.16.0.39	25905018	EREN DUMRUL	25905018	OTOMATIK_GIRIS	0
12	2026-03-09	10:16:42	172.16.0.20	25901003	FURKAN SAFA ÇÜRÜTTÜ	25901003	OTOMATIK_GIRIS	0
13	2026-03-09	10:22:26	172.16.0.107	25903006	ESMANUR DİNÇER	25903006	OTOMATIK_GIRIS	0
14	2026-03-09	10:22:26	172.16.0.63	25904017	SAFA HASOĞLU	25904017	OTOMATIK_GIRIS	0
15	2026-03-09	10:22:26	172.16.0.23	25904004	SÜLEYMAN ESER DİNÇ	25904004	OTOMATIK_GIRIS	0
16	2026-03-09	10:22:26	172.16.0.43	25902003	ARİF SEVBAN KIRIT	25902003	OTOMATIK_GIRIS	0
17	2026-03-09	10:22:26	172.16.0.11	25904011	FURKAN İLİK	25904011	OTOMATIK_GIRIS	0
18	2026-03-09	10:22:26	172.16.0.114	25901007	ARDA KARATAŞ	25901007	OTOMATIK_GIRIS	0
19	2026-03-09	10:22:26	172.16.0.26	25901011	EFEKAN İÇÖZ	25901011	OTOMATIK_GIRIS	0
20	2026-03-09	10:22:26	172.16.0.126	25901010	KAZIM EFE TAŞDEMİR	25901010	OTOMATIK_GIRIS	0
21	2026-03-09	10:22:26	172.16.0.177	25904005	SUDE ELMAS AYKIRI	25904005	OTOMATIK_GIRIS	0
22	2026-03-09	10:22:26	172.16.0.25	25901016	MUZAFFER TAHA GÜL	25901016	OTOMATIK_GIRIS	0
23	2026-03-09	10:22:26	172.16.0.9	25905028	YASİN BOLAT	25905028	OTOMATIK_GIRIS	0
24	2026-03-09	10:22:27	172.16.0.101	25902007	MEHMET CAN ERŞEN	25902007	OTOMATIK_GIRIS	0
25	2026-03-09	10:22:27	172.16.0.13	25904032	AGAH ABDULLAH SARSILMAZ	25904032	OTOMATIK_GIRIS	0
26	2026-03-09	10:22:30	172.16.0.125	25904029	EFZA KAÇMAZ	25904029	OTOMATIK_GIRIS	0
27	2026-03-09	10:22:31	172.16.0.100	25902023	EFEHAN KULU	25902023	OTOMATIK_GIRIS	0
28	2026-03-09	10:23:12	172.16.0.104	25905007	SEFA YUSUF KÜTÜK	25905007	OTOMATIK_GIRIS	0
29	2026-03-09	10:23:16	172.16.0.19	25905001	AHMET BAŞOĞLU	25905001	OTOMATIK_GIRIS	0
30	2026-03-09	10:31:09	172.16.0.179	25905008	FATMA RANA GÖKDEMİR	25905008	OTOMATIK_GIRIS	0
31	2026-03-09	10:31:09	172.16.0.38	25903015	SEVİM ÇELİK	25903015	OTOMATIK_GIRIS	0
32	2026-03-09	10:31:09	172.16.0.182	25905002	TUANNA ALTIN	25905002	OTOMATIK_GIRIS	0
33	2026-03-09	11:05:25	172.16.0.26	25901011	EFEKAN İÇÖZ	25901011	OTOMATIK_GIRIS	0
34	2026-03-09	11:49:50	172.16.0.113	25905016	BAHRİ AYDOĞDU	25905016	OTOMATIK_GIRIS	0
35	2026-03-09	11:49:50	172.16.0.118	25905020	BERAT ALİ ERİŞ	25905020	OTOMATIK_GIRIS	0
36	2026-03-09	12:26:30	127.0.0.1	123	TEST TEST	123	OTOMATIK_GIRIS	0
37	2026-03-09	13:16:53	172.16.0.43	25902012	FAHRİ ARDA KARATAŞ	25902012	OTOMATIK_GIRIS	0
38	2026-03-09	13:16:54	172.16.0.113	25904018	YAVUZ SELİM SEZER	25904018	OTOMATIK_GIRIS	0
39	2026-03-09	13:16:54	172.16.0.25	25901008	EZGİ YILDIZ	25901008	OTOMATIK_GIRIS	0
40	2026-03-09	13:16:55	172.16.0.107	25903003	BÜŞRA SENA MUTLU	25903003	OTOMATIK_GIRIS	0
41	2026-03-09	13:16:55	172.16.0.177	25903001	AHMET MAHLİ	25903001	OTOMATIK_GIRIS	0
42	2026-03-09	13:16:55	172.16.0.20	25905012	ERKAM SONUÇ	25905012	OTOMATIK_GIRIS	0
43	2026-03-09	13:16:55	172.16.0.101	25905011	KAMURAN İNAN AYDOĞAN	25905011	OTOMATIK_GIRIS	0
44	2026-03-09	13:17:02	172.16.0.39	25902013	MUSTAFA ŞAHİN	25902013	OTOMATIK_GIRIS	0
45	2026-03-09	13:17:04	172.16.0.72	25902009	RESUL EKREM ÖZCAN	25902009	OTOMATIK_GIRIS	0
46	2026-03-09	13:17:04	172.16.0.112	25904024	SUDE ÖZTÜRK	25904024	OTOMATIK_GIRIS	0
47	2026-03-09	13:17:05	172.16.0.182	25904027	YUSUF ŞAHBAZ	25904027	OTOMATIK_GIRIS	0
48	2026-03-09	13:48:43	172.16.0.47	25903009	CEMRE SU GENÇ	25903009	OTOMATIK_GIRIS	0
49	2026-03-09	13:48:43	172.16.0.108	25904019	YUSUF ENES BİLGİN	25904019	OTOMATIK_GIRIS	0
50	2026-03-09	13:48:43	172.16.0.125	25903010	AZRA ŞAHİN	25903010	OTOMATIK_GIRIS	0
51	2026-03-09	13:48:43	172.16.0.139	25904036	ZEREN NEBİOĞLU	25904036	OTOMATIK_GIRIS	0
52	2026-03-09	13:48:44	172.16.0.126	25902017	TARIK BUĞRA BODUR	25902017	OTOMATIK_GIRIS	0
53	2026-03-09	13:48:44	172.16.0.178	25904030	AYŞE DEMİRKAYA	25904030	OTOMATIK_GIRIS	0
54	2026-03-09	13:48:44	172.16.0.19	25902008	MUSTAFA ÇETİN	25902008	OTOMATIK_GIRIS	0
55	2026-03-09	13:48:44	172.16.0.29	25903004	MİRAY KAMİLE TİRAŞ	25903004	OTOMATIK_GIRIS	0
56	2026-03-09	13:48:44	172.16.0.9	25902010	AHMET FARUK YÜKSEL	25902010	OTOMATIK_GIRIS	0
57	2026-03-09	13:48:44	172.16.0.118	25904012	MEHMET EREN BODUROĞLU	25904012	OTOMATIK_GIRIS	0
58	2026-03-09	14:01:30	172.16.0.61	25903011	SEMİH ÇELİKEL	25903011	OTOMATIK_GIRIS	0
59	2026-03-09	14:02:04	172.16.0.100	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
60	2026-03-09	14:03:07	172.16.0.121	25903013	AHMET MERT KÖYBAŞI	25903013	OTOMATIK_GIRIS	0
61	2026-03-09	14:23:59	172.16.0.45	25904020	ALMILA FATMA ÖZER	25904020	OTOMATIK_GIRIS	0
62	2026-03-09	15:40:46	172.16.0.177	25901017	ÖMER YEŞİLYURT	25901017	OTOMATIK_GIRIS	0
63	2026-03-09	16:44:37	172.16.0.38	25901012	NİSA NUR ÇELİK	25901012	OTOMATIK_GIRIS	0
64	2026-03-09	16:44:37	172.16.0.43	25904007	ERTÜMEN YAYLA	25904007	OTOMATIK_GIRIS	0
65	2026-03-09	16:44:37	172.16.0.108	25902020	DOĞUKAN DURAN	25902020	OTOMATIK_GIRIS	0
66	2026-03-09	16:44:38	172.16.0.101	25904004	SÜLEYMAN ESER DİNÇ	25904004	OTOMATIK_GIRIS	0
67	2026-03-09	16:44:38	172.16.0.120	25904016	MEHMET ENES KAYA	25904016	OTOMATIK_GIRIS	0
68	2026-03-09	16:44:41	172.16.0.125	25901018	ZEHRA YILDIRIM	25901018	OTOMATIK_GIRIS	0
69	2026-03-09	16:44:41	172.16.0.20	25904037	MUHAMMED EFENDİ AYHANOĞLU	25904037	OTOMATIK_GIRIS	0
70	2026-03-09	16:44:45	172.16.0.107	25902021	ESRA BAYRAM	25902021	OTOMATIK_GIRIS	0
71	2026-03-09	16:44:46	172.16.0.178	25903002	İREM UYSAL	25903002	OTOMATIK_GIRIS	0
72	2026-03-09	16:44:53	172.16.0.72	25904001	ALAATTİN EFE YURTERİ	25904001	OTOMATIK_GIRIS	0
73	2026-03-09	16:44:55	172.16.0.118	25902025	BURAK AYYILDIZ	25902025	OTOMATIK_GIRIS	0
74	2026-03-09	16:44:55	172.16.0.114	25904010	EMİRHAN ESENOĞLU	25904010	OTOMATIK_GIRIS	0
75	2026-03-09	16:44:59	172.16.0.39	25904022	MEHMET KAYRA AKKUŞ	25904022	OTOMATIK_GIRIS	0
76	2026-03-11	11:16:29	192.168.111.77	123	TEST TEST	123	OTOMATIK_GIRIS	0
77	2026-03-29	23:26:57	192.168.31.80	123	TEST TEST	123	OTOMATIK_GIRIS	0
78	2026-03-29	23:51:47	127.0.0.1	123	TEST TEST	123	OTOMATIK_GIRIS	0
79	2026-03-29	23:57:18	127.0.0.1	123	TEST TEST	123	OTOMATIK_GIRIS	0
80	2026-03-30	09:26:28	172.16.0.70	25902002	ENES ÖZTÜRK	25902002	OTOMATIK_GIRIS	0
81	2026-03-30	09:26:28	172.16.0.47	25902001	İLKAY ŞIK	25902001	OTOMATIK_GIRIS	0
82	2026-03-30	09:26:28	172.16.0.39	25901002	BEHİÇ ARDA DEMİRER	25901002	OTOMATIK_GIRIS	0
83	2026-03-30	09:26:28	172.16.0.120	25905003	DİLEK KARAÇE	25905003	OTOMATIK_GIRIS	0
84	2026-03-30	09:26:28	172.16.0.126	25904008	ZEHRA ÇALIK	25904008	OTOMATIK_GIRIS	0
85	2026-03-30	09:26:28	172.16.0.63	25903012	MUHAMMED HAKTAN SAZÇALAN	25903012	OTOMATIK_GIRIS	0
86	2026-03-30	09:26:29	172.16.0.104	25905001	AHMET BAŞOĞLU	25905001	OTOMATIK_GIRIS	0
87	2026-03-30	09:26:29	172.16.0.125	25904033	SAHRA GÜNDOĞDU	25904033	OTOMATIK_GIRIS	0
88	2026-03-30	09:26:29	172.16.0.56	25904038	YUNUS EMRE KARAKEÇİLİ	25904038	OTOMATIK_GIRIS	0
89	2026-03-30	09:26:29	172.16.0.42	25905022	ISMAIL KAAN YÜKSEKER	25905022	OTOMATIK_GIRIS	0
90	2026-03-30	09:26:29	172.16.0.107	25904006	İREM GENEŞ	25904006	OTOMATIK_GIRIS	0
91	2026-03-30	09:26:29	172.16.0.44	25905007	SEFA YUSUF KÜTÜK	25905007	OTOMATIK_GIRIS	0
92	2026-03-30	09:26:29	172.16.0.66	25904002	SALİH GÖKAY KÖKSAL	25904002	OTOMATIK_GIRIS	0
93	2026-03-30	09:26:29	172.16.0.177	25904005	SUDE ELMAS AYKIRI	25904005	OTOMATIK_GIRIS	0
94	2026-03-30	09:26:29	172.16.0.108	25904041	İSMET HALİT DEMİRCİ	25904041	OTOMATIK_GIRIS	0
95	2026-03-30	09:26:29	172.16.0.84	25904032	AGAH ABDULLAH SARSILMAZ	25904032	OTOMATIK_GIRIS	0
96	2026-03-30	09:26:29	172.16.0.112	25902004	EYLÜL KAYA	25902004	OTOMATIK_GIRIS	0
97	2026-03-30	09:26:29	172.16.0.43	25904003	SÜHEYLA TUĞÇE GÜN	25904003	OTOMATIK_GIRIS	0
98	2026-03-30	09:26:29	172.16.0.26	25901011	EFEKAN İÇÖZ	25901011	OTOMATIK_GIRIS	0
99	2026-03-30	09:26:29	172.16.0.85	25905015	YUNUS EGE MÖNÜR	25905015	OTOMATIK_GIRIS	0
100	2026-03-30	09:26:29	172.16.0.101	25904011	FURKAN İLİK	25904011	OTOMATIK_GIRIS	0
101	2026-03-30	09:26:29	172.16.0.62	25905009	VEYSEL KAAN DÜMAN	25905009	OTOMATIK_GIRIS	0
102	2026-03-30	09:26:29	172.16.0.61	25901006	EREN GÜLER	25901006	OTOMATIK_GIRIS	0
103	2026-03-30	09:26:29	172.16.0.14	24090003	EFE BARAN DEMIRHAN	24090003	OTOMATIK_GIRIS	0
104	2026-03-30	09:26:29	172.16.0.118	25904023	HASAN ARDA TAHTACI	25904023	OTOMATIK_GIRIS	0
105	2026-03-30	09:26:29	172.16.0.113	25905011	KAMURAN İNAN AYDOĞAN	25905011	OTOMATIK_GIRIS	0
106	2026-03-30	09:26:29	172.16.0.114	25901007	ARDA KARATAŞ	25901007	OTOMATIK_GIRIS	0
107	2026-03-30	09:26:29	172.16.0.23	25901003	FURKAN SAFA ÇÜRÜTTÜ	25901003	OTOMATIK_GIRIS	0
108	2026-03-30	09:26:29	172.16.0.57	25904035	GÖKTUĞ ERDEM PEHLİVAN	25904035	OTOMATIK_GIRIS	0
109	2026-03-30	09:26:29	172.16.0.139	25901004	ALPEREN DURKUT	25901004	OTOMATIK_GIRIS	0
110	2026-03-30	09:26:29	172.16.0.100	25905016	BAHRİ AYDOĞDU	25905016	OTOMATIK_GIRIS	0
111	2026-03-30	09:26:29	172.16.0.41	25903015	SEVİM ÇELİK	25903015	OTOMATIK_GIRIS	0
112	2026-03-30	09:26:29	172.16.0.10	25901005	SALİH BİLAL KORKMAZ	25901005	OTOMATIK_GIRIS	0
113	2026-03-30	09:26:29	172.16.0.4	25902007	MEHMET CAN ERŞEN	25902007	OTOMATIK_GIRIS	0
114	2026-03-30	09:26:29	172.16.0.179	25903006	ESMANUR DİNÇER	25903006	OTOMATIK_GIRIS	0
115	2026-03-30	09:26:34	172.16.0.72	25904026	ONUR YENİPAZARLI	25904026	OTOMATIK_GIRIS	0
116	2026-03-30	09:26:38	172.16.0.10	25901010	KAZIM EFE TAŞDEMİR	25901010	OTOMATIK_GIRIS	0
117	2026-03-30	09:39:47	172.16.0.126	25904029	EFZA KAÇMAZ	25904029	OTOMATIK_GIRIS	0
118	2026-03-30	10:06:48	172.16.0.62	25905009	VEYSEL KAAN DÜMAN	25905009	OTOMATIK_GIRIS	0
119	2026-03-30	10:08:36	172.16.0.23	25901003	FURKAN SAFA ÇÜRÜTTÜ	25901003	OTOMATIK_GIRIS	0
120	2026-03-30	10:35:14	172.16.0.70	25902002	ENES ÖZTÜRK	25902002	OTOMATIK_GIRIS	0
121	2026-03-30	10:57:22	172.16.0.26	25901011	EFEKAN İÇÖZ	25901011	OTOMATIK_GIRIS	0
122	2026-03-30	10:57:49	172.16.0.47	25902001	İLKAY ŞIK	25902001	OTOMATIK_GIRIS	0
123	2026-03-30	10:58:12	172.16.0.26	25901011	EFEKAN İÇÖZ	25901011	OTOMATIK_GIRIS	0
124	2026-03-30	10:58:30	172.16.0.47	25902001	İLKAY ŞIK	25902001	OTOMATIK_GIRIS	0
125	2026-03-30	11:07:39	172.16.0.41	25903015	SEVİM ÇELİK	25903015	OTOMATIK_GIRIS	0
126	2026-03-30	13:19:46	172.16.0.61	25903002	İREM UYSAL	25903002	OTOMATIK_GIRIS	0
127	2026-03-30	13:19:46	172.16.0.104	25904021	ÖMER YILDIZ	25904021	OTOMATIK_GIRIS	0
128	2026-03-30	13:19:46	172.16.0.70	25904030	AYŞE DEMİRKAYA	25904030	OTOMATIK_GIRIS	0
129	2026-03-30	13:19:46	172.16.0.179	25902024	EFEHAN EKINCI	25902024	OTOMATIK_GIRIS	0
130	2026-03-30	13:19:51	172.16.0.62	25902014	ZÜBEYİR CUMA YILMAZ	25902014	OTOMATIK_GIRIS	0
131	2026-03-30	13:19:51	172.16.0.114	25905012	ERKAM SONUÇ	25905012	OTOMATIK_GIRIS	0
132	2026-03-30	13:19:51	172.16.0.101	25902013	MUSTAFA ŞAHİN	25902013	OTOMATIK_GIRIS	0
133	2026-03-30	13:19:51	172.16.0.112	25903007	TUĞBA GÜLMEZ	25903007	OTOMATIK_GIRIS	0
134	2026-03-30	13:19:51	172.16.0.57	25902012	FAHRİ ARDA KARATAŞ	25902012	OTOMATIK_GIRIS	0
135	2026-03-30	13:19:52	172.16.0.177	25905008	FATMA RANA GÖKDEMİR	25905008	OTOMATIK_GIRIS	0
136	2026-03-30	13:19:52	172.16.0.139	25903004	MİRAY KAMİLE TİRAŞ	25903004	OTOMATIK_GIRIS	0
137	2026-03-30	13:19:52	172.16.0.182	25904027	YUSUF ŞAHBAZ	25904027	OTOMATIK_GIRIS	0
138	2026-03-30	13:19:52	172.16.0.39	25903010	AZRA ŞAHİN	25903010	OTOMATIK_GIRIS	0
139	2026-03-30	13:19:52	172.16.0.125	25905002	TUANNA ALTIN	25905002	OTOMATIK_GIRIS	0
140	2026-03-30	13:19:57	172.16.0.85	25901016	MUZAFFER TAHA GÜL	25901016	OTOMATIK_GIRIS	0
141	2026-03-30	13:19:57	172.16.0.66	25904010	EMİRHAN ESENOĞLU	25904010	OTOMATIK_GIRIS	0
142	2026-03-30	13:19:57	172.16.0.41	25903013	AHMET MERT KÖYBAŞI	25903013	OTOMATIK_GIRIS	0
143	2026-03-30	13:19:57	172.16.0.14	25901008	EZGİ YILDIZ	25901008	OTOMATIK_GIRIS	0
144	2026-03-30	13:19:57	172.16.0.100	25904018	YAVUZ SELİM SEZER	25904018	OTOMATIK_GIRIS	0
145	2026-03-30	13:19:57	172.16.0.43	25905027	İNCİ HALICI	25905027	OTOMATIK_GIRIS	0
146	2026-03-30	13:19:57	172.16.0.107	25905013	ATA ÇAĞAN KESKİN	25905013	OTOMATIK_GIRIS	0
147	2026-03-30	13:19:57	172.16.0.26	25901012	NİSA NUR ÇELİK	25901012	OTOMATIK_GIRIS	0
148	2026-03-30	13:19:57	172.16.0.47	25903001	AHMET MAHLİ	25903001	OTOMATIK_GIRIS	0
149	2026-03-30	13:19:57	172.16.0.120	25903008	HATİCE ÖZLÜ	25903008	OTOMATIK_GIRIS	0
150	2026-03-30	13:20:02	172.16.0.56	25902008	MUSTAFA ÇETİN	25902008	OTOMATIK_GIRIS	0
151	2026-03-30	13:20:02	172.16.0.44	25904014	AHMET TAYLAN ERDEN	25904014	OTOMATIK_GIRIS	0
152	2026-03-30	13:20:03	172.16.0.63	25903011	SEMİH ÇELİKEL	25903011	OTOMATIK_GIRIS	0
153	2026-03-30	13:20:03	172.16.0.126	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
154	2026-03-30	13:20:03	172.16.0.84	25902009	RESUL EKREM ÖZCAN	25902009	OTOMATIK_GIRIS	0
155	2026-03-30	13:20:03	172.16.0.42	25904039	ÖMER FARUK GÖKSU	25904039	OTOMATIK_GIRIS	0
156	2026-03-30	13:20:03	172.16.0.23	25905018	EREN DUMRUL	25905018	OTOMATIK_GIRIS	0
157	2026-03-30	13:20:04	172.16.0.4	25902021	ESRA BAYRAM	25902021	OTOMATIK_GIRIS	0
158	2026-03-30	13:20:04	172.16.0.72	25904012	MEHMET EREN BODUROĞLU	25904012	OTOMATIK_GIRIS	0
159	2026-03-30	13:20:04	172.16.0.108	25904019	YUSUF ENES BİLGİN	25904019	OTOMATIK_GIRIS	0
160	2026-03-30	13:20:07	172.16.0.118	25904017	SAFA HASOĞLU	25904017	OTOMATIK_GIRIS	0
161	2026-03-30	13:20:57	172.16.0.126	25902010	AHMET FARUK YÜKSEL	25902010	OTOMATIK_GIRIS	0
162	2026-03-30	13:45:07	172.16.0.125	25905002	TUANNA ALTIN	25905002	OTOMATIK_GIRIS	0
163	2026-03-30	14:13:07	172.16.0.125	25905002	TUANNA ALTIN	25905002	OTOMATIK_GIRIS	0
164	2026-03-30	14:15:35	172.16.0.85	25904401	SALIH DEMIRTAŞ	25904401	OTOMATIK_GIRIS	0
165	2026-03-30	14:33:53	172.16.0.121	25902025	BURAK AYYILDIZ	25902025	OTOMATIK_GIRIS	0
166	2026-03-30	14:38:12	172.16.0.61	25903002	İREM UYSAL	25903002	OTOMATIK_GIRIS	0
167	2026-03-30	14:38:37	172.16.0.125	25905002	TUANNA ALTIN	25905002	OTOMATIK_GIRIS	0
168	2026-03-30	14:45:33	172.16.0.61	25903002	İREM UYSAL	25903002	OTOMATIK_GIRIS	0
169	2026-03-30	14:48:30	172.16.0.41	25903013	AHMET MERT KÖYBAŞI	25903013	OTOMATIK_GIRIS	0
170	2026-03-30	14:51:16	172.16.0.139	25903004	MİRAY KAMİLE TİRAŞ	25903004	OTOMATIK_GIRIS	0
171	2026-03-30	14:53:19	172.16.0.113	25904025	ÖYKÜM NİLDENİZ AKPINAR	25904025	OTOMATIK_GIRIS	0
172	2026-03-30	14:57:04	172.16.0.121	25902025	BURAK AYYILDIZ	25902025	OTOMATIK_GIRIS	0
173	2026-03-30	14:59:29	172.16.0.100	25902010	AHMET FARUK YÜKSEL	25902010	OTOMATIK_GIRIS	0
174	2026-03-30	15:46:29	172.16.0.4	25902023	EFEHAN KULU	25902023	OTOMATIK_GIRIS	0
175	2026-03-30	15:46:30	172.16.0.42	25905020	BERAT ALİ ERİŞ	25905020	OTOMATIK_GIRIS	0
176	2026-03-30	15:46:31	172.16.0.41	25901018	ZEHRA YILDIRIM	25901018	OTOMATIK_GIRIS	0
177	2026-03-30	15:46:31	172.16.0.14	25905028	YASİN BOLAT	25905028	OTOMATIK_GIRIS	0
178	2026-03-30	15:46:32	172.16.0.121	25902020	DOĞUKAN DURAN	25902020	OTOMATIK_GIRIS	0
179	2026-03-30	15:46:33	172.16.0.62	25905017	MEHMET ARDA YENENER	25905017	OTOMATIK_GIRIS	0
180	2026-03-30	15:46:34	172.16.0.63	25901017	ÖMER YEŞİLYURT	25901017	OTOMATIK_GIRIS	0
181	2026-03-30	15:46:41	172.16.0.139	25146901	SAMI KARACA	25146901	OTOMATIK_GIRIS	0
182	2026-03-30	15:47:15	172.16.0.120	25903009	CEMRE SU GENÇ	25903009	OTOMATIK_GIRIS	0
183	2026-03-30	15:47:37	172.16.0.118	25904004	SÜLEYMAN ESER DİNÇ	25904004	OTOMATIK_GIRIS	0
184	2026-03-30	15:48:21	172.16.0.104	25904007	ERTÜMEN YAYLA	25904007	OTOMATIK_GIRIS	0
185	2026-03-30	15:48:58	172.16.0.179	25904016	MEHMET ENES KAYA	25904016	OTOMATIK_GIRIS	0
186	2026-03-30	15:51:11	172.16.0.113	25904022	MEHMET KAYRA AKKUŞ	25904022	OTOMATIK_GIRIS	0
187	2026-03-30	15:51:14	172.16.0.182	25904001	ALAATTİN EFE YURTERİ	25904001	OTOMATIK_GIRIS	0
188	2026-03-30	15:54:06	172.16.0.84	25904043	HASAN BERK KOCA	25904043	OTOMATIK_GIRIS	0
189	2026-03-30	15:58:47	172.16.0.57	25904028	BÜNYAMİN EFE BULUT	25904028	OTOMATIK_GIRIS	0
190	2026-03-30	15:59:28	172.16.0.57	25904028	BÜNYAMİN EFE BULUT	25904028	OTOMATIK_GIRIS	0
191	2026-03-30	15:59:46	172.16.0.121	25904020	ALMILA FATMA ÖZER	25904020	OTOMATIK_GIRIS	0
192	2026-03-30	16:00:00	172.16.0.72	25904037	MUHAMMED EFENDİ AYHANOĞLU	25904037	OTOMATIK_GIRIS	0
193	2026-03-30	16:00:41	172.16.0.14	25905028	YASİN BOLAT	25905028	OTOMATIK_GIRIS	0
194	2026-03-30	16:02:14	172.16.0.72	25904037	MUHAMMED EFENDİ AYHANOĞLU	25904037	OTOMATIK_GIRIS	0
195	2026-03-30	16:02:53	172.16.0.39	25904024	SUDE ÖZTÜRK	25904024	OTOMATIK_GIRIS	0
196	2026-03-30	16:08:51	172.16.0.41	25904036	ZEREN NEBİOĞLU	25904036	OTOMATIK_GIRIS	0
197	2026-03-30	16:21:11	172.16.0.139	25146901	SAMI KARACA	25146901	OTOMATIK_GIRIS	0
198	2026-03-30	16:31:39	172.16.0.139	25146901	SAMI KARACA	25146901	OTOMATIK_GIRIS	0
199	2026-03-30	16:36:36	172.16.0.47	25146901	SAMI KARACA	25146901	OTOMATIK_GIRIS	0
200	2026-03-30	16:48:49	172.16.0.43	25901017	ÖMER YEŞİLYURT	25901017	OTOMATIK_GIRIS	0
201	2026-03-30	16:49:40	172.16.0.125	25901018	ZEHRA YILDIRIM	25901018	OTOMATIK_GIRIS	0
202	2026-03-30	16:56:00	172.16.0.107	25902020	DOĞUKAN DURAN	25902020	OTOMATIK_GIRIS	0
203	2026-03-30	17:07:15	172.16.0.62	25905017	MEHMET ARDA YENENER	25905017	OTOMATIK_GIRIS	0
204	2026-03-30	17:07:26	172.16.0.39	25904024	SUDE ÖZTÜRK	25904024	OTOMATIK_GIRIS	0
205	2026-03-30	17:10:51	172.16.0.72	25904037	MUHAMMED EFENDİ AYHANOĞLU	25904037	OTOMATIK_GIRIS	0
206	2026-03-30	17:11:35	172.16.0.84	25904043	HASAN BERK KOCA	25904043	OTOMATIK_GIRIS	0
207	2026-03-30	17:12:18	172.16.0.72	25904037	MUHAMMED EFENDİ AYHANOĞLU	25904037	OTOMATIK_GIRIS	0
208	2026-03-30	17:12:42	172.16.0.113	25904022	MEHMET KAYRA AKKUŞ	25904022	OTOMATIK_GIRIS	0
209	2026-03-30	17:13:00	172.16.0.57	25904028	BÜNYAMİN EFE BULUT	25904028	OTOMATIK_GIRIS	0
210	2026-03-30	17:39:59	172.16.0.47	25146901	SAMI KARACA	25146901	OTOMATIK_GIRIS	0
211	2026-03-30	17:45:03	172.16.0.62	25905017	MEHMET ARDA YENENER	25905017	OTOMATIK_GIRIS	0
212	2026-04-01	16:13:07	127.0.0.1	123	TEST TEST	123	OTOMATIK_GIRIS	0
213	2026-04-02	13:39:11	127.0.0.1	123	TEST TEST	123	OTOMATIK_GIRIS	0
214	2026-04-02	21:37:53	192.168.111.53	test4	Öğrenci-4 TEST	test4	OTOMATIK_GIRIS	0
215	2026-04-02	22:27:15	127.0.0.1	001	A B	001	OTOMATIK_GIRIS	0
216	2026-04-02	22:30:34	192.168.111.53	001	A B	001	OTOMATIK_GIRIS	0
217	2026-04-02	22:47:22	192.168.111.53	test4	Öğrenci-4 TEST	test4	OTOMATIK_GIRIS	0
218	2026-04-02	22:47:48	192.168.111.53	test5	Öğrenci-5 TEST	test5	OTOMATIK_GIRIS	0
219	2026-04-02	22:49:00	192.168.111.53	test5	Öğrenci-5 TEST	test5	OTOMATIK_GIRIS	0
220	2026-04-02	23:12:27	192.168.111.53	test1	Öğrenci-1 TEST	test1	OTOMATIK_GIRIS	0
221	2026-04-02	23:13:53	192.168.111.53	test2	Öğrenci-2 TEST	test2	OTOMATIK_GIRIS	0
222	2026-04-02	23:15:10	192.168.111.53	test1	Öğrenci-1 TEST	test1	OTOMATIK_GIRIS	0
223	2026-04-02	23:15:29	192.168.111.53	test1	Öğrenci-1 TEST	test1	OTOMATIK_GIRIS	0
224	2026-04-03	00:00:13	127.0.0.1	test1	Öğrenci-1 TEST	test1	OTOMATIK_GIRIS	0
225	2026-04-06	10:54:34	172.16.0.74	25902003	ARİF SEVBAN KIRIT	25902003	OTOMATIK_GIRIS	0
226	2026-04-06	10:54:34	172.16.0.43	25905008	FATMA RANA GÖKDEMİR	25905008	OTOMATIK_GIRIS	0
227	2026-04-06	10:54:34	172.16.0.73	25904023	HASAN ARDA TAHTACI	25904023	OTOMATIK_GIRIS	0
228	2026-04-06	10:54:34	172.16.0.48	25901002	BEHİÇ ARDA DEMİRER	25901002	OTOMATIK_GIRIS	0
229	2026-04-06	10:54:34	172.16.0.108	25905006	RECEP FURKAN ÇELİK	25905006	OTOMATIK_GIRIS	0
230	2026-04-06	10:54:34	172.16.0.100	25903015	SEVİM ÇELİK	25903015	OTOMATIK_GIRIS	0
231	2026-04-06	10:54:34	172.16.0.14	25904014	AHMET TAYLAN ERDEN	25904014	OTOMATIK_GIRIS	0
232	2026-04-06	10:54:34	172.16.0.78	24090003	EFE BARAN DEMIRHAN	24090003	OTOMATIK_GIRIS	0
233	2026-04-06	10:54:34	172.16.0.126	25901011	EFEKAN İÇÖZ	25901011	OTOMATIK_GIRIS	0
234	2026-04-06	10:54:34	172.16.0.13	25901005	SALİH BİLAL KORKMAZ	25901005	OTOMATIK_GIRIS	0
235	2026-04-06	10:54:34	172.16.0.39	25903003	BÜŞRA SENA MUTLU	25903003	OTOMATIK_GIRIS	0
236	2026-04-06	10:54:34	172.16.0.120	24118904	ABDELRAHMAN KHALIL	24118904	OTOMATIK_GIRIS	0
237	2026-04-06	10:54:34	172.16.0.139	25904032	AGAH ABDULLAH SARSILMAZ	25904032	OTOMATIK_GIRIS	0
238	2026-04-06	10:54:34	172.16.0.11	25904041	İSMET HALİT DEMİRCİ	25904041	OTOMATIK_GIRIS	0
239	2026-04-06	10:54:34	172.16.0.56	25903006	ESMANUR DİNÇER	25903006	OTOMATIK_GIRIS	0
240	2026-04-06	10:54:34	172.16.0.118	25904011	FURKAN İLİK	25904011	OTOMATIK_GIRIS	0
241	2026-04-06	10:54:34	172.16.0.61	24090901	AMINJON PRIMOV	24090901	OTOMATIK_GIRIS	0
242	2026-04-06	10:54:34	172.16.0.179	25902001	İLKAY ŞIK	25902001	OTOMATIK_GIRIS	0
243	2026-04-06	10:54:34	172.16.0.125	25904033	SAHRA GÜNDOĞDU	25904033	OTOMATIK_GIRIS	0
244	2026-04-06	10:54:34	172.16.0.84	25904008	ZEHRA ÇALIK	25904008	OTOMATIK_GIRIS	0
245	2026-04-06	10:54:34	172.16.0.101	25904029	EFZA KAÇMAZ	25904029	OTOMATIK_GIRIS	0
246	2026-04-06	10:54:34	172.16.0.54	25904038	YUNUS EMRE KARAKEÇİLİ	25904038	OTOMATIK_GIRIS	0
247	2026-04-06	10:54:34	172.16.0.107	25905003	DİLEK KARAÇE	25905003	OTOMATIK_GIRIS	0
248	2026-04-06	10:54:34	172.16.0.177	25904005	SUDE ELMAS AYKIRI	25904005	OTOMATIK_GIRIS	0
249	2026-04-06	10:54:34	172.16.0.75	25904017	SAFA HASOĞLU	25904017	OTOMATIK_GIRIS	0
250	2026-04-06	10:54:34	172.16.0.104	25904035	GÖKTUĞ ERDEM PEHLİVAN	25904035	OTOMATIK_GIRIS	0
251	2026-04-06	10:54:34	172.16.0.41	25901004	ALPEREN DURKUT	25901004	OTOMATIK_GIRIS	0
252	2026-04-06	10:54:34	172.16.0.23	25901003	FURKAN SAFA ÇÜRÜTTÜ	25901003	OTOMATIK_GIRIS	0
253	2026-04-06	10:54:34	172.16.0.85	25903009	CEMRE SU GENÇ	25903009	OTOMATIK_GIRIS	0
254	2026-04-06	10:54:34	172.16.0.112	25902004	EYLÜL KAYA	25902004	OTOMATIK_GIRIS	0
255	2026-04-06	10:54:34	172.16.0.114	25902002	ENES ÖZTÜRK	25902002	OTOMATIK_GIRIS	0
256	2026-04-06	10:56:57	172.16.0.108	25905006	RECEP FURKAN ÇELİK	25905006	OTOMATIK_GIRIS	0
257	2026-04-06	10:56:57	172.16.0.63	25903012	MUHAMMED HAKTAN SAZÇALAN	25903012	OTOMATIK_GIRIS	0
258	2026-04-06	10:56:57	172.16.0.26	25902007	MEHMET CAN ERŞEN	25902007	OTOMATIK_GIRIS	0
259	2026-04-06	14:30:10	172.16.0.121	25901006	EREN GÜLER	25901006	OTOMATIK_GIRIS	0
260	2026-04-06	14:30:10	172.16.0.61	25901010	KAZIM EFE TAŞDEMİR	25901010	OTOMATIK_GIRIS	0
261	2026-04-06	14:30:10	172.16.0.108	25903010	AZRA ŞAHİN	25903010	OTOMATIK_GIRIS	0
262	2026-04-06	14:30:10	172.16.0.107	25904006	İREM GENEŞ	25904006	OTOMATIK_GIRIS	0
263	2026-04-06	14:30:10	172.16.0.41	25901007	ARDA KARATAŞ	25901007	OTOMATIK_GIRIS	0
264	2026-04-06	14:30:10	172.16.0.55	25904039	ÖMER FARUK GÖKSU	25904039	OTOMATIK_GIRIS	0
265	2026-04-06	14:30:10	172.16.0.104	25902014	ZÜBEYİR CUMA YILMAZ	25902014	OTOMATIK_GIRIS	0
266	2026-04-06	14:30:10	172.16.0.14	25905013	ATA ÇAĞAN KESKİN	25905013	OTOMATIK_GIRIS	0
267	2026-04-06	14:30:10	172.16.0.139	25905012	ERKAM SONUÇ	25905012	OTOMATIK_GIRIS	0
268	2026-04-06	14:30:10	172.16.0.85	25905009	VEYSEL KAAN DÜMAN	25905009	OTOMATIK_GIRIS	0
269	2026-04-06	14:30:10	172.16.0.182	25903013	AHMET MERT KÖYBAŞI	25903013	OTOMATIK_GIRIS	0
270	2026-04-06	14:30:10	172.16.0.26	25902012	FAHRİ ARDA KARATAŞ	25902012	OTOMATIK_GIRIS	0
271	2026-04-06	14:30:10	172.16.0.118	25903001	AHMET MAHLİ	25903001	OTOMATIK_GIRIS	0
272	2026-04-06	14:30:10	172.16.0.54	25904012	MEHMET EREN BODUROĞLU	25904012	OTOMATIK_GIRIS	0
273	2026-04-06	14:30:11	172.16.0.23	25902008	MUSTAFA ÇETİN	25902008	OTOMATIK_GIRIS	0
274	2026-04-06	14:30:13	172.16.0.11	25904036	ZEREN NEBİOĞLU	25904036	OTOMATIK_GIRIS	0
275	2026-04-06	14:30:13	172.16.0.101	25904024	SUDE ÖZTÜRK	25904024	OTOMATIK_GIRIS	0
276	2026-04-06	14:30:13	172.16.0.73	25903004	MİRAY KAMİLE TİRAŞ	25903004	OTOMATIK_GIRIS	0
277	2026-04-06	14:30:13	172.16.0.63	25904021	ÖMER YILDIZ	25904021	OTOMATIK_GIRIS	0
278	2026-04-06	14:30:13	172.16.0.84	25904020	ALMILA FATMA ÖZER	25904020	OTOMATIK_GIRIS	0
279	2026-04-06	14:30:14	172.16.0.43	25901008	EZGİ YILDIZ	25901008	OTOMATIK_GIRIS	0
280	2026-04-06	14:30:14	172.16.0.56	25904027	YUSUF ŞAHBAZ	25904027	OTOMATIK_GIRIS	0
281	2026-04-06	14:30:24	172.16.0.100	25905015	YUNUS EGE MÖNÜR	25905015	OTOMATIK_GIRIS	0
282	2026-04-06	14:30:53	172.16.0.126	25902009	RESUL EKREM ÖZCAN	25902009	OTOMATIK_GIRIS	0
283	2026-04-06	14:31:36	172.16.0.18	25904003	SÜHEYLA TUĞÇE GÜN	25904003	OTOMATIK_GIRIS	0
284	2026-04-06	14:31:39	172.16.0.114	25905011	KAMURAN İNAN AYDOĞAN	25905011	OTOMATIK_GIRIS	0
285	2026-04-06	14:37:17	172.16.0.120	25905016	BAHRİ AYDOĞDU	25905016	OTOMATIK_GIRIS	0
286	2026-04-06	15:04:07	127.0.0.1	123	TEST TEST	123	OTOMATIK_GIRIS	0
287	2026-04-06	16:40:13	172.16.0.61	25905019	TUĞRA TAŞ	25905019	OTOMATIK_GIRIS	0
288	2026-04-06	16:40:13	172.16.0.125	25903011	SEMİH ÇELİKEL	25903011	OTOMATIK_GIRIS	0
289	2026-04-06	16:40:13	172.16.0.107	25904028	BÜNYAMİN EFE BULUT	25904028	OTOMATIK_GIRIS	0
290	2026-04-06	16:40:13	172.16.0.113	25902017	TARIK BUĞRA BODUR	25902017	OTOMATIK_GIRIS	0
291	2026-04-06	16:40:13	172.16.0.177	25904019	YUSUF ENES BİLGİN	25904019	OTOMATIK_GIRIS	0
292	2026-04-06	16:40:13	172.16.0.75	25904025	ÖYKÜM NİLDENİZ AKPINAR	25904025	OTOMATIK_GIRIS	0
293	2026-04-06	16:40:13	172.16.0.100	25902023	EFEHAN KULU	25902023	OTOMATIK_GIRIS	0
294	2026-04-06	16:40:13	172.16.0.48	25904007	ERTÜMEN YAYLA	25904007	OTOMATIK_GIRIS	0
295	2026-04-06	16:40:13	172.16.0.14	25904043	HASAN BERK KOCA	25904043	OTOMATIK_GIRIS	0
296	2026-04-06	16:40:14	172.16.0.101	25901012	NİSA NUR ÇELİK	25901012	OTOMATIK_GIRIS	0
297	2026-04-06	16:40:14	172.16.0.43	25903002	İREM UYSAL	25903002	OTOMATIK_GIRIS	0
298	2026-04-06	16:40:14	172.16.0.56	25905018	EREN DUMRUL	25905018	OTOMATIK_GIRIS	0
299	2026-04-06	16:40:14	172.16.0.23	25901017	ÖMER YEŞİLYURT	25901017	OTOMATIK_GIRIS	0
300	2026-04-06	16:40:14	172.16.0.73	25902020	DOĞUKAN DURAN	25902020	OTOMATIK_GIRIS	0
301	2026-04-06	16:40:14	172.16.0.118	25903005	IŞIL KORKMAZ	25903005	OTOMATIK_GIRIS	0
302	2026-04-06	16:40:14	172.16.0.54	25905017	MEHMET ARDA YENENER	25905017	OTOMATIK_GIRIS	0
303	2026-04-06	16:40:14	172.16.0.55	25905027	İNCİ HALICI	25905027	OTOMATIK_GIRIS	0
304	2026-04-06	16:40:14	172.16.0.84	25901013	BUSENUR ALTAN	25901013	OTOMATIK_GIRIS	0
305	2026-04-06	16:40:14	172.16.0.108	25903008	HATİCE ÖZLÜ	25903008	OTOMATIK_GIRIS	0
306	2026-04-06	16:40:14	172.16.0.78	25903014	RANA BEDRİYE DAĞTEKİN	25903014	OTOMATIK_GIRIS	0
307	2026-04-06	16:40:14	172.16.0.74	25901018	ZEHRA YILDIRIM	25901018	OTOMATIK_GIRIS	0
308	2026-04-06	16:40:14	172.16.0.11	25902021	ESRA BAYRAM	25902021	OTOMATIK_GIRIS	0
309	2026-04-06	16:40:14	172.16.0.26	25904031	SELAHATTİN EFE SORGUN	25904031	OTOMATIK_GIRIS	0
310	2026-04-06	16:40:14	172.16.0.104	25902024	EFEHAN EKINCI	25902024	OTOMATIK_GIRIS	0
311	2026-04-06	16:40:14	172.16.0.126	25904037	MUHAMMED EFENDİ AYHANOĞLU	25904037	OTOMATIK_GIRIS	0
312	2026-04-06	16:40:26	172.16.0.39	25904022	MEHMET KAYRA AKKUŞ	25904022	OTOMATIK_GIRIS	0
313	2026-04-06	16:40:29	172.16.0.41	25904004	SÜLEYMAN ESER DİNÇ	25904004	OTOMATIK_GIRIS	0
314	2026-04-06	16:40:42	172.16.0.85	25905028	YASİN BOLAT	25905028	OTOMATIK_GIRIS	0
315	2026-04-06	16:40:44	172.16.0.63	25905024	RÜZGAR KAYA	25905024	OTOMATIK_GIRIS	0
316	2026-04-12	20:11:26	167.82.4.223	123	TEST TEST	123	OTOMATIK_GIRIS	0
317	2026-04-12	20:42:23	167.82.4.223	123	TEST TEST	123	OTOMATIK_GIRIS	0
\.


--
-- Data for Name: yardim_talepleri; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.yardim_talepleri (id, tarih, saat, numara, ad_soyad, durum, kategori) FROM stdin;
\.


--
-- Data for Name: yoklama; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.yoklama (id, tarih, ad_soyad, numara, saat, sinif, paket, ip, kaynak) FROM stdin;
16	2026-03-02	TEST TEST	123	09:51:31	TEST	1. Paket (09:00-11:35)	127.0.0.1	web
17	2026-03-02	SALİH BİLAL KORKMAZ	25901005	09:55:25	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.7	web
18	2026-03-02	BEHİÇ ARDA DEMİRER	25901002	09:56:08	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.61	web
19	2026-03-02	MUSTAFA ŞAHİN	25902013	10:00:11	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.36	web
20	2026-03-02	YUNUS EGE MÖNÜR	25905015	10:00:44	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.112	web
21	2026-03-02	BUSENUR ALTAN	25901013	10:00:47	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.118	web
22	2026-03-02	MUHAMMED HAKTAN SAZÇALAN	25903012	10:03:00	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	manuel	manuel
23	2026-03-02	MUSTAFA AVCI	25905004	10:03:09	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
24	2026-03-02	RECEP FURKAN ÇELİK	25905006	10:03:24	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
25	2026-03-02	ÖMER YEŞİLYURT	25901017	10:42:43	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.63	web
26	2026-03-02	ZEHRA YILDIRIM	25901018	10:45:56	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.21	web
27	2026-03-02	FAHRİ ARDA KARATAŞ	25902012	10:52:56	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.101	web
28	2026-03-02	ERKAM SONUÇ	25905012	10:53:13	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.178	web
29	2026-03-02	ARİF SEVBAN KIRIT	25902003	10:53:49	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.43	web
30	2026-03-02	MEHMET ARDA YENENER	25905017	10:54:10	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.120	web
31	2026-03-02	RÜZGAR KAYA	25905024	11:23:31	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
32	2026-03-02	BERAT ALİ ERİŞ	25905020	11:24:44	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
33	2026-03-02	DİLEK KARAÇE	25905003	11:25:12	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
34	2026-03-02	FATMA RANA GÖKDEMİR	25905008	11:25:21	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
35	2026-03-02	TUANNA ALTIN	25905002	11:25:34	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
36	2026-03-02	AHMET TAYLAN ERDEN	25904014	11:25:47	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	manuel	manuel
37	2026-03-02	ESMANUR DİNÇER	25903006	11:26:26	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	manuel	manuel
38	2026-03-02	EFEKAN İÇÖZ	25901011	11:26:41	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	manuel	manuel
39	2026-03-02	GÖKTUĞ ERDEM PEHLİVAN	25904035	11:27:17	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	manuel	manuel
40	2026-03-02	ONUR YENİPAZARLI	25904026	11:27:29	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	manuel	manuel
41	2026-03-02	EREN GÜLER	25901006	11:30:07	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	manuel	manuel
42	2026-03-02	ATA ÇAĞAN KESKİN	25905013	11:31:20	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
43	2026-03-02	İSMET HALİT DEMİRCİ	25904041	11:31:45	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	manuel	manuel
44	2026-03-02	HASAN ARDA TAHTACI	25904023	11:32:05	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	manuel	manuel
45	2026-03-02	DOĞUKAN DURAN	25902020	11:32:20	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	manuel	manuel
46	2026-03-02	EZGİ YILDIZ	25901008	11:32:59	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	manuel	manuel
47	2026-03-02	FURKAN SAFA ÇÜRÜTTÜ	25901003	11:33:13	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	manuel	manuel
48	2026-03-02	NİSA NUR ÇELİK	25901012	11:33:42	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	manuel	manuel
49	2026-03-02	MUSTAFA ÇETİN	25902008	11:33:53	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	manuel	manuel
50	2026-03-02	İLKAY ŞIK	25902001	11:34:04	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	manuel	manuel
51	2026-03-02	EYLÜL KAYA	25902004	11:34:25	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	manuel	manuel
52	2026-03-02	ESRA BAYRAM	25902021	11:34:34	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	manuel	manuel
53	2026-03-02	SUDE ELMAS AYKIRI	25904005	11:34:47	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	manuel	manuel
54	2026-03-02	SEFA YUSUF KÜTÜK	25905007	11:36:00	Yazılım Geliştirme	—	manuel	manuel
55	2026-03-02	ENES ÖZTÜRK	25902002	11:36:47	Bilişim Sistemleri ve Teknolojileri	—	manuel	manuel
56	2026-03-02	ARDA KARATAŞ	25901007	11:36:59	Bilgi Güvenliği Teknolojisi	—	manuel	manuel
57	2026-03-02	EREN DUMRUL	25905018	11:37:09	Yazılım Geliştirme	—	manuel	manuel
58	2026-03-02	VEYSEL KAAN DÜMAN	25905009	11:37:20	Yazılım Geliştirme	—	manuel	manuel
59	2026-03-02	BAHRİ AYDOĞDU	25905016	11:37:30	Yazılım Geliştirme	—	manuel	manuel
60	2026-03-02	EFZA KAÇMAZ	25904029	11:37:42	Yapay Zeka ve Makine Öğrenmesi	—	manuel	manuel
61	2026-03-02	ZEHRA ÇALIK	25904008	11:37:57	Yapay Zeka ve Makine Öğrenmesi	—	manuel	manuel
62	2026-03-02	ALMILA FATMA ÖZER	25904020	11:38:11	Yapay Zeka ve Makine Öğrenmesi	—	manuel	manuel
63	2026-03-02	ALPEREN DURKUT	25901004	11:38:24	Bilgi Güvenliği Teknolojisi	—	manuel	manuel
64	2026-03-02	AYBÜKE TERCAN	25904009	13:02:51	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.179	web
65	2026-03-02	ZEREN NEBİOĞLU	25904036	13:11:28	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.39	web
66	2026-03-02	MİRAY KAMİLE TİRAŞ	25903004	13:12:04	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.72	web
67	2026-03-02	AYŞE DEMİRKAYA	25904030	13:14:31	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.108	web
79	2026-03-09	ALPEREN DURKUT	25901004	10:15:16	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.139	web
80	2026-03-09	VEYSEL KAAN DÜMAN	25905009	10:15:42	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.36	web
81	2026-03-09	ENES ÖZTÜRK	25902002	10:15:43	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.178	web
82	2026-03-09	ATA ÇAĞAN KESKİN	25905013	10:16:25	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.72	web
83	2026-03-09	EREN DUMRUL	25905018	10:16:30	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.39	web
84	2026-03-09	FURKAN SAFA ÇÜRÜTTÜ	25901003	10:16:38	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.20	web
85	2026-03-09	ARDA KARATAŞ	25901007	10:17:06	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.114	web
86	2026-03-09	EFEKAN İÇÖZ	25901011	10:17:32	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.26	web
87	2026-03-09	MEHMET CAN ERŞEN	25902007	10:18:04	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.101	web
88	2026-03-09	ARİF SEVBAN KIRIT	25902003	10:18:29	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.43	web
89	2026-03-09	ESMANUR DİNÇER	25903006	10:19:49	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.107	web
90	2026-03-09	EFZA KAÇMAZ	25904029	10:19:52	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.125	web
91	2026-03-09	KAZIM EFE TAŞDEMİR	25901010	10:19:55	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.126	web
92	2026-03-09	MUZAFFER TAHA GÜL	25901016	10:20:03	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.25	web
93	2026-03-09	AGAH ABDULLAH SARSILMAZ	25904032	10:20:47	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.13	web
94	2026-03-09	YASİN BOLAT	25905028	10:21:03	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.9	web
95	2026-03-09	FURKAN İLİK	25904011	10:21:22	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.11	web
96	2026-03-09	SÜLEYMAN ESER DİNÇ	25904004	10:21:30	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.23	web
97	2026-03-09	SAFA HASOĞLU	25904017	10:21:31	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.63	web
98	2026-03-09	SUDE ELMAS AYKIRI	25904005	10:21:40	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.177	web
99	2026-03-09	EFEHAN KULU	25902023	10:22:24	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.100	web
100	2026-03-09	SEFA YUSUF KÜTÜK	25905007	10:23:03	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.104	web
101	2026-03-09	AHMET BAŞOĞLU	25905001	10:23:08	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.19	web
102	2026-03-09	TUANNA ALTIN	25905002	10:25:55	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.182	web
103	2026-03-09	FATMA RANA GÖKDEMİR	25905008	10:26:11	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.179	web
104	2026-03-09	SEVİM ÇELİK	25903015	10:27:36	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.38	web
105	2026-03-09	BERAT ALİ ERİŞ	25905020	11:17:40	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.118	web
106	2026-03-09	BAHRİ AYDOĞDU	25905016	11:20:54	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.113	web
107	2026-03-09	BEHİÇ ARDA DEMİRER	25901002	11:25:12	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.29	web
108	2026-03-09	TEST2 TEST2	124	11:48:48	TEST	—	172.16.0.14	web
109	2026-03-09	TEST TEST	123	11:52:16	TEST	—	manuel	manuel
110	2026-03-09	RESUL EKREM ÖZCAN	25902009	12:50:33	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.72	web
111	2026-03-09	FAHRİ ARDA KARATAŞ	25902012	12:50:41	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.43	web
112	2026-03-09	MUSTAFA ÇETİN	25902008	12:50:41	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.19	web
113	2026-03-09	AHMET FARUK YÜKSEL	25902010	12:50:53	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.9	web
114	2026-03-09	KAMURAN İNAN AYDOĞAN	25905011	12:50:53	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.101	web
115	2026-03-09	ERKAM SONUÇ	25905012	12:51:33	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.20	web
116	2026-03-09	MUSTAFA ŞAHİN	25902013	12:51:44	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.39	web
117	2026-03-09	AHMET MAHLİ	25903001	12:52:33	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.177	web
118	2026-03-09	EZGİ YILDIZ	25901008	12:52:48	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.25	web
119	2026-03-09	AZRA ŞAHİN	25903010	12:53:07	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.125	web
120	2026-03-09	YUSUF ŞAHBAZ	25904027	12:53:21	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.182	web
121	2026-03-09	TARIK BUĞRA BODUR	25902017	12:55:57	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.126	web
122	2026-03-09	AYŞE DEMİRKAYA	25904030	12:55:59	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.178	web
123	2026-03-09	BÜŞRA SENA MUTLU	25903003	12:57:31	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.107	web
124	2026-03-09	YUSUF ENES BİLGİN	25904019	12:57:31	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.108	web
125	2026-03-09	MEHMET EREN BODUROĞLU	25904012	12:58:10	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.118	web
126	2026-03-09	YAVUZ SELİM SEZER	25904018	12:59:10	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.113	web
127	2026-03-09	SUDE ÖZTÜRK	25904024	12:59:16	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.112	web
128	2026-03-09	ALMILA FATMA ÖZER	25904020	13:21:47	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.45	web
129	2026-03-09	ZEREN NEBİOĞLU	25904036	13:22:56	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.139	web
130	2026-03-09	MİRAY KAMİLE TİRAŞ	25903004	13:25:08	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.29	web
131	2026-03-09	CEMRE SU GENÇ	25903009	13:25:47	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.47	web
132	2026-03-09	SALİH BİLAL KORKMAZ	25901005	13:46:43	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	manuel	manuel
133	2026-03-09	AMINJON PRIMOV	24090901	13:48:53	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	manuel	manuel
134	2026-03-09	EREN GÜLER	25901006	13:49:17	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	manuel	manuel
135	2026-03-09	MUSTAFA AVCI	25905004	13:49:24	Yazılım Geliştirme	2. Paket (12:40-15:15)	manuel	manuel
136	2026-03-09	RECEP FURKAN ÇELİK	25905006	13:49:31	Yazılım Geliştirme	2. Paket (12:40-15:15)	manuel	manuel
137	2026-03-09	ABDELRAHMAN KHALIL	24118904	13:51:06	Yazılım Geliştirme	2. Paket (12:40-15:15)	manuel	manuel
138	2026-03-09	İNCİ HALICI	25905027	13:52:30	Yazılım Geliştirme	2. Paket (12:40-15:15)	manuel	manuel
139	2026-03-09	DİLEK KARAÇE	25905003	13:53:02	Yazılım Geliştirme	2. Paket (12:40-15:15)	manuel	manuel
140	2026-03-09	YUNUS EGE MÖNÜR	25905015	13:53:19	Yazılım Geliştirme	2. Paket (12:40-15:15)	manuel	manuel
141	2026-03-09	EFEHAN EKINCI	25902024	14:00:37	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	manuel	manuel
142	2026-03-09	SEMİH ÇELİKEL	25903011	14:01:07	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.61	web
143	2026-03-09	BUSENUR ALTAN	25901013	14:01:39	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.100	web
144	2026-03-09	AHMET MERT KÖYBAŞI	25903013	14:02:44	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.121	web
145	2026-03-09	EFE BARAN DEMIRHAN	24090003	14:03:21	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	manuel	manuel
146	2026-03-09	ÖMER YEŞİLYURT	25901017	15:39:58	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.177	web
147	2026-03-09	MUHAMMED EFENDİ AYHANOĞLU	25904037	15:40:16	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.20	web
148	2026-03-09	ESRA BAYRAM	25902021	15:40:47	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.107	web
149	2026-03-09	ZEHRA YILDIRIM	25901018	15:41:06	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.125	web
150	2026-03-09	DOĞUKAN DURAN	25902020	15:41:14	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.108	web
151	2026-03-09	SÜLEYMAN ESER DİNÇ	25904004	15:41:40	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.101	web
152	2026-03-09	MEHMET ARDA YENENER	25905017	15:42:04	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.47	web
153	2026-03-09	ERTÜMEN YAYLA	25904007	15:42:08	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.43	web
154	2026-03-09	MEHMET KAYRA AKKUŞ	25904022	15:42:42	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.39	web
155	2026-03-09	BURAK AYYILDIZ	25902025	15:43:04	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.118	web
156	2026-03-09	İREM UYSAL	25903002	15:43:51	Veri Bilimi ve Analitiği	3. Paket (15:25-18:00)	172.16.0.178	web
157	2026-03-09	HASAN BERK KOCA	25904043	15:45:42	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.139	web
158	2026-03-09	EMİRHAN ESENOĞLU	25904010	15:45:45	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.114	web
159	2026-03-09	ALAATTİN EFE YURTERİ	25904001	15:45:49	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.72	web
160	2026-03-09	NİSA NUR ÇELİK	25901012	15:45:51	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.38	web
161	2026-03-09	MEHMET ENES KAYA	25904016	15:46:43	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.120	web
165	2026-03-30	ESMANUR DİNÇER	25903006	09:08:44	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.179	web
166	2026-03-30	ARDA KARATAŞ	25901007	09:08:47	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.114	web
167	2026-03-30	BEHİÇ ARDA DEMİRER	25901002	09:08:49	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.39	web
168	2026-03-30	SAHRA GÜNDOĞDU	25904033	09:08:49	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.125	web
169	2026-03-30	ENES ÖZTÜRK	25902002	09:08:56	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.70	web
170	2026-03-30	ALPEREN DURKUT	25901004	09:08:58	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.139	web
171	2026-03-30	SALİH GÖKAY KÖKSAL	25904002	09:09:00	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.66	web
172	2026-03-30	SEFA YUSUF KÜTÜK	25905007	09:09:02	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.44	web
173	2026-03-30	EREN GÜLER	25901006	09:09:05	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.61	web
174	2026-03-30	MUHAMMED HAKTAN SAZÇALAN	25903012	09:09:07	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.63	web
175	2026-03-30	ONUR YENİPAZARLI	25904026	09:09:08	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.72	web
176	2026-03-30	FURKAN İLİK	25904011	09:09:08	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.101	web
177	2026-03-30	İREM GENEŞ	25904006	09:09:10	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.107	web
178	2026-03-30	SEVİM ÇELİK	25903015	09:09:15	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.41	web
179	2026-03-30	SUDE ELMAS AYKIRI	25904005	09:09:17	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.177	web
180	2026-03-30	AGAH ABDULLAH SARSILMAZ	25904032	09:09:19	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.84	web
181	2026-03-30	YUNUS EMRE KARAKEÇİLİ	25904038	09:09:19	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.56	web
182	2026-03-30	HASAN ARDA TAHTACI	25904023	09:09:20	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.118	web
183	2026-03-30	EFEKAN İÇÖZ	25901011	09:09:22	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.26	web
184	2026-03-30	DİLEK KARAÇE	25905003	09:09:26	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.120	web
185	2026-03-30	SÜHEYLA TUĞÇE GÜN	25904003	09:09:28	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.43	web
186	2026-03-30	ZEHRA ÇALIK	25904008	09:09:37	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.126	web
187	2026-03-30	YUNUS EGE MÖNÜR	25905015	09:09:38	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.85	web
188	2026-03-30	GÖKTUĞ ERDEM PEHLİVAN	25904035	09:09:45	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.57	web
189	2026-03-30	SALİH BİLAL KORKMAZ	25901005	09:09:46	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.10	web
190	2026-03-30	EFE BARAN DEMIRHAN	24090003	09:09:48	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.14	web
191	2026-03-30	VEYSEL KAAN DÜMAN	25905009	09:09:58	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.62	web
192	2026-03-30	İLKAY ŞIK	25902001	09:09:59	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.47	web
193	2026-03-30	BAHRİ AYDOĞDU	25905016	09:10:25	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.100	web
194	2026-03-30	FURKAN SAFA ÇÜRÜTTÜ	25901003	09:10:48	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.23	web
195	2026-03-30	MEHMET CAN ERŞEN	25902007	09:11:38	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.4	web
196	2026-03-30	AHMET BAŞOĞLU	25905001	09:11:52	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.104	web
197	2026-03-30	İSMET HALİT DEMİRCİ	25904041	09:12:17	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.108	web
198	2026-03-30	EYLÜL KAYA	25902004	09:12:41	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.112	web
199	2026-03-30	ISMAIL KAAN YÜKSEKER	25905022	09:14:27	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.42	web
200	2026-03-30	ARİF SEVBAN KIRIT	25902003	09:14:47	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	manuel	manuel
201	2026-03-30	RECEP FURKAN ÇELİK	25905006	09:14:58	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
202	2026-03-30	KAMURAN İNAN AYDOĞAN	25905011	09:16:13	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.113	web
203	2026-03-30	KAZIM EFE TAŞDEMİR	25901010	09:17:41	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.10	web
204	2026-03-30	EFZA KAÇMAZ	25904029	09:17:54	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.126	web
205	2026-03-30	ABDELRAHMAN KHALIL	24118904	09:49:43	Yazılım Geliştirme	1. Paket (09:00-11:35)	manuel	manuel
206	2026-03-30	BÜŞRA SENA MUTLU	25903003	09:50:30	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	manuel	manuel
207	2026-03-30	TUANNA ALTIN	25905002	12:40:51	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.125	web
208	2026-03-30	ÖYKÜM NİLDENİZ AKPINAR	25904025	12:40:51	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.104	web
209	2026-03-30	İNCİ HALICI	25905027	12:41:06	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.43	web
210	2026-03-30	FAHRİ ARDA KARATAŞ	25902012	12:41:09	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.57	web
211	2026-03-30	ZÜBEYİR CUMA YILMAZ	25902014	12:49:02	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.62	web
212	2026-03-30	ERKAM SONUÇ	25905012	12:49:02	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.114	web
213	2026-03-30	MİRAY KAMİLE TİRAŞ	25903004	12:49:02	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.139	web
214	2026-03-30	ATA ÇAĞAN KESKİN	25905013	12:49:02	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.107	web
215	2026-03-30	ÖMER FARUK GÖKSU	25904039	12:49:05	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.42	web
216	2026-03-30	MUZAFFER TAHA GÜL	25901016	12:49:06	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.85	web
217	2026-03-30	YAVUZ SELİM SEZER	25904018	12:49:08	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.100	web
218	2026-03-30	MUSTAFA ÇETİN	25902008	12:49:10	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.56	web
219	2026-03-30	NİSA NUR ÇELİK	25901012	12:49:11	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.26	web
220	2026-03-30	BUSENUR ALTAN	25901013	12:49:12	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.126	web
221	2026-03-30	SAFA HASOĞLU	25904017	12:49:12	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.118	web
222	2026-03-30	EREN DUMRUL	25905018	12:49:12	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.23	web
223	2026-03-30	MUSTAFA ŞAHİN	25902013	12:49:14	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.101	web
224	2026-03-30	AHMET TAYLAN ERDEN	25904014	12:49:15	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.44	web
225	2026-03-30	TUĞBA GÜLMEZ	25903007	12:49:16	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.112	web
226	2026-03-30	YUSUF ENES BİLGİN	25904019	12:49:17	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.108	web
227	2026-03-30	EZGİ YILDIZ	25901008	12:49:19	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.14	web
228	2026-03-30	ESRA BAYRAM	25902021	12:49:21	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.4	web
229	2026-03-30	EMİRHAN ESENOĞLU	25904010	12:49:23	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.66	web
230	2026-03-30	AHMET MAHLİ	25903001	12:49:27	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.47	web
231	2026-03-30	MEHMET EREN BODUROĞLU	25904012	12:49:28	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.72	web
232	2026-03-30	HATİCE ÖZLÜ	25903008	12:49:29	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.120	web
233	2026-03-30	RESUL EKREM ÖZCAN	25902009	12:49:29	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.84	web
234	2026-03-30	FATMA RANA GÖKDEMİR	25905008	12:49:31	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.177	web
235	2026-03-30	SEMİH ÇELİKEL	25903011	12:49:36	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.63	web
236	2026-03-30	AZRA ŞAHİN	25903010	12:49:55	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.39	web
237	2026-03-30	YUSUF ŞAHBAZ	25904027	12:49:58	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.182	web
238	2026-03-30	AHMET MERT KÖYBAŞI	25903013	12:50:02	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.41	web
239	2026-03-30	AYŞE DEMİRKAYA	25904030	13:04:28	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.70	web
240	2026-03-30	İREM UYSAL	25903002	13:04:44	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.61	web
241	2026-03-30	ÖMER YILDIZ	25904021	13:04:52	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.104	web
242	2026-03-30	EFEHAN EKINCI	25902024	13:07:46	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.179	web
243	2026-03-30	AHMET FARUK YÜKSEL	25902010	13:20:56	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.126	web
244	2026-03-30	RANA BEDRİYE DAĞTEKİN	25903014	13:58:05	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	manuel	manuel
245	2026-03-30	SALIH DEMIRTAŞ	25904401	14:15:33	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.85	web
246	2026-03-30	BURAK AYYILDIZ	25902025	14:33:52	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.121	web
247	2026-03-30	TARIK BUĞRA BODUR	25902017	15:17:30	Bilişim Sistemleri ve Teknolojileri	—	172.16.0.44	web
248	2026-03-30	CEMRE SU GENÇ	25903009	15:36:14	Veri Bilimi ve Analitiği	3. Paket (15:25-18:00)	172.16.0.120	web
249	2026-03-30	DOĞUKAN DURAN	25902020	15:36:30	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.121	web
250	2026-03-30	ÖMER YEŞİLYURT	25901017	15:36:32	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.63	web
251	2026-03-30	ERTÜMEN YAYLA	25904007	15:36:43	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.104	web
252	2026-03-30	ZEHRA YILDIRIM	25901018	15:37:39	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.41	web
253	2026-03-30	BERAT ALİ ERİŞ	25905020	15:37:45	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.42	web
254	2026-03-30	SÜLEYMAN ESER DİNÇ	25904004	15:38:03	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.118	web
255	2026-03-30	EFEHAN KULU	25902023	15:38:52	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.4	web
256	2026-03-30	YASİN BOLAT	25905028	15:39:01	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.14	web
257	2026-03-30	MEHMET KAYRA AKKUŞ	25904022	15:39:27	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.113	web
258	2026-03-30	MEHMET ARDA YENENER	25905017	15:44:59	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.62	web
259	2026-03-30	SAMI KARACA	25146901	15:46:38	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.139	web
260	2026-03-30	MEHMET ENES KAYA	25904016	15:48:56	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.179	web
261	2026-03-30	ALAATTİN EFE YURTERİ	25904001	15:51:09	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.182	web
262	2026-03-30	HASAN BERK KOCA	25904043	15:53:49	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.84	web
263	2026-03-30	BÜNYAMİN EFE BULUT	25904028	15:58:45	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.57	web
264	2026-03-30	ALMILA FATMA ÖZER	25904020	15:59:45	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.121	web
265	2026-03-30	MUHAMMED EFENDİ AYHANOĞLU	25904037	15:59:59	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.72	web
266	2026-03-30	SUDE ÖZTÜRK	25904024	16:02:52	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.39	web
267	2026-03-30	ZEREN NEBİOĞLU	25904036	16:08:49	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.41	web
268	2026-04-01	TEST TEST	123	16:10:59	TEST	3. Paket (15:25-18:00)	127.0.0.1	web
326	2026-04-02	ÖĞRENCI-1 TEST	test1	23:12:17	Test Sınıfı (5 Kişi)	—	192.168.111.53	web
327	2026-04-02	ÖĞRENCI-2 TEST	test2	23:13:52	Test Sınıfı (5 Kişi)	—	192.168.111.53	web
328	2026-04-03	ÖĞRENCI-1 TEST	test1	00:00:12	Test Sınıfı (5 Kişi)	—	127.0.0.1	web
329	2026-04-06	EFE BARAN DEMIRHAN	24090003	09:19:58	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.78	web
330	2026-04-06	SALİH GÖKAY KÖKSAL	25904002	09:20:16	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.113	web
331	2026-04-06	GÖKTUĞ ERDEM PEHLİVAN	25904035	09:20:18	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.104	web
332	2026-04-06	FURKAN İLİK	25904011	09:20:53	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.118	web
333	2026-04-06	AMINJON PRIMOV	24090901	09:21:09	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.61	web
334	2026-04-06	SALİH BİLAL KORKMAZ	25901005	09:21:17	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.13	web
335	2026-04-06	SAFA HASOĞLU	25904017	09:21:18	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.75	web
336	2026-04-06	BEHİÇ ARDA DEMİRER	25901002	09:21:21	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.48	web
337	2026-04-06	İSMET HALİT DEMİRCİ	25904041	09:21:22	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.11	web
338	2026-04-06	ENES ÖZTÜRK	25902002	09:21:23	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.114	web
339	2026-04-06	HASAN ARDA TAHTACI	25904023	09:21:23	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.73	web
340	2026-04-06	ALPEREN DURKUT	25901004	09:21:27	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.41	web
341	2026-04-06	AGAH ABDULLAH SARSILMAZ	25904032	09:21:35	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.139	web
342	2026-04-06	YUNUS EMRE KARAKEÇİLİ	25904038	09:21:44	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.54	web
343	2026-04-06	ESMANUR DİNÇER	25903006	09:21:47	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.56	web
344	2026-04-06	SAHRA GÜNDOĞDU	25904033	09:21:50	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.125	web
345	2026-04-06	ZEHRA ÇALIK	25904008	09:21:52	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.84	web
346	2026-04-06	FATMA RANA GÖKDEMİR	25905008	09:22:05	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.43	web
347	2026-04-06	ARİF SEVBAN KIRIT	25902003	09:22:09	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.74	web
348	2026-04-06	MUHAMMED HAKTAN SAZÇALAN	25903012	09:22:09	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.63	web
349	2026-04-06	CEMRE SU GENÇ	25903009	09:46:24	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.85	web
350	2026-04-06	AHMET TAYLAN ERDEN	25904014	09:46:31	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.14	web
351	2026-04-06	RECEP FURKAN ÇELİK	25905006	09:46:40	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.108	web
352	2026-04-06	BÜŞRA SENA MUTLU	25903003	09:46:49	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.39	web
353	2026-04-06	SUDE ELMAS AYKIRI	25904005	09:46:55	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.177	web
354	2026-04-06	DİLEK KARAÇE	25905003	09:47:26	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.107	web
355	2026-04-06	EFZA KAÇMAZ	25904029	09:47:58	Yapay Zeka ve Makine Öğrenmesi	1. Paket (09:00-11:35)	172.16.0.101	web
356	2026-04-06	AHMET BAŞOĞLU	25905001	09:48:00	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.108	web
357	2026-04-06	SEVİM ÇELİK	25903015	09:50:29	Veri Bilimi ve Analitiği	1. Paket (09:00-11:35)	172.16.0.100	web
358	2026-04-06	EYLÜL KAYA	25902004	09:51:04	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.112	web
359	2026-04-06	ABDELRAHMAN KHALIL	24118904	09:51:07	Yazılım Geliştirme	1. Paket (09:00-11:35)	172.16.0.120	web
360	2026-04-06	FURKAN SAFA ÇÜRÜTTÜ	25901003	09:53:55	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.23	web
361	2026-04-06	MEHMET CAN ERŞEN	25902007	09:54:00	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.26	web
362	2026-04-06	EFEKAN İÇÖZ	25901011	09:54:39	Bilgi Güvenliği Teknolojisi	1. Paket (09:00-11:35)	172.16.0.126	web
363	2026-04-06	İLKAY ŞIK	25902001	10:25:03	Bilişim Sistemleri ve Teknolojileri	1. Paket (09:00-11:35)	172.16.0.179	web
364	2026-04-06	MİRAY KAMİLE TİRAŞ	25903004	12:32:00	Veri Bilimi ve Analitiği	—	172.16.0.73	web
365	2026-04-06	MEHMET EREN BODUROĞLU	25904012	12:32:22	Yapay Zeka ve Makine Öğrenmesi	—	172.16.0.100	web
366	2026-04-06	ZEREN NEBİOĞLU	25904036	12:32:54	Yapay Zeka ve Makine Öğrenmesi	—	172.16.0.11	web
367	2026-04-06	TUĞBA GÜLMEZ	25903007	12:33:33	Veri Bilimi ve Analitiği	—	172.16.0.75	web
368	2026-04-06	ALMILA FATMA ÖZER	25904020	12:34:00	Yapay Zeka ve Makine Öğrenmesi	—	172.16.0.84	web
369	2026-04-06	YUSUF ŞAHBAZ	25904027	12:34:05	Yapay Zeka ve Makine Öğrenmesi	—	172.16.0.56	web
370	2026-04-06	SUDE ÖZTÜRK	25904024	12:34:23	Yapay Zeka ve Makine Öğrenmesi	—	172.16.0.101	web
371	2026-04-06	EZGİ YILDIZ	25901008	12:34:50	Bilgi Güvenliği Teknolojisi	—	172.16.0.43	web
372	2026-04-06	ÖMER YILDIZ	25904021	12:34:55	Yapay Zeka ve Makine Öğrenmesi	—	172.16.0.63	web
373	2026-04-06	AYBÜKE TERCAN	25904009	12:35:00	Yapay Zeka ve Makine Öğrenmesi	—	172.16.0.125	web
374	2026-04-06	AYŞE DEMİRKAYA	25904030	12:44:35	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.179	web
375	2026-04-06	YAVUZ SELİM SEZER	25904018	12:44:36	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.177	web
376	2026-04-06	FAHRİ ARDA KARATAŞ	25902012	12:49:37	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.26	web
377	2026-04-06	AZRA ŞAHİN	25903010	12:49:45	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.108	web
378	2026-04-06	ERKAM SONUÇ	25905012	12:49:56	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.139	web
379	2026-04-06	KAZIM EFE TAŞDEMİR	25901010	12:50:04	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.61	web
380	2026-04-06	ARDA KARATAŞ	25901007	12:50:05	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.41	web
381	2026-04-06	İREM GENEŞ	25904006	12:50:05	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.107	web
382	2026-04-06	AHMET MAHLİ	25903001	12:50:10	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.118	web
383	2026-04-06	VEYSEL KAAN DÜMAN	25905009	12:50:19	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.85	web
384	2026-04-06	KAMURAN İNAN AYDOĞAN	25905011	12:50:20	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.114	web
385	2026-04-06	MUSTAFA ŞAHİN	25902013	12:50:22	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.74	web
386	2026-04-06	ATA ÇAĞAN KESKİN	25905013	12:50:23	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.14	web
387	2026-04-06	AHMET MERT KÖYBAŞI	25903013	12:50:32	Veri Bilimi ve Analitiği	2. Paket (12:40-15:15)	172.16.0.182	web
388	2026-04-06	ZÜBEYİR CUMA YILMAZ	25902014	12:50:57	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.104	web
389	2026-04-06	EREN GÜLER	25901006	12:51:59	Bilgi Güvenliği Teknolojisi	2. Paket (12:40-15:15)	172.16.0.121	web
390	2026-04-06	MEHMET EREN BODUROĞLU	25904012	12:52:31	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.54	web
391	2026-04-06	AHMET FARUK YÜKSEL	25902010	12:53:34	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.78	web
392	2026-04-06	ÖMER FARUK GÖKSU	25904039	12:54:10	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	172.16.0.55	web
393	2026-04-06	MUSTAFA ÇETİN	25902008	12:58:05	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.23	web
394	2026-04-06	RESUL EKREM ÖZCAN	25902009	13:00:08	Bilişim Sistemleri ve Teknolojileri	2. Paket (12:40-15:15)	172.16.0.126	web
395	2026-04-06	SÜHEYLA TUĞÇE GÜN	25904003	13:37:52	Yapay Zeka ve Makine Öğrenmesi	2. Paket (12:40-15:15)	manuel	manuel
396	2026-04-06	YUNUS EGE MÖNÜR	25905015	13:57:28	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.100	web
397	2026-04-06	BAHRİ AYDOĞDU	25905016	14:36:59	Yazılım Geliştirme	2. Paket (12:40-15:15)	172.16.0.120	web
398	2026-04-06	TEST TEST	123	15:01:26	TEST	2. Paket (12:40-15:15)	127.0.0.1	web
399	2026-04-06	HASAN BERK KOCA	25904043	15:28:12	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.14	web
400	2026-04-06	BUSENUR ALTAN	25901013	15:28:27	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.84	web
401	2026-04-06	SELAHATTİN EFE SORGUN	25904031	15:28:28	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.26	web
402	2026-04-06	MUHAMMED EFENDİ AYHANOĞLU	25904037	15:28:29	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.126	web
403	2026-04-06	YUSUF ENES BİLGİN	25904019	15:28:38	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.177	web
404	2026-04-06	ZEHRA YILDIRIM	25901018	15:28:39	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.74	web
405	2026-04-06	İNCİ HALICI	25905027	15:28:40	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.55	web
406	2026-04-06	BÜNYAMİN EFE BULUT	25904028	15:28:41	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.107	web
407	2026-04-06	SEMİH ÇELİKEL	25903011	15:29:09	Veri Bilimi ve Analitiği	3. Paket (15:25-18:00)	172.16.0.125	web
408	2026-04-06	ÖMER YEŞİLYURT	25901017	15:29:16	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.23	web
409	2026-04-06	İREM UYSAL	25903002	15:29:35	Veri Bilimi ve Analitiği	3. Paket (15:25-18:00)	172.16.0.43	web
410	2026-04-06	MEHMET ARDA YENENER	25905017	15:29:57	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.54	web
411	2026-04-06	ESRA BAYRAM	25902021	15:30:23	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.11	web
412	2026-04-06	DOĞUKAN DURAN	25902020	15:30:25	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.73	web
413	2026-04-06	ERTÜMEN YAYLA	25904007	15:31:28	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.48	web
414	2026-04-06	MUZAFFER TAHA GÜL	25901016	15:32:10	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.101	web
415	2026-04-06	NİSA NUR ÇELİK	25901012	15:32:35	Bilgi Güvenliği Teknolojisi	3. Paket (15:25-18:00)	172.16.0.101	web
416	2026-04-06	TARIK BUĞRA BODUR	25902017	15:33:09	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.113	web
417	2026-04-06	EFEHAN EKINCI	25902024	15:33:15	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.104	web
418	2026-04-06	EREN DUMRUL	25905018	15:34:53	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.56	web
419	2026-04-06	IŞIL KORKMAZ	25903005	15:35:18	Veri Bilimi ve Analitiği	3. Paket (15:25-18:00)	172.16.0.118	web
420	2026-04-06	ÖYKÜM NİLDENİZ AKPINAR	25904025	15:35:43	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.75	web
421	2026-04-06	YASİN BOLAT	25905028	15:35:55	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.85	web
422	2026-04-06	EFEHAN KULU	25902023	15:36:33	Bilişim Sistemleri ve Teknolojileri	3. Paket (15:25-18:00)	172.16.0.100	web
423	2026-04-06	HATİCE ÖZLÜ	25903008	15:36:35	Veri Bilimi ve Analitiği	3. Paket (15:25-18:00)	172.16.0.108	web
424	2026-04-06	BERAT ALİ ERİŞ	25905020	15:36:52	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.63	web
425	2026-04-06	RÜZGAR KAYA	25905024	15:37:36	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.63	web
426	2026-04-06	RANA BEDRİYE DAĞTEKİN	25903014	15:39:58	Veri Bilimi ve Analitiği	3. Paket (15:25-18:00)	172.16.0.78	web
427	2026-04-06	MEHMET KAYRA AKKUŞ	25904022	15:48:06	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.39	web
428	2026-04-06	SÜLEYMAN ESER DİNÇ	25904004	15:48:23	Yapay Zeka ve Makine Öğrenmesi	3. Paket (15:25-18:00)	172.16.0.41	web
429	2026-04-06	TUĞRA TAŞ	25905019	15:49:13	Yazılım Geliştirme	3. Paket (15:25-18:00)	172.16.0.61	web
432	2026-04-12	TEST TEST	123	20:41:51	TEST	—	167.82.4.223	web
\.


--
-- Data for Name: yoklama_override; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.yoklama_override (id, numara, hafta, durum, tarih, ogretmen) FROM stdin;
\.


--
-- Name: ogrenci_aktivite_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ogrenci_aktivite_log_id_seq', 1, true);


--
-- Name: ogrenci_cevaplari_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ogrenci_cevaplari_id_seq', 263, true);


--
-- Name: ogrenci_cikis_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ogrenci_cikis_log_id_seq', 116, true);


--
-- Name: ogrenciler_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ogrenciler_id_seq', 167, true);


--
-- Name: ogrenme_ciktilari_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ogrenme_ciktilari_id_seq', 34, true);


--
-- Name: sahte_giris_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sahte_giris_log_id_seq', 35, true);


--
-- Name: seb_cikis_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seb_cikis_log_id_seq', 202, true);


--
-- Name: seb_cikis_talepleri_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seb_cikis_talepleri_id_seq', 31, true);


--
-- Name: secenekler_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.secenekler_id_seq', 128, true);


--
-- Name: sinav_ihlaller_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sinav_ihlaller_id_seq', 5, true);


--
-- Name: sinavlar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sinavlar_id_seq', 16, true);


--
-- Name: siniflar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.siniflar_id_seq', 10, true);


--
-- Name: soru_cikti_iliskisi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.soru_cikti_iliskisi_id_seq', 65, true);


--
-- Name: sorular_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sorular_id_seq', 58, true);


--
-- Name: terminal_guvenlik_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.terminal_guvenlik_log_id_seq', 317, true);


--
-- Name: yardim_talepleri_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.yardim_talepleri_id_seq', 1, true);


--
-- Name: yoklama_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.yoklama_id_seq', 432, true);


--
-- Name: yoklama_override_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.yoklama_override_id_seq', 1, true);


--
-- Name: ayarlar ayarlar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ayarlar
    ADD CONSTRAINT ayarlar_pkey PRIMARY KEY (anahtar);


--
-- Name: ogrenci_aktivite_log ogrenci_aktivite_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenci_aktivite_log
    ADD CONSTRAINT ogrenci_aktivite_log_pkey PRIMARY KEY (id);


--
-- Name: ogrenci_cevaplari ogrenci_cevaplari_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenci_cevaplari
    ADD CONSTRAINT ogrenci_cevaplari_pkey PRIMARY KEY (id);


--
-- Name: ogrenci_cikis_log ogrenci_cikis_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenci_cikis_log
    ADD CONSTRAINT ogrenci_cikis_log_pkey PRIMARY KEY (id);


--
-- Name: ogrenciler ogrenciler_numara_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenciler
    ADD CONSTRAINT ogrenciler_numara_key UNIQUE (numara);


--
-- Name: ogrenciler ogrenciler_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenciler
    ADD CONSTRAINT ogrenciler_pkey PRIMARY KEY (id);


--
-- Name: ogrenme_ciktilari ogrenme_ciktilari_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ogrenme_ciktilari
    ADD CONSTRAINT ogrenme_ciktilari_pkey PRIMARY KEY (id);


--
-- Name: sahte_giris_log sahte_giris_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sahte_giris_log
    ADD CONSTRAINT sahte_giris_log_pkey PRIMARY KEY (id);


--
-- Name: seb_cikis_log seb_cikis_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seb_cikis_log
    ADD CONSTRAINT seb_cikis_log_pkey PRIMARY KEY (id);


--
-- Name: seb_cikis_talepleri seb_cikis_talepleri_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seb_cikis_talepleri
    ADD CONSTRAINT seb_cikis_talepleri_pkey PRIMARY KEY (id);


--
-- Name: secenekler secenekler_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.secenekler
    ADD CONSTRAINT secenekler_pkey PRIMARY KEY (id);


--
-- Name: sinav_ihlaller sinav_ihlaller_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sinav_ihlaller
    ADD CONSTRAINT sinav_ihlaller_pkey PRIMARY KEY (id);


--
-- Name: sinavlar sinavlar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sinavlar
    ADD CONSTRAINT sinavlar_pkey PRIMARY KEY (id);


--
-- Name: siniflar siniflar_ad_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.siniflar
    ADD CONSTRAINT siniflar_ad_key UNIQUE (ad);


--
-- Name: siniflar siniflar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.siniflar
    ADD CONSTRAINT siniflar_pkey PRIMARY KEY (id);


--
-- Name: soru_cikti_iliskisi soru_cikti_iliskisi_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soru_cikti_iliskisi
    ADD CONSTRAINT soru_cikti_iliskisi_pkey PRIMARY KEY (id);


--
-- Name: sorular sorular_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sorular
    ADD CONSTRAINT sorular_pkey PRIMARY KEY (id);


--
-- Name: terminal_guvenlik_log terminal_guvenlik_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.terminal_guvenlik_log
    ADD CONSTRAINT terminal_guvenlik_log_pkey PRIMARY KEY (id);


--
-- Name: yardim_talepleri yardim_talepleri_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.yardim_talepleri
    ADD CONSTRAINT yardim_talepleri_pkey PRIMARY KEY (id);


--
-- Name: yoklama_override yoklama_override_numara_hafta_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.yoklama_override
    ADD CONSTRAINT yoklama_override_numara_hafta_key UNIQUE (numara, hafta);


--
-- Name: yoklama_override yoklama_override_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.yoklama_override
    ADD CONSTRAINT yoklama_override_pkey PRIMARY KEY (id);


--
-- Name: yoklama yoklama_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.yoklama
    ADD CONSTRAINT yoklama_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict yqCWc2ZmUZPSyUb6pd2H2mQ2gdySlBVVDujICwFFBJOOaRkF06pfQMo0sDwyFdU

