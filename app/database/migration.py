from app.database.connection import get_connection



def migrate_orders():


    conn = get_connection()



    columns = [


        (
            "provider_response",
            "TEXT"
        ),


        (
            "retry_count",
            "INTEGER DEFAULT 0"
        ),


        (
            "updated_at",
            "TIMESTAMP"
        ),


        (
            "telegram_id",
            "INTEGER"
        )


    ]



    existing = [


        row["name"]


        for row in conn.execute(

            "PRAGMA table_info(orders)"

        )

    ]



    for name, datatype in columns:


        if name not in existing:


            print(

                f"[MIGRATION] Adding {name}"

            )


            conn.execute(

                f"""

                ALTER TABLE orders

                ADD COLUMN {name} {datatype}

                """

            )




    # isi updated_at untuk data lama


    conn.execute(

        """

        UPDATE orders

        SET updated_at = CURRENT_TIMESTAMP

        WHERE updated_at IS NULL

        """

    )



    conn.commit()


    conn.close()



    print(

        "[MIGRATION] DONE"

    )