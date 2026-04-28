CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE first_name = p_contact_name LIMIT 1;
    IF v_contact_id IS NOT NULL THEN
        INSERT INTO phones(contact_id, phone, type) VALUES(v_contact_id, p_phone, p_type);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES(p_group_name) RETURNING id INTO v_group_id;
    END IF;
    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_contact_name;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts_advanced(p_query TEXT)
RETURNS TABLE(contact_name VARCHAR, email VARCHAR, phone_num VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.first_name, c.email, p.phone 
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(l INT, o INT)
RETURNS TABLE(id INT, first_name VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.first_name, c.email FROM contacts c
                 ORDER BY c.first_name
                 LIMIT l OFFSET o;
END;
$$ LANGUAGE plpgsql;
