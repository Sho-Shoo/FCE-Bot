def get_printout(row): 
        cnum, instructor, cname, hours, rating = row
        return f"Course number: {cnum} \nInstructor: {instructor} \nCourse name: {cname} \nWeekly hours: {hours} \nRating: {rating}/5 \n====================\n"

class FCE_services: 

    def __init__(self, cursor) -> None:
        self.cur = cursor


    def get_fce_info_by_cnum(self, cnum: int): 
        query = """
                SELECT cnum, instructor, cname, hours, rating 
                  FROM FCE_info 
                 WHERE cnum = %s
                """
        cmd = self.cur.mogrify(query, (cnum,)) 
        self.cur.execute(cmd)
        rows = self.cur.fetchall()

        if len(rows) == 0: 
            return "No records found. "
        else: 
            res_str = "====================\n"
            for row in rows: 
                row_str = get_printout(row)
                res_str += row_str 

            return res_str

    def get_fce_info_by_cname(self, cname: str): 
        return "Search by course name currently unsupported. "

    def get_fce_info(self, query: str):
        try: 
            course_num = int(query)
            return self.get_fce_info_by_cnum(course_num)
        except ValueError: 
            return self.get_fce_info_by_cname(query) 
        except Exception as e:
            print(e)
            return "Unknown error encountered. Try again. "

# for testing 
if __name__ =="__main__": 
    import psycopg2
    import sys

    try:
        db, user = 'fce_db', 'ec2-user'
        if len(sys.argv) >= 2:
            db = sys.argv[1]
        if len(sys.argv) >= 3:
            user = sys.argv[2]
        conn = psycopg2.connect(database=db, user=user)
        conn.autocommit = True
        cur = conn.cursor()
        print("Successfully connected to database. ")
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))
        exit()
    except Exception as e: 
        print(f"Other DB connection error: {e}")
        exit()

    FCE = FCE_services(cur)

    print(FCE.get_fce_info("15122"))
    print(FCE.get_fce_info("15112"))
    print(FCE.get_fce_info("Fundamentals"))
    print(FCE.get_fce_info("12345"))


