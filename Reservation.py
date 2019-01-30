class Reservation:

  def __init__(self, email, hotel_id, room_num, check_in,  check_out, num_persons):
    self.email = email
    self.hotel_id = hotel_id
    self.room_num = room_num
    self.check_in = check_in
    self.check_out = check_out
    self.num_persons = num_persons

  def create_table(conn):
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reservation (
      email TEXT NOT NULL,
      hotel_id INTEGER NOT NULL,
      room_num INTEGER NOT NULL,
      check_in DATE NOT NULL,
      check_out DATE NOT NULL,
      num_persons INTEGER NOT NULL,
      FOREIGN KEY(hotel_id, room_num) REFERENCES room(id_hotel, num),
      PRIMARY KEY (hotel_id, room_num, check_in)
    )""")

  def load(self, conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO room (email, hotel_id, room_num, check_in, check_out, num_persons) VALUES(%s, %s, %s, %s)", (self.email, self.hotel_id, self.room_num, self.check_in, self.check_out, self.num_persons))
    
  def is_room_available (conn, hotel_id, room_num, check_in):
    cur = conn.cursor()

    request = "SELECT * FROM Hotel WHERE id = {} AND open = 1"
    cur.execute(request.format(hotel_id))

    if cur.fetchone() is None : return False

    request = "SELECT * FROM Reservation WHERE hotel_id = {} AND room_num = {} AND check_in = '{}'"
    cur.execute(request.format(hotel_id, room_num, check_in))
    
    return cur.fetchone() is None
