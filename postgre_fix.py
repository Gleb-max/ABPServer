import psycopg2

dsn = 'postgres://oevaqidctpcmgn:b7b4498465f27c9c4cc3cda45202b0e307de150398e46b3a21097f6918bed295@ec2-3-91-127-228.compute-1.amazonaws.com:5432/d23lm6ck07c3ru'


try:
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    # cur.execute('DROP TABLE "subject" CASCADE')
    # cur.execute("ALTER TABLE subject ADD COLUMN teacher_id "
    #             "FOREIGN KEY(fk_columns) REFERENCES parent_table(parent_key_columns) constraint;")
    cur.close()
    conn.commit()
except (Exception) as error:
    print(error)

