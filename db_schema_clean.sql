CREATE TABLE public.admin (
    admin_id integer NOT NULL,
    admin_user character varying(50) NOT NULL,
    admin_pass character varying(100) NOT NULL,
    admin_name character varying(100),
    admin_email character varying(100),
    admin_pmnt_add text,
    admin_zip character varying(20),
    admin_prsnt_add text,
    admin_city character varying(50),
    admin_country character varying(50)
);

ALTER TABLE public.admin OWNER TO postgres;

CREATE SEQUENCE public.admin_admin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.category (
    cat_id integer NOT NULL,
    cat_name character varying(50) NOT NULL
);

ALTER TABLE public.category OWNER TO postgres;

CREATE SEQUENCE public.category_cat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.customer (
    cus_code integer NOT NULL,
    cus_fname character varying(50) NOT NULL,
    cus_lname character varying(50) NOT NULL,
    cus_email character varying(100),
    cus_phone character varying(11),
    cus_address character varying(255),
    cus_last_updated timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    admin_id integer
);

ALTER TABLE public.customer OWNER TO postgres;

CREATE SEQUENCE public.customer_cus_code_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.orders (
    ord_id integer NOT NULL,
    ord_total_amount numeric(10,2),
    ord_category character varying(255),
    ord_type_product character varying(255),
    ord_quantity integer,
    ord_size text,
    ord_date date DEFAULT CURRENT_TIMESTAMP,
    ord_date_completion date,
    prod_id integer,
    cus_code integer
);

ALTER TABLE public.orders OWNER TO postgres;

CREATE SEQUENCE public.orders_cus_code_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.orders_ord_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.orders_prod_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.product (
    prod_id integer NOT NULL,
    prod_name character varying(255) NOT NULL,
    prod_quantity integer NOT NULL,
    prod_thickness integer,
    prod_image bytea,
    prod_last_updated date DEFAULT CURRENT_TIMESTAMP,
    prod_roll_size character varying(200),
    pur_id integer,
    prod_price numeric(10,2),
    cat_id integer,
    prod_category character varying(200)
);

ALTER TABLE public.product OWNER TO postgres;

CREATE SEQUENCE public.product_prod_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.purchase (
    pur_id integer NOT NULL,
    sup_id integer,
    pur_amount numeric(10,2),
    pur_order_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    pur_product_name text,
    pur_roll_size text,
    pur_quantity integer,
    pur_thickness integer
);

ALTER TABLE public.purchase OWNER TO postgres;

CREATE SEQUENCE public.purchase_pur_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.supplier (
    sup_id integer NOT NULL,
    sup_name character varying(255) NOT NULL,
    sup_contact character varying(11) NOT NULL,
    sup_address character varying(255) NOT NULL,
    sup_country character varying(100) NOT NULL,
    sup_email text NOT NULL
);

ALTER TABLE public.supplier OWNER TO postgres;

CREATE SEQUENCE public.supplier_sup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY public.admin ALTER COLUMN admin_id SET DEFAULT nextval('public.admin_admin_id_seq'::regclass);
ALTER TABLE ONLY public.category ALTER COLUMN cat_id SET DEFAULT nextval('public.category_cat_id_seq'::regclass);
ALTER TABLE ONLY public.customer ALTER COLUMN cus_code SET DEFAULT nextval('public.customer_cus_code_seq'::regclass);
ALTER TABLE ONLY public.orders ALTER COLUMN ord_id SET DEFAULT nextval('public.orders_ord_id_seq'::regclass);
ALTER TABLE ONLY public.orders ALTER COLUMN prod_id SET DEFAULT nextval('public.orders_prod_id_seq'::regclass);
ALTER TABLE ONLY public.orders ALTER COLUMN cus_code SET DEFAULT nextval('public.orders_cus_code_seq'::regclass);
ALTER TABLE ONLY public.product ALTER COLUMN prod_id SET DEFAULT nextval('public.product_prod_id_seq'::regclass);
ALTER TABLE ONLY public.purchase ALTER COLUMN pur_id SET DEFAULT nextval('public.purchase_pur_id_seq'::regclass);
ALTER TABLE ONLY public.supplier ALTER COLUMN sup_id SET DEFAULT nextval('public.supplier_sup_id_seq'::regclass);

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_admin_email_key UNIQUE (admin_email);
ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (admin_id);
ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (cat_id);
ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_cus_email_key UNIQUE (cus_email);
ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (cus_code);
ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (ord_id);
ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (prod_id);
ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_pkey PRIMARY KEY (pur_id);
ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT supplier_pkey PRIMARY KEY (sup_id);

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES public.admin(admin_id) NOT VALID;
ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_cus_code_fkey FOREIGN KEY (cus_code) REFERENCES public.customer(cus_code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.orders
    ADD CONSTRAINT prod_id FOREIGN KEY (prod_id) REFERENCES public.product(prod_id) NOT VALID;
ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_cat_id_fkey FOREIGN KEY (cat_id) REFERENCES public.category(cat_id) NOT VALID;
ALTER TABLE ONLY public.product
    ADD CONSTRAINT pur_id FOREIGN KEY (pur_id) REFERENCES public.purchase(pur_id) NOT VALID;
ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_sup_id_fkey FOREIGN KEY (sup_id) REFERENCES public.supplier(sup_id);
ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_sup_id_fkey1 FOREIGN KEY (sup_id) REFERENCES public.supplier(sup_id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_sup_id_fkey2 FOREIGN KEY (sup_id) REFERENCES public.supplier(sup_id) ON UPDATE CASCADE ON DELETE CASCADE;
