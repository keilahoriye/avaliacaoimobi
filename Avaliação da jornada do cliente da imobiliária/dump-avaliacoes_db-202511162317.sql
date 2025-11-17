--
-- PostgreSQL database dump
--

\restrict 0yFeBZTdrfU6GNbcGtWnen9GZw8TNGhMBQ8cMotiuHuWAc8jeaJgQXyb4vf0pG9

-- Dumped from database version 16.10
-- Dumped by pg_dump version 16.10

-- Started on 2025-11-16 23:17:16

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16438)
-- Name: avaliacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.avaliacao (
    id_avaliacao integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text,
    data_criacao date NOT NULL,
    id_gestor integer NOT NULL,
    id_tipo_avaliacao integer
);


ALTER TABLE public.avaliacao OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16437)
-- Name: avaliacao_id_avaliacao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.avaliacao_id_avaliacao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.avaliacao_id_avaliacao_seq OWNER TO postgres;

--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 217
-- Name: avaliacao_id_avaliacao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.avaliacao_id_avaliacao_seq OWNED BY public.avaliacao.id_avaliacao;


--
-- TOC entry 224 (class 1259 OID 16480)
-- Name: formulario_respondido; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formulario_respondido (
    id_form integer NOT NULL,
    id_avaliacao integer NOT NULL,
    id_cliente integer NOT NULL,
    id_corretor integer NOT NULL,
    data_resposta date NOT NULL
);


ALTER TABLE public.formulario_respondido OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16479)
-- Name: formulario_respondido_id_form_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formulario_respondido_id_form_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.formulario_respondido_id_form_seq OWNER TO postgres;

--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 223
-- Name: formulario_respondido_id_form_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formulario_respondido_id_form_seq OWNED BY public.formulario_respondido.id_form;


--
-- TOC entry 222 (class 1259 OID 16461)
-- Name: questao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questao (
    id_questao integer NOT NULL,
    texto text NOT NULL,
    id_avaliacao integer NOT NULL,
    id_tipo integer NOT NULL
);


ALTER TABLE public.questao OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16460)
-- Name: questao_id_questao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questao_id_questao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.questao_id_questao_seq OWNER TO postgres;

--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 221
-- Name: questao_id_questao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questao_id_questao_seq OWNED BY public.questao.id_questao;


--
-- TOC entry 226 (class 1259 OID 16504)
-- Name: resposta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.resposta (
    id_resposta integer NOT NULL,
    id_form integer NOT NULL,
    id_questao integer NOT NULL,
    resposta_texto text,
    resposta_numero numeric(10,2),
    CONSTRAINT resposta_check CHECK ((((resposta_texto IS NOT NULL) AND (resposta_numero IS NULL)) OR ((resposta_texto IS NULL) AND (resposta_numero IS NOT NULL))))
);


ALTER TABLE public.resposta OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16503)
-- Name: resposta_id_resposta_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.resposta_id_resposta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.resposta_id_resposta_seq OWNER TO postgres;

--
-- TOC entry 4864 (class 0 OID 0)
-- Dependencies: 225
-- Name: resposta_id_resposta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.resposta_id_resposta_seq OWNED BY public.resposta.id_resposta;


--
-- TOC entry 228 (class 1259 OID 16524)
-- Name: tipo_avaliacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipo_avaliacao (
    id_tipo_avaliacao integer NOT NULL,
    nome_tipo character varying(50) NOT NULL,
    descricao text
);


ALTER TABLE public.tipo_avaliacao OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16523)
-- Name: tipo_avaliacao_id_tipo_avaliacao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipo_avaliacao_id_tipo_avaliacao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipo_avaliacao_id_tipo_avaliacao_seq OWNER TO postgres;

--
-- TOC entry 4865 (class 0 OID 0)
-- Dependencies: 227
-- Name: tipo_avaliacao_id_tipo_avaliacao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipo_avaliacao_id_tipo_avaliacao_seq OWNED BY public.tipo_avaliacao.id_tipo_avaliacao;


--
-- TOC entry 220 (class 1259 OID 16452)
-- Name: tipo_questao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipo_questao (
    id_tipo integer NOT NULL,
    nome_tipo character varying(50) NOT NULL,
    descricao text,
    opcoes text
);


ALTER TABLE public.tipo_questao OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16451)
-- Name: tipo_questao_id_tipo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipo_questao_id_tipo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipo_questao_id_tipo_seq OWNER TO postgres;

--
-- TOC entry 4866 (class 0 OID 0)
-- Dependencies: 219
-- Name: tipo_questao_id_tipo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipo_questao_id_tipo_seq OWNED BY public.tipo_questao.id_tipo;


--
-- TOC entry 216 (class 1259 OID 16429)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    nome character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    telefone character varying(20),
    senha character varying(100) NOT NULL,
    perfil character varying(50)
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16428)
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_usuario_seq OWNER TO postgres;

--
-- TOC entry 4867 (class 0 OID 0)
-- Dependencies: 215
-- Name: usuario_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;


--
-- TOC entry 4665 (class 2604 OID 16441)
-- Name: avaliacao id_avaliacao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.avaliacao ALTER COLUMN id_avaliacao SET DEFAULT nextval('public.avaliacao_id_avaliacao_seq'::regclass);


--
-- TOC entry 4668 (class 2604 OID 16483)
-- Name: formulario_respondido id_form; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formulario_respondido ALTER COLUMN id_form SET DEFAULT nextval('public.formulario_respondido_id_form_seq'::regclass);


--
-- TOC entry 4667 (class 2604 OID 16464)
-- Name: questao id_questao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questao ALTER COLUMN id_questao SET DEFAULT nextval('public.questao_id_questao_seq'::regclass);


--
-- TOC entry 4669 (class 2604 OID 16507)
-- Name: resposta id_resposta; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resposta ALTER COLUMN id_resposta SET DEFAULT nextval('public.resposta_id_resposta_seq'::regclass);


--
-- TOC entry 4670 (class 2604 OID 16527)
-- Name: tipo_avaliacao id_tipo_avaliacao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_avaliacao ALTER COLUMN id_tipo_avaliacao SET DEFAULT nextval('public.tipo_avaliacao_id_tipo_avaliacao_seq'::regclass);


--
-- TOC entry 4666 (class 2604 OID 16455)
-- Name: tipo_questao id_tipo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_questao ALTER COLUMN id_tipo SET DEFAULT nextval('public.tipo_questao_id_tipo_seq'::regclass);


--
-- TOC entry 4664 (class 2604 OID 16432)
-- Name: usuario id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);


--
-- TOC entry 4845 (class 0 OID 16438)
-- Dependencies: 218
-- Data for Name: avaliacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.avaliacao (id_avaliacao, nome, descricao, data_criacao, id_gestor, id_tipo_avaliacao) FROM stdin;
1	Avaliação de Primeiro Atendimento	Avaliação após primeiro contato	2025-11-12	3	1
2	Avaliação de Visita	Avaliação após visita	2025-11-12	3	2
3	Avaliação de Fechamento	Avaliação sobre a negociação	2025-11-16	3	3
4	Avaliação de Visita MRV	Avaliação MRV	2025-11-16	3	2
\.


--
-- TOC entry 4851 (class 0 OID 16480)
-- Dependencies: 224
-- Data for Name: formulario_respondido; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formulario_respondido (id_form, id_avaliacao, id_cliente, id_corretor, data_resposta) FROM stdin;
1	1	1	2	2025-11-12
3	2	7	8	2025-11-12
4	1	5	2	2025-11-13
5	2	1	4	2025-11-13
12	2	5	2	2025-11-16
13	2	7	9	2025-11-16
14	3	11	2	2025-11-16
\.


--
-- TOC entry 4849 (class 0 OID 16461)
-- Dependencies: 222
-- Data for Name: questao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questao (id_questao, texto, id_avaliacao, id_tipo) FROM stdin;
1	Como você avalia o atendimento que recebeu?	1	1
3	O que podemos melhorar nesse primeiro contato?	1	3
4	De 0 a 5 o quanto você se vê morando nesse local?	2	4
2	O corretor entendeu bem o que você procura?	1	6
8	O(a) corretor(a) chegou no horário combinado?	2	9
9	Você se sentiu bem atendido(a) durante a visita?	2	2
10	Como você avalia a experiência da visita?	2	1
11	O que podemos melhorar na visita?	2	3
6	Você se sentiu à vontade para tirar suas dúvidas?	1	2
7	O agendamento e horário da visita foram convenientes? Sendo 0 ruim e 5 excelente.	2	4
5	O(a) corretor(a) demorou para entrar em contato? Sendo 0 muito demorado e 5 muito rápido.	1	4
13	Você se sentiu confortável com a reunião de fechamento de negócio?	3	6
\.


--
-- TOC entry 4853 (class 0 OID 16504)
-- Dependencies: 226
-- Data for Name: resposta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resposta (id_resposta, id_form, id_questao, resposta_texto, resposta_numero) FROM stdin;
1	1	1	\N	9.00
2	1	2	\N	1.00
3	1	3	Tudo ótimo, muito atencioso!	\N
5	12	4	5	\N
6	12	7	5	\N
7	12	8	Sim	\N
8	12	9	Sim	\N
9	12	10	10	\N
10	12	11	Nada. Foi perfeito!	\N
11	13	4	5	\N
12	13	7	5	\N
13	13	8	Sim	\N
14	13	9	Sim	\N
15	13	10	10	\N
16	13	11	Nada. Foi perfeito!	\N
17	14	13	Sim	\N
\.


--
-- TOC entry 4855 (class 0 OID 16524)
-- Dependencies: 228
-- Data for Name: tipo_avaliacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipo_avaliacao (id_tipo_avaliacao, nome_tipo, descricao) FROM stdin;
1	Primeiro Atendimento	Avaliação após primeiro contato
2	Visita	Avaliação após visita
3	Negociação	Avaliação a respeito da negociação
\.


--
-- TOC entry 4847 (class 0 OID 16452)
-- Dependencies: 220
-- Data for Name: tipo_questao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipo_questao (id_tipo, nome_tipo, descricao, opcoes) FROM stdin;
3	Texto livre	Respostas abertas	\N
2	Sim, Mais ou menos, Não	Questões com opções fixas: sim, mais ou menos, não	Sim, Mais ou menos, Não
4	Escala (0 a 5)	De 0 a 5	0, 1, 2, 3, 4, 5
5	Nota	Numérico	\N
6	Sim, Parcialmente, Não	Questões com opções fixas: sim, parcialmente, não	Sim, Parcialmente, Não
7	Motivo para não seguir a negociação	Questões com opções fixas: Valor do imóvel, Condições do contrato, Localização, Atendimento, Outro	Valor do imóvel, Condições do contrato, Localização, Atendimento, Outro
8	Sim, talvez, não	Questões com opções fixas: sim, talvez, não	Sim, Talvez, Não
9	Sim ou não	Questões com opções fixas: sim, não	Sim, Não
1	Escala (0 a 10)	De 0 a 10	0,1,2,3,4,5,6,7,8,9,10
\.


--
-- TOC entry 4843 (class 0 OID 16429)
-- Dependencies: 216
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usuario, nome, email, telefone, senha, perfil) FROM stdin;
1	Ana Silva	ana@email.com	11999990000	1234	cliente
2	Carlos Souza	carlos@email.com	11988887777	1234	corretor
3	Fernanda Lima	fernanda@email.com	11977776666	1234	gestor
5	Giovana	gigi@gmail.com	19984531578	gigi	cliente
8	Ana Claudia	clau@ana.com	4987689672	4321	gestor
9	Joana	joana@email.com	43987459652	joana	corretor
7	Luanna Garla	lua@email.com	439876578765	1234	corretor
4	Administrador	admin@email.com	11900001111	admin123	cliente
10	Admin	administrador@email.com	11999880000	1234	admin
11	Marlon	marlon@email.com.br	11987458213	1234	cliente
\.


--
-- TOC entry 4868 (class 0 OID 0)
-- Dependencies: 217
-- Name: avaliacao_id_avaliacao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.avaliacao_id_avaliacao_seq', 4, true);


--
-- TOC entry 4869 (class 0 OID 0)
-- Dependencies: 223
-- Name: formulario_respondido_id_form_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formulario_respondido_id_form_seq', 14, true);


--
-- TOC entry 4870 (class 0 OID 0)
-- Dependencies: 221
-- Name: questao_id_questao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questao_id_questao_seq', 13, true);


--
-- TOC entry 4871 (class 0 OID 0)
-- Dependencies: 225
-- Name: resposta_id_resposta_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.resposta_id_resposta_seq', 17, true);


--
-- TOC entry 4872 (class 0 OID 0)
-- Dependencies: 227
-- Name: tipo_avaliacao_id_tipo_avaliacao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_avaliacao_id_tipo_avaliacao_seq', 3, true);


--
-- TOC entry 4873 (class 0 OID 0)
-- Dependencies: 219
-- Name: tipo_questao_id_tipo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_questao_id_tipo_seq', 9, true);


--
-- TOC entry 4874 (class 0 OID 0)
-- Dependencies: 215
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 11, true);


--
-- TOC entry 4677 (class 2606 OID 16445)
-- Name: avaliacao avaliacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.avaliacao
    ADD CONSTRAINT avaliacao_pkey PRIMARY KEY (id_avaliacao);


--
-- TOC entry 4683 (class 2606 OID 16485)
-- Name: formulario_respondido formulario_respondido_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formulario_respondido
    ADD CONSTRAINT formulario_respondido_pkey PRIMARY KEY (id_form);


--
-- TOC entry 4685 (class 2606 OID 16538)
-- Name: formulario_respondido formulario_unica_resposta_por_corretor; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formulario_respondido
    ADD CONSTRAINT formulario_unica_resposta_por_corretor UNIQUE (id_avaliacao, id_cliente, id_corretor);


--
-- TOC entry 4681 (class 2606 OID 16468)
-- Name: questao questao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questao
    ADD CONSTRAINT questao_pkey PRIMARY KEY (id_questao);


--
-- TOC entry 4687 (class 2606 OID 16512)
-- Name: resposta resposta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resposta
    ADD CONSTRAINT resposta_pkey PRIMARY KEY (id_resposta);


--
-- TOC entry 4689 (class 2606 OID 16531)
-- Name: tipo_avaliacao tipo_avaliacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_avaliacao
    ADD CONSTRAINT tipo_avaliacao_pkey PRIMARY KEY (id_tipo_avaliacao);


--
-- TOC entry 4679 (class 2606 OID 16459)
-- Name: tipo_questao tipo_questao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_questao
    ADD CONSTRAINT tipo_questao_pkey PRIMARY KEY (id_tipo);


--
-- TOC entry 4673 (class 2606 OID 16436)
-- Name: usuario usuario_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);


--
-- TOC entry 4675 (class 2606 OID 16434)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4690 (class 2606 OID 16446)
-- Name: avaliacao avaliacao_id_gestor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.avaliacao
    ADD CONSTRAINT avaliacao_id_gestor_fkey FOREIGN KEY (id_gestor) REFERENCES public.usuario(id_usuario) ON DELETE CASCADE;


--
-- TOC entry 4691 (class 2606 OID 16532)
-- Name: avaliacao avaliacao_id_tipo_avaliacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.avaliacao
    ADD CONSTRAINT avaliacao_id_tipo_avaliacao_fkey FOREIGN KEY (id_tipo_avaliacao) REFERENCES public.tipo_avaliacao(id_tipo_avaliacao);


--
-- TOC entry 4694 (class 2606 OID 16488)
-- Name: formulario_respondido formulario_respondido_id_avaliacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formulario_respondido
    ADD CONSTRAINT formulario_respondido_id_avaliacao_fkey FOREIGN KEY (id_avaliacao) REFERENCES public.avaliacao(id_avaliacao) ON DELETE CASCADE;


--
-- TOC entry 4695 (class 2606 OID 16493)
-- Name: formulario_respondido formulario_respondido_id_cliente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formulario_respondido
    ADD CONSTRAINT formulario_respondido_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4696 (class 2606 OID 16498)
-- Name: formulario_respondido formulario_respondido_id_corretor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formulario_respondido
    ADD CONSTRAINT formulario_respondido_id_corretor_fkey FOREIGN KEY (id_corretor) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4692 (class 2606 OID 16469)
-- Name: questao questao_id_avaliacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questao
    ADD CONSTRAINT questao_id_avaliacao_fkey FOREIGN KEY (id_avaliacao) REFERENCES public.avaliacao(id_avaliacao) ON DELETE CASCADE;


--
-- TOC entry 4693 (class 2606 OID 16474)
-- Name: questao questao_id_tipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questao
    ADD CONSTRAINT questao_id_tipo_fkey FOREIGN KEY (id_tipo) REFERENCES public.tipo_questao(id_tipo);


--
-- TOC entry 4697 (class 2606 OID 16513)
-- Name: resposta resposta_id_form_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resposta
    ADD CONSTRAINT resposta_id_form_fkey FOREIGN KEY (id_form) REFERENCES public.formulario_respondido(id_form) ON DELETE CASCADE;


--
-- TOC entry 4698 (class 2606 OID 16518)
-- Name: resposta resposta_id_questao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resposta
    ADD CONSTRAINT resposta_id_questao_fkey FOREIGN KEY (id_questao) REFERENCES public.questao(id_questao);


-- Completed on 2025-11-16 23:17:16

--
-- PostgreSQL database dump complete
--

\unrestrict 0yFeBZTdrfU6GNbcGtWnen9GZw8TNGhMBQ8cMotiuHuWAc8jeaJgQXyb4vf0pG9

