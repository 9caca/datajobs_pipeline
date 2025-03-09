--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.4 (Debian 17.4-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: companies; Type: TABLE; Schema: public; Owner: datajobs_scraper
--

CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    industry character varying(100),
    location character varying(100),
    website character varying(255)
);


ALTER TABLE public.companies OWNER TO datajobs_scraper;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: public; Owner: datajobs_scraper
--

CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.companies_id_seq OWNER TO datajobs_scraper;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: datajobs_scraper
--

ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;


--
-- Name: job_requirements; Type: TABLE; Schema: public; Owner: datajobs_scraper
--

CREATE TABLE public.job_requirements (
    id integer NOT NULL,
    job_id integer NOT NULL,
    requirement_id integer NOT NULL
);


ALTER TABLE public.job_requirements OWNER TO datajobs_scraper;

--
-- Name: job_requirements_id_seq; Type: SEQUENCE; Schema: public; Owner: datajobs_scraper
--

CREATE SEQUENCE public.job_requirements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_requirements_id_seq OWNER TO datajobs_scraper;

--
-- Name: job_requirements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: datajobs_scraper
--

ALTER SEQUENCE public.job_requirements_id_seq OWNED BY public.job_requirements.id;


--
-- Name: job_tasks; Type: TABLE; Schema: public; Owner: datajobs_scraper
--

CREATE TABLE public.job_tasks (
    id integer NOT NULL,
    job_id integer,
    task text
);


ALTER TABLE public.job_tasks OWNER TO datajobs_scraper;

--
-- Name: job_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: datajobs_scraper
--

CREATE SEQUENCE public.job_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_tasks_id_seq OWNER TO datajobs_scraper;

--
-- Name: job_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: datajobs_scraper
--

ALTER SEQUENCE public.job_tasks_id_seq OWNED BY public.job_tasks.id;


--
-- Name: job_technologies; Type: TABLE; Schema: public; Owner: datajobs_scraper
--

CREATE TABLE public.job_technologies (
    id integer NOT NULL,
    job_id integer,
    technology character varying(255)
);


ALTER TABLE public.job_technologies OWNER TO datajobs_scraper;

--
-- Name: job_technologies_id_seq; Type: SEQUENCE; Schema: public; Owner: datajobs_scraper
--

CREATE SEQUENCE public.job_technologies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_technologies_id_seq OWNER TO datajobs_scraper;

--
-- Name: job_technologies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: datajobs_scraper
--

ALTER SEQUENCE public.job_technologies_id_seq OWNED BY public.job_technologies.id;


--
-- Name: jobs; Type: TABLE; Schema: public; Owner: datajobs_scraper
--

CREATE TABLE public.jobs (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    company_id integer,
    description text,
    location character varying(100),
    salary_range character varying(100),
    job_type character varying(50),
    date_posted date,
    source character varying(50),
    link character varying(512),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    experience_required character varying,
    work_setting character varying,
    external_id character varying(20)
);


ALTER TABLE public.jobs OWNER TO datajobs_scraper;

--
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: datajobs_scraper
--

CREATE SEQUENCE public.jobs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jobs_id_seq OWNER TO datajobs_scraper;

--
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: datajobs_scraper
--

ALTER SEQUENCE public.jobs_id_seq OWNED BY public.jobs.id;


--
-- Name: requirements; Type: TABLE; Schema: public; Owner: datajobs_scraper
--

CREATE TABLE public.requirements (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    category character varying(100)
);


ALTER TABLE public.requirements OWNER TO datajobs_scraper;

--
-- Name: requirements_id_seq; Type: SEQUENCE; Schema: public; Owner: datajobs_scraper
--

CREATE SEQUENCE public.requirements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.requirements_id_seq OWNER TO datajobs_scraper;

--
-- Name: requirements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: datajobs_scraper
--

ALTER SEQUENCE public.requirements_id_seq OWNED BY public.requirements.id;


--
-- Name: companies id; Type: DEFAULT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: job_requirements id; Type: DEFAULT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_requirements ALTER COLUMN id SET DEFAULT nextval('public.job_requirements_id_seq'::regclass);


--
-- Name: job_tasks id; Type: DEFAULT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_tasks ALTER COLUMN id SET DEFAULT nextval('public.job_tasks_id_seq'::regclass);


--
-- Name: job_technologies id; Type: DEFAULT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_technologies ALTER COLUMN id SET DEFAULT nextval('public.job_technologies_id_seq'::regclass);


--
-- Name: jobs id; Type: DEFAULT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.jobs ALTER COLUMN id SET DEFAULT nextval('public.jobs_id_seq'::regclass);


--
-- Name: requirements id; Type: DEFAULT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.requirements ALTER COLUMN id SET DEFAULT nextval('public.requirements_id_seq'::regclass);


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: datajobs_scraper
--

COPY public.companies (id, name, industry, location, website) FROM stdin;
1	Zenith Algorithms	\N	Halifax (NS)	\N
2	Newest Immigration Consulting Ltd.	\N	Remote	\N
3	LTIMindtree	\N	Toronto (ON)	\N
4	NES Fircroft	\N	Calgary (AB)	\N
5	Stoic Finch	\N	Calgary (AB)	\N
6	Designed Wealth Management	\N	Toronto (ON)	\N
7	Navacord	\N	Toronto (ON)	\N
8	Ramp Group	\N	Surrey (BC)	\N
9	Incepta Solutions	\N	Toronto (ON)	\N
10	BBD Insights Inc.	\N	North York (ON)	\N
11	Clientserver Tech Systems	\N	Mississauga (ON)	\N
12	Nextgen System Canada	\N	North York (ON)	\N
13	WESTGATE TECHNOLOGY CORPORATION	\N	Delta (BC)	\N
14	Celestial Systems Inc.	\N	Burnaby (BC)	\N
15	Wynshop	\N	North York (ON)	\N
16	PostgreSQL Pros	\N	Milton (ON)	\N
17	Superior Events Group/Luxe Modern Rentals	\N	North York (ON)	\N
18	IODEVOPS SERVICES INC.	\N	Vancouver (BC)	\N
19	VISAY TECHNOLOGIES INC	\N	Edmonton (AB)	\N
20	Niagara Casinos	\N	Niagara Falls (ON)	\N
21	Industries Machinex inc.	\N	Lévis (QC)	\N
22	Northern Base Technologies LLP	\N	Toronto (ON)	\N
23	ONTARIO HIV TREATMENT NETWORK	\N	\N	\N
24	JUMP TECHNOLOGY DEVELOPMENT	\N	\N	\N
25	Ren's Pets Depot	\N	\N	\N
26	Produits Boréal	\N	\N	\N
\.


--
-- Data for Name: job_requirements; Type: TABLE DATA; Schema: public; Owner: datajobs_scraper
--

COPY public.job_requirements (id, job_id, requirement_id) FROM stdin;
1	8	1
2	8	2
3	8	3
4	8	4
5	8	5
6	8	6
7	12	7
8	12	8
9	12	9
10	12	10
11	12	2
12	12	11
13	12	12
14	13	13
15	13	7
16	13	1
17	13	14
18	13	15
19	14	1
20	14	16
21	14	15
22	15	13
23	15	2
24	15	17
25	15	18
26	15	19
27	15	20
28	15	21
29	15	22
30	15	6
31	15	23
32	15	24
33	15	11
34	15	15
35	15	25
36	15	26
37	17	27
38	17	28
39	17	29
40	17	30
41	17	31
42	17	32
43	17	33
44	17	34
45	17	35
46	17	36
47	17	3
48	17	37
49	17	6
50	17	23
51	17	24
52	17	38
53	17	39
54	17	40
55	17	41
56	17	15
57	17	42
58	17	43
59	17	44
60	18	7
61	18	1
62	18	3
63	18	6
64	18	23
65	18	15
66	19	30
67	19	45
68	19	11
69	19	46
70	21	47
71	21	30
72	21	48
73	21	49
74	21	34
75	21	46
76	21	35
77	21	36
78	21	50
79	21	51
80	21	52
81	21	53
82	21	23
83	21	16
84	21	54
85	21	11
86	21	12
87	21	41
88	21	55
89	21	56
90	21	25
91	21	26
\.


--
-- Data for Name: job_tasks; Type: TABLE DATA; Schema: public; Owner: datajobs_scraper
--

COPY public.job_tasks (id, job_id, task) FROM stdin;
1	8	Build predictive models
2	8	Data Science
3	8	Design methods of collecting and processing data to answer specific research questions
4	8	Document technical requirements to ensure that products, processes and solutions meet business requirements
5	8	Extract information from unstructured sets of data
6	8	Highlight key data sources and the methodology to be used on a specific project
7	8	Research data collection and administration policy
8	8	Synthesize technical information through creation of data visualization
9	8	Develop and implement data administration policy, standards and models
10	8	Lead and co-ordinate teams of information systems professionals in the development of software and integrated information systems, process control software and other embedded software control systems
11	8	Develop and implement policies and procedures throughout the software development life cycle
12	8	Research and document data requirements, data collection and administration policy, and data access rules
13	8	Conduct reviews to assess quality assurance practices, software products and information systems
14	8	Lead and co-ordinate teams of data administrators in the development and implementation of data policies, standards and models
15	8	Conduct tests and perform security and quality controls
16	8	Execute and document results of software application tests and information and telecommunication systems tests
17	12	Data Science
18	12	Design, develop and implement information systems business solutions
19	12	Operate database management systems to analyze data
20	12	Develop and implement data administration policy, standards and models
21	12	Develop and implement policies and procedures throughout the software development life cycle
22	12	Research and document data requirements, data collection and administration policy, and data access rules
23	12	Write scripts related to stored procedures and triggers
24	12	Research and evaluate a variety of software products
25	12	Meet with clients to discuss system requirements, specifications, costs and timelines
26	13	Build predictive models
27	13	Communicate the business and technical benefits of the analytic solution to both business and technical audiences
28	13	Conduct research regarding availability and suitability of data
29	13	Data Science
30	13	Document technical requirements to ensure that products, processes and solutions meet business requirements
31	13	Research data collection and administration policy
32	13	Use ensemble modelling to combine multiple algorithms to obtain better predictive performance
33	13	Provide advice on information systems strategy, policy, management and service delivery
34	13	Research and document data requirements, data collection and administration policy, and data access rules
35	13	Lead and co-ordinate teams of data administrators in the development and implementation of data policies, standards and models
36	13	Operate automatic or other testing equipment to ensure product quality
37	13	Conduct tests and perform security and quality controls
38	13	Execute and document results of software application tests and information and telecommunication systems tests
39	14	Confer with clients to identify requirements
40	14	Develop data mapping methods
41	14	Extract information from unstructured sets of data
42	14	Research data collection and administration policy
43	14	Synthesize technical information through creation of data visualization
44	14	Design and develop database
45	14	Design, develop and implement information systems business solutions
46	14	Operate database management systems to analyze data
47	14	Develop and implement data administration policy, standards and models
48	14	Lead and co-ordinate teams of information systems professionals in the development of software and integrated information systems, process control software and other embedded software control systems
49	14	Develop policies and procedures for network access and usage and for the backup and recovery of data
50	15	Develop queries and logic to generate reports
51	15	Document technical requirements to ensure that products, processes and solutions meet business requirements
52	15	Extract information from unstructured sets of data
53	15	Highlight key data sources and the methodology to be used on a specific project
54	15	Prepare plan to maintain software
55	15	Synthesize technical information through creation of data visualization
56	15	Use ensemble modelling to combine multiple algorithms to obtain better predictive performance
57	15	Design and develop database
58	15	Design, develop and implement information systems business solutions
59	15	Provide advice on information systems strategy, policy, management and service delivery
60	15	Operate database management systems to analyze data
61	15	Develop policies, procedures and contingency plans to minimize the effects of security breaches
62	15	Develop and implement policies and procedures throughout the software development life cycle
63	15	Research and document data requirements, data collection and administration policy, and data access rules
64	15	Conduct reviews to assess quality assurance practices, software products and information systems
65	15	Lead and co-ordinate teams of data administrators in the development and implementation of data policies, standards and models
66	15	Operate automatic or other testing equipment to ensure product quality
67	16	Data Science
68	16	Design and develop database
69	16	Design, develop and implement information systems business solutions
70	16	Operate database management systems to analyze data
71	16	Develop and implement data administration policy, standards and models
72	16	Write scripts related to stored procedures and triggers
73	16	Collect and document user's requirements
74	17	Data Science
75	17	Design and develop database
76	17	Design, develop and implement information systems business solutions
77	17	Provide advice on information systems strategy, policy, management and service delivery
78	17	Operate database management systems to analyze data
79	17	Develop and implement data administration policy, standards and models
80	17	Conduct reviews to assess quality assurance practices, software products and information systems
81	18	Assess and troubleshoot applications software
82	18	Communicate the business and technical benefits of the analytic solution to both business and technical audiences
83	18	Data Science
84	18	Design and develop database
85	18	Provide advice on information systems strategy, policy, management and service delivery
86	18	Operate database management systems to analyze data
87	18	Conduct tests and perform security and quality controls
88	19	Collect data to identify areas for improvement within an organization’s IT infrastructure
89	19	Develop and maintain computer databases
90	19	Document customers’ requirements for projects
91	19	Document reporting needs, queries, logic, results and recommendations to other information systems professionals
92	19	Design and develop database
93	19	Operate database management systems to analyze data
94	19	Research and document data requirements, data collection and administration policy, and data access rules
95	20	Operate database management systems to analyze data
96	20	Research and document data requirements, data collection and administration policy, and data access rules
97	20	Develop policies and procedures for network access and usage and for the backup and recovery of data
98	20	Lead and co-ordinate teams of data administrators in the development and implementation of data policies, standards and models
99	20	Write scripts related to stored procedures and triggers
100	21	Assess and troubleshoot applications software
101	21	Communicate the business and technical benefits of the analytic solution to both business and technical audiences
102	21	Data Science
103	21	Develop data mapping methods
104	21	Document data access rules
105	21	Document technical requirements to ensure that products, processes and solutions meet business requirements
106	21	Extract information from unstructured sets of data
107	21	Highlight key data sources and the methodology to be used on a specific project
108	21	Research data collection and administration policy
109	21	Design and develop database
110	21	Develop and implement data administration policy, standards and models
111	21	Research and document data requirements, data collection and administration policy, and data access rules
112	21	Usability testing
113	21	Operate automatic or other testing equipment to ensure product quality
\.


--
-- Data for Name: job_technologies; Type: TABLE DATA; Schema: public; Owner: datajobs_scraper
--

COPY public.job_technologies (id, job_id, technology) FROM stdin;
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: datajobs_scraper
--

COPY public.jobs (id, title, company_id, description, location, salary_range, job_type, date_posted, source, link, created_at, experience_required, work_setting, external_id) FROM stdin;
1	data engineer	3	\N	Toronto (ON)	Salary not available	\N	2025-03-07	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43543951;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:00.187988	\N	On-site	\N
2	data engineer	22	\N	Toronto (ON)	$60.00 hourly	\N	2025-02-26	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43494252;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:00.865644	\N	On-site	\N
3	data engineer	23	\N	Toronto (ON)	$79,567.50 to $97,857.99 annually	\N	2025-02-27	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43502349;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:01.810405	\N	On-site	\N
4	data engineer	25	\N	Guelph (ON)	Salary not available	\N	2025-03-07	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43545956;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:02.44423	\N	On-site	\N
5	data engineer	3	\N	Toronto (ON)	Salary not available	\N	2025-02-12	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43389673;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:03.079181	\N	On-site	\N
6	data engineer	1	\N	Toronto (ON)	$50.00 to $60.00 hourly	\N	2025-02-14	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43407323;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:03.763015	\N	On-site	\N
7	data engineer	7	\N	Toronto (ON)	Salary not available	\N	2025-02-18	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43433129;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:04.73182	\N	On-site	\N
8	data engineer	8	\N	Surrey (BC)	$45.87 hourly	\N	2025-02-20	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43442353;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:05.410839	3 years to less than 5 years	On-site	\N
9	data engineer	6	\N	Toronto (ON)	$44.00 hourly	\N	2025-02-10	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43378059;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:06.307646	\N	On-site	\N
10	data engineer	1	\N	Halifax (NS)	$50.00 to $60.00 hourly	\N	2025-02-18	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43423762;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:07.007862	\N	On-site	\N
11	data engineer	3	\N	Toronto (ON)	Salary not available	\N	2025-02-20	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43450750;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:07.679712	\N	On-site	\N
12	data engineer	11	\N	Mississauga (ON)	$51.00 hourly	\N	2025-01-17	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43133078;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:08.35901	1 year to less than 2 years	On-site	\N
13	data engineer	12	\N	North York (ON)	$49.00 to $51.00 hourly (to be negotiated)	\N	2024-12-30	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/42959711;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:09.089112	2 years to less than 3 years	On-site	\N
14	data engineer	8	\N	Surrey (BC)	$45.87 to $48.08 hourly (to be negotiated)	\N	2024-11-22	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/42634767;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:09.796634	1 year to less than 2 years	On-site	\N
15	data engineer	13	\N	Delta (BC)	$70.00 hourly	\N	2024-11-14	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/42542376;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:10.426596	5 years or more	On-site	\N
16	data engineer	14	\N	Burnaby (BC)	$60.10 hourly	\N	2024-12-04	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/42759879;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:11.374665	5 years or more	On-site	\N
17	data engineer	10	\N	North York (ON)	$85,000.00 to $95,000.00 annually (to be negotiated)	\N	2025-02-06	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43335482;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:12.122557	2 years to less than 3 years	On-site	\N
18	data engineer	16	\N	Milton (ON)	$50.00 hourly	\N	2024-11-14	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/42541766;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:13.051435	3 years to less than 5 years	On-site	\N
19	data warehouse analyst	24	\N	Ottawa (ON)	$44.50 hourly	\N	2025-03-03	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43523730;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:13.787104	2 years to less than 3 years	On-site	\N
20	data warehouse analyst	19	\N	Edmonton (AB)	$42.05 hourly	\N	2025-01-22	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43190996;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:14.84383	2 years to less than 3 years	On-site	\N
21	artificial intelligence (AI) designer\n\t\t\t\t\n\t\t\t\t\t\n\n\n\n\n\n\nThis job posting is advertised by a recruitment agency on behalf of the employer.	2	\N	Remote	$50.00 to $70.00 hourly (to be negotiated)	\N	2025-01-27	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43235780;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:15.629466	2 years to less than 3 years	Remote	\N
22	artificial intelligence (AI) designer	26	\N	Alma (QC)	$60,000.00 to $80,000.00 annually	\N	2025-03-07	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43544916;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:16.416634	\N	On-site	\N
23	artificial intelligence designer	21	\N	Plessisville (QC)	Salary not available	\N	2025-03-08	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43548709;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:17.204591	\N	On-site	\N
24	artificial intelligence (AI) designer	21	\N	Lévis (QC)	Salary not available	\N	2025-02-14	Job Bank	https://www.jobbank.gc.ca/jobsearch/jobposting/43404163;jsessionid=C1CF6AB4DE9BC67D10AE1809F17DAFDA.jobsearch76?source=searchresults	2025-03-08 06:25:17.848945	\N	On-site	\N
\.


--
-- Data for Name: requirements; Type: TABLE DATA; Schema: public; Owner: datajobs_scraper
--

COPY public.requirements (id, name, category) FROM stdin;
1	Machine Learning	Technology
2	MS SQL Server	Technology
3	MySQL	Technology
4	Oracle	Technology
5	Programming software	Technology
6	SQL	Technology
7	Cloud	Technology
8	Microsoft Visio	Technology
9	TERADATA	Technology
10	DB2	Technology
11	MS Office	Technology
12	Git	Technology
13	Business intelligence	Technology
14	Enterprise Applications Integration (EAI)	Technology
15	Big data	Technology
16	Programming languages	Technology
17	Networking software	Technology
18	Networking security	Technology
19	Internet	Technology
20	Servers	Technology
21	Oracle Solaris	Technology
22	Visual C++ / MFC	Technology
23	Database software	Technology
24	Software development	Technology
25	MS Excel	Technology
26	MS Outlook	Technology
27	Model-View-Controller (MVC)	Technology
28	R	Technology
29	Shell script	Technology
30	Data Warehouse	Technology
31	Linux	Technology
32	C	Technology
33	C++	Technology
34	HTML	Technology
35	JavaScript	Technology
36	CSS	Technology
37	Object-Oriented programming languages	Technology
38	Enterprise resource planning (ERP) software	Technology
39	Hadoop	Technology
40	React.js	Technology
41	Python	Technology
42	TypeScript	Technology
43	Vue.js	Technology
44	Database development	Technology
45	MS Access	Technology
46	MS Windows	Technology
47	Automatic data processing (ADP)	Technology
48	COM / COM+ / DCOM / MTS / ActiveX	Technology
49	Device drivers	Technology
50	Multimedia software	Technology
51	Communication software	Technology
52	Image editing software	Technology
53	HTML editing software	Technology
54	Data analysis software	Technology
55	Figma	Technology
56	GitHub	Technology
\.


--
-- Name: companies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: datajobs_scraper
--

SELECT pg_catalog.setval('public.companies_id_seq', 27, true);


--
-- Name: job_requirements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: datajobs_scraper
--

SELECT pg_catalog.setval('public.job_requirements_id_seq', 91, true);


--
-- Name: job_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: datajobs_scraper
--

SELECT pg_catalog.setval('public.job_tasks_id_seq', 113, true);


--
-- Name: job_technologies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: datajobs_scraper
--

SELECT pg_catalog.setval('public.job_technologies_id_seq', 1, false);


--
-- Name: jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: datajobs_scraper
--

SELECT pg_catalog.setval('public.jobs_id_seq', 25, true);


--
-- Name: requirements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: datajobs_scraper
--

SELECT pg_catalog.setval('public.requirements_id_seq', 56, true);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: job_requirements job_requirements_pkey; Type: CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_requirements
    ADD CONSTRAINT job_requirements_pkey PRIMARY KEY (id);


--
-- Name: job_tasks job_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_tasks
    ADD CONSTRAINT job_tasks_pkey PRIMARY KEY (id);


--
-- Name: job_technologies job_technologies_pkey; Type: CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_technologies
    ADD CONSTRAINT job_technologies_pkey PRIMARY KEY (id);


--
-- Name: jobs jobs_job_id_unique; Type: CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_job_id_unique UNIQUE (external_id);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: requirements requirements_pkey; Type: CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.requirements
    ADD CONSTRAINT requirements_pkey PRIMARY KEY (id);


--
-- Name: jobs unique_external_id; Type: CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT unique_external_id UNIQUE (external_id);


--
-- Name: idx_job_tasks_job_id; Type: INDEX; Schema: public; Owner: datajobs_scraper
--

CREATE INDEX idx_job_tasks_job_id ON public.job_tasks USING btree (job_id);


--
-- Name: idx_job_technologies_job_id; Type: INDEX; Schema: public; Owner: datajobs_scraper
--

CREATE INDEX idx_job_technologies_job_id ON public.job_technologies USING btree (job_id);


--
-- Name: idx_jobs_job_id; Type: INDEX; Schema: public; Owner: datajobs_scraper
--

CREATE INDEX idx_jobs_job_id ON public.jobs USING btree (external_id);


--
-- Name: job_requirements job_requirements_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_requirements
    ADD CONSTRAINT job_requirements_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_requirements job_requirements_requirement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_requirements
    ADD CONSTRAINT job_requirements_requirement_id_fkey FOREIGN KEY (requirement_id) REFERENCES public.requirements(id);


--
-- Name: job_tasks job_tasks_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_tasks
    ADD CONSTRAINT job_tasks_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_technologies job_technologies_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.job_technologies
    ADD CONSTRAINT job_technologies_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: jobs jobs_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: datajobs_scraper
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- PostgreSQL database dump complete
--

