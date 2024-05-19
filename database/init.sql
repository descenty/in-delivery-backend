-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION postgres;
-- public.city definition

-- Drop table

-- DROP TABLE public.city;

CREATE TABLE public.city (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT city_pk PRIMARY KEY (id),
	CONSTRAINT city_unique UNIQUE (name)
);


-- public.customer definition

-- Drop table

-- DROP TABLE public.customer;

CREATE TABLE public.customer (
	user_id uuid NOT NULL,
	delivery_address_id uuid NULL,
	CONSTRAINT customer_pkey PRIMARY KEY (user_id)
);


-- public.category definition

-- Drop table

-- DROP TABLE public.category;

CREATE TABLE public.category (
	slug varchar(20) NOT NULL,
	title text NOT NULL,
	parent_slug varchar(20) NULL,
	CONSTRAINT category_pkey PRIMARY KEY (slug),
	CONSTRAINT category_parent_fkey FOREIGN KEY (parent_slug) REFERENCES public.category(slug)
);


-- public.customer_delivery_address definition

-- Drop table

-- DROP TABLE public.customer_delivery_address;

CREATE TABLE public.customer_delivery_address (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	user_id uuid NOT NULL,
	"name" varchar(255) NOT NULL,
	latitude float8 NOT NULL,
	longitude float8 NOT NULL,
	city_id uuid NOT NULL,
	CONSTRAINT user_delivery_address_pkey PRIMARY KEY (id),
	CONSTRAINT customer_delivery_address_city_fk FOREIGN KEY (city_id) REFERENCES public.city(id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.product definition

-- Drop table

-- DROP TABLE public.product;

CREATE TABLE public.product (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	title varchar(64) NOT NULL,
	description text NOT NULL,
	price numeric(7, 2) NOT NULL,
	best_before int4 NULL,
	proteins float4 NULL,
	fats float4 NULL,
	carbohydrates float4 NULL,
	energy float4 NOT NULL,
	weight int4 NULL,
	category_slug varchar(20) NULL,
	CONSTRAINT product_pkey PRIMARY KEY (id),
	CONSTRAINT product_category_slug_fkey FOREIGN KEY (category_slug) REFERENCES public.category(slug)
);


-- public.restaurant definition

-- Drop table

-- DROP TABLE public.restaurant;

CREATE TABLE public.restaurant (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	admin_user_id uuid NULL,
	address varchar NOT NULL,
	city_id uuid NOT NULL,
	CONSTRAINT restaurant_pk PRIMARY KEY (id),
	CONSTRAINT restaurant_city_fk FOREIGN KEY (city_id) REFERENCES public.city(id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.cart_product definition

-- Drop table

-- DROP TABLE public.cart_product;

CREATE TABLE public.cart_product (
	product_id uuid NOT NULL,
	user_id uuid NOT NULL,
	quantity int4 NOT NULL,
	is_active bool DEFAULT true NOT NULL,
	CONSTRAINT cart_product_pkey PRIMARY KEY (user_id, product_id),
	CONSTRAINT cart_product_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id)
);


-- public.orders definition

-- Drop table

-- DROP TABLE public.orders;

CREATE TABLE public.orders (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	user_id uuid NOT NULL,
	created_at timestamp DEFAULT now() NOT NULL,
	status varchar(20) NOT NULL,
	total_price numeric(7, 2) NOT NULL,
	delivery_address text NOT NULL,
	restaurant_id uuid NULL,
	CONSTRAINT order_pkey PRIMARY KEY (id),
	CONSTRAINT orders_restaurant_fk FOREIGN KEY (restaurant_id) REFERENCES public.restaurant(id)
);


-- public.order_product definition

-- Drop table

-- DROP TABLE public.order_product;

CREATE TABLE public.order_product (
	order_id uuid NOT NULL,
	product_id uuid NOT NULL,
	quantity int4 NOT NULL,
	price numeric NOT NULL,
	CONSTRAINT order_product_pkey PRIMARY KEY (order_id, product_id),
	CONSTRAINT order_product_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id),
	CONSTRAINT order_product_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id)
);