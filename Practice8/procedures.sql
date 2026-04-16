-- 1. Upsert (Add or Update)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone_number = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone_number) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Bulk insert with validation
-- Accepts arrays of names and phone numbers
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        -- Simple validation: phone number must be at least 10 characters long
        IF length(p_phones[i]) >= 10 THEN
            INSERT INTO phonebook(first_name, phone_number) 
            VALUES(p_names[i], p_phones[i])
            ON CONFLICT (phone_number) DO NOTHING;
        ELSE
            RAISE NOTICE 'Invalid phone number for user %: %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Deletion
CREATE OR REPLACE PROCEDURE delete_contact_by_data(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook 
    WHERE first_name = p_identifier OR phone_number = p_identifier;
END;
$$;