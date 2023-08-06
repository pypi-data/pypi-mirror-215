from ctypes.wintypes import POINT
from CirclesLocalLoggerPython.LoggerServiceSingleton import LoggerServiceSingleton
from config import db_connection

class Profile:

  def __init__(self, name_in, lang_in, address_in, city_in, state_in, country_in, postal_code_in, telephone_in, photo_in, latitude_in, longitude_in, hours_in, reaction_in, reaction_type_in):
    self.name = name_in
    self.lang = lang_in
    self.address = address_in
    self.city = city_in
    self.state = state_in
    self.country = country_in
    self.postal_code = postal_code_in 
    self.latitude = latitude_in 
    self.longitude = longitude_in
    self.telephone = telephone_in
    self.photo = photo_in
    self.hours = hours_in
    self.reaction = reaction_in
    self.reaction_type = reaction_type_in

  def create(self):
    profile_id = self.insert_profile()
    self.insert_location()
    self.insert_location_profile(profile_id)

    self.insert_telephone()
    self.insert_profile_telephone(profile_id)

    self.insert_storage(profile_id)
    self.insert_profile_storage(profile_id)
    
    self.insert_operational_hours(profile_id)
    
    self.insert_reaction()
    self.insert_profile_reaction(profile_id)

  # def read(self):
  
  def update(self):
    profile_id = self.get_profile_id()
    self.update_profile(profile_id)
    self.update_location(profile_id)
    self.update_telephone(profile_id)
    self.update_storage(profile_id)
    self.update_operational_hours(profile_id)
    self.update_reaction(profile_id)
  
  # def delete(self):

  def get_profile_id(self):
    db = db_connection("profile")
    cursor = db.cursor()

    cursor.execute("SELECT profile_id FROM profile_ml_table WHERE name = '{}'".format(self.name))
    profile_id = cursor.fetchone()

    if not profile_id:
      profile_id = self.insert_profile()

    db.close()
    return profile_id 


  def get_location_id(profile_id):
    db = db_connection("location_profile")
    cursor = db.cursor()

    cursor.execute("SELECT location_id FROM location_profile_table WHERE profile_id = '{}'".format(profile_id))
    location_id = cursor.fetchone()
        
    db.close()
    return location_id

  def get_telephone_id(profile_id):
    db = db_connection("profile_telephone")
    cursor = db.cursor()

    cursor.execute("SELECT telephone_id FROM profile_telephone_table WHERE profile_id = '{}'".format(profile_id))
    telephone_id = cursor.fetchone()
        
    db.close()
    return telephone_id

  def get_reaction_id(profile_id):
    db = db_connection("profile_reaction")
    cursor = db.cursor()

    cursor.execute("SELECT reaction_d FROM profile_reaction_table WHERE profile_id = '{}'".format(profile_id))
    location_id = cursor.fetchone()
        
    db.close()
    return location_id

  def get_storage_id(profile_id):
    db = db_connection("profile_storage")
    cursor = db.cursor()

    cursor.execute("SELECT storage_id FROM profile_storage_table WHERE profile_id = '{}'".format(profile_id))
    storage_id = cursor.fetchone()
        
    db.close()
    return storage_id
  
  def get_hours_ids(profile_id):
    db = db_connection("operational_hours")
    cursor = db.cursor()

    cursor.execute("SELECT id FROM operational_hours_rable WHERE profile_id = '{}'".format(profile_id))
    hours_id = cursor.fetchall()

    db.close()
    return hours_id 

  def insert_profile(self):
    db = db_connection("profile")
    cursor = db.cursor()
    
    cursor.execute("INSERT INTO profile_table(created_user_id, updated_user_id) VALUES (0, 0)")
    db.commit()

    prof_id = cursor.lastrowid
    sql = "INSERT INTO profile_ml_table(profile_id, lang_code, name) VALUES (%s, %s, %s)"
    cursor.execute(sql, (prof_id, self.lang, self.name))

    db.commit() 
    return prof_id

  def update_profile(self, profile_id):
    db = db_connection("profile")
    cursor = db.cursor()

    sql = "UPDATE profile_ml_table SET name = %s WHERE profile_id = %s"
    cursor.execute(sql, (self.name, profile_id))

    db.commit() 
    db.close()

  def insert_location_profile(self, profile_id):
    db = db_connection("location_profile")
    cursor = db.cursor()

    location_id = self.get_location_id(profile_id)
    sql = "INSERT INTO location_profile_table(profile_id, location_id) VALUES (%s, %s)"
    cursor.execute(sql, profile_id, location_id)
        
    db.commit()
    db.close()

  def insert_location(self):
    db = db_connection("location")
    cursor = db.cursor()

    cursor.execute("SELECT state_id from state_ml_table WHERE state_name = '{}'".format(self.state))
    state_id = cursor.fetchone()

    cursor.execute("SELECT country_id from country_table WHERE name = '{}'".format(self.country))
    country_id = cursor.fetchone()

    location_sql = """INSERT INTO location_table (coordinate, address_local_language, state_id, country_id, postal_code, created_user_id, updated_user_id)
                        VALUES (POINT(%s, %s), %s, %s, %s, %s, 0, 0)"""
    cursor.execute(location_sql, (self.latitude, self.longitude, self.address, state_id, country_id, self.postal_code))

    db.commit()
    db.close()

  def update_location(self, profile_id):
    db = db_connection("location")
    cursor = db.cursor()

    cursor.execute("SELECT state_id from state_ml_table WHERE state_name = '{}'".format(self.state))
    state_id = cursor.fetchone()

    cursor.execute("SELECT country_id from country_table WHERE name = '{}'".format(self.country))
    country_id = cursor.fetchone()

    location_id = self.get_location_id(profile_id)
    sql = "UPDATE location_table SET coordinate = POINT(%s, %s), address_local_language = %s, state_id = %s, country_id = %s, postal_code = %s WHERE id = %s"
    cursor.execute(sql, (self.latitude, self.longitude, self.address, state_id, country_id, self.postal_code, location_id))
    db.commit()

    db.close() 

  def insert_profile_telephone(self, profile_id):
    db = db_connection("profile_telephone")
    cursor = db.cursor()

    telephone_id = self.get_telephone_id(profile_id)
    sql = "INSERT INTO profile_telephone_table(profile_id, telephone_id) VALUES (%s, %s)"
    cursor.execute(sql, profile_id, telephone_id)
        
    db.commit()
    db.close()

  def insert_telephone(self, profile_id):
    db = db_connection("telephone")
    cursor = db.cursor()

    sql = "INSERT INTO telephone_table(profile_id, telephone, created_user_id, updated_user_id) VALUES (%s, %s, 0, 0)"
    cursor.execute(sql, (profile_id, self.telephone))
    db.commit()

    db.close()

  def update_telephone(self, profile_id):
    db = db_connection("telephone")
    cursor = db.cursor()

    telephone_id = self.get_telephone_id(profile_id)
    sql = "UPDATE telephone_table SET telephone = %s WHERE id = %s"
    cursor.execute(sql, (self.telephone, telephone_id))
    db.commit()

    db.close()

  def insert_profile_storage(self, profile_id):
    db = db_connection("profile_storage")
    cursor = db.cursor()

    storage_id = self.get_storage_id(profile_id)
    sql = "INSERT INTO profile_storage_table(profile_id, storage_id) VALUES (%s, %s)"
    cursor.execute(sql, profile_id, storage_id)
        
    db.commit()
    db.close()

  def insert_storage(self, profile_id):
    db = db_connection("storage")
    cursor = db.cursor()

    cursor.execute("SELECT id FROM file_type_table WHERE file_type = 'Photo'")
    file_type_id = cursor.fetchone()

    if not file_type_id:
      cursor.execute("INSERT INTO file_type_table(file_type) VALUE ('Photo')")
      db.commit()
      file_type_id = cursor.lastrowid
      cursor.execute("INSERT INTO file_type_ml_table(file_type_id, lang_code, name) VALUES (%s, 'en', 'Photo')")
      db.commit

    sql = "INSERT INTO storage_table(path, filename, file_type_id, created_user_id, updated_user_id) VALUES (%s, %s, %s, 0, 0)"
    filename = "profile_" + profile_id + "_photo"
    cursor.execute(sql, (self.photo, filename, file_type_id))
    db.commit()

    db.close()

  def update_storage(self, profile_id):
    db = db_connection("storage")
    cursor = db.cursor()

    storage_id = self.get_storage_id(profile_id)
    sql = "UPDATE storage_table SET path = %s WHERE id = %s"
    cursor.execute(sql, (self.photo, storage_id))
    db.commit()

    db.close()

  def insert_profile_reaction(self, profile_id):
    db = db_connection("profile_reaction")
    cursor = db.cursor()

    reaction_id = self.get_reaction_id(profile_id)
    sql = "INSERT INTO profile_reacion_table(profile_id, reaction_d) VALUES (%s, %s)"
    cursor.execute(sql, profile_id, reaction_id)
        
    db.commit()
    db.close()

  def insert_reaction(self):
    db = db_connection("reaction")
    cursor = db.cursor()

    cursor.execute("SELECT id FROM reaction_type_ml_table WHERE name = '{}'".format(self.reaction_type))
    reaction_type_id = cursor.fetchone()

    if not reaction_type_id:
      cursor.execute("INSERT INTO reaction_type_table VALUE (NULL))")
      db.commit()
      reaction_type_id = cursor.lastrowid

      sql_ml = "INSERT INTO reaction_type_ml_table(reaction_type_id, lang_code, name) VALUES (%s, %s, %s)"
      cursor.execute(sql_ml, (reaction_type_id, self.lang, self.reaction_type))
      
      db.commit()

    sql = "INSERT INTO reacion_table(value, reaction_type_id) VALUES (%s, %s)"
    cursor.execute(sql, self.reaction, reaction_type_id)
        
    db.commit()
    db.close()

  def update_reaction(self, profile_id):
    db = db_connection("reaction")
    cursor = db.cursor()

    reaction_id = self.get_reaction_id(profile_id)
    sql = "UPDATE reaction_table SET value = %s WHERE id = %s"
    cursor.execute(sql, (self.reaction, reaction_id))
    db.commit()

    db.close()

  def insert_operational_hours(self, profile_id):
    db = db_connection("operational_hours")
    cursor = db.cursor()

    location_id = self.get_location_id(profile_id)

    for day in self.hours:
      sql = "INSERT INTO operational_hours_table(profile_id, location_id, day_of_week, from, until) VALUES (%s, %s, %s, %s, %s)"
      cursor.execute(sql, (profile_id, location_id, day, day[0], day[1]))
      db.commit()

    db.close()

  def update_operational_hours(self, profile_id):
      db = db_connection("operational_hours")
      cursor = db.cursor()

      hours_rows = self.get_hours_ids(profile_id)
      for id, day, (start, end) in zip(hours_rows, self.hours.keys(), self.hours.values()):
        sql = "UPDATE operational_hours_table SET day_of_week = %s, from = %s, until = %s WHERE id = %s"
        cursor.execute(sql, (day, start, end, id))
        db.commit()

      db.close()
    


